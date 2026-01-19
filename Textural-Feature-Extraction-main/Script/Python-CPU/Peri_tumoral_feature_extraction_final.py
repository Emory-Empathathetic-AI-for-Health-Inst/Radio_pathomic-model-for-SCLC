import os
import numpy as np
import time
import nibabel as nib
from skimage.measure import label
from skimage.util import img_as_float
from multiprocessing import Pool
from scipy.io import savemat
from scipy.stats import skew, kurtosis

from peritumoral import peritumoral
from extract_gabor import extract_gabor
from extract_law import extract_law
from extract_haralick import extract_haralick

# Set Path
input_path_ct = r'E:\GT\Research\BatchTest\CT_nii'
input_path_mask = r'E:\GT\Research\BatchTest\CT_pred_nodSep'
result_path = r'E:\GT\Research\BatchTest\results\intra_peri\new\peri'

def stat_ring(func):
    horz = []
    X1, X2, X3, X4, X5 = [], [], [], [], []
    k = func.shape[1]
    for j in range(k):
        x11 = func[:, j]
        x1 = np.mean(x11)
        x2 = np.median(x11)
        x3 = np.std(x11)
        x4 = skew(x11)
        x5 = kurtosis(x11)
        X1.append(x1)
        X2.append(x2)
        X3.append(x3)
        X4.append(x4)
        X5.append(x5)
    horz = np.hstack((X1, X2, X3, X4, X5))
    return horz

def process_file(file_name):
    print(f'\n{file_name}\n')

    # Read CT image
    ct_path = os.path.join(input_path_ct, file_name)
    V1a = nib.load(ct_path).get_fdata()

    # Find corresponding mask files
    ct_prefix = file_name[:-7]  # Remove .nii.gz extension
    mask_files = [f for f in os.listdir(input_path_mask) if f.startswith(ct_prefix + '_pred_nodule_')]

    print("File Name:", file_name)
    print("Mask:", mask_files)

    results = []

    for mask_file in mask_files:
        print(f'Processing mask file: {mask_file}')

        # Read CT mask
        mask_path = os.path.join(input_path_mask, mask_file)
        V2a = nib.load(mask_path).get_fdata()

        # Make sure the last slice is not split
        V1a_padded = np.dstack((V1a, np.zeros((V1a.shape[0], V1a.shape[1], 1))))
        V2a_padded = np.dstack((V2a, np.zeros((V2a.shape[0], V2a.shape[1], 1))))

        # Find the section with the tumor
        flag1 = 0
        first1 = []
        last1 = []
        n = 0
        for i in range(V2a_padded.shape[2]):
            B1 = V2a_padded[:, :, i]
            B1 = B1.astype(bool)
            L = label(B1, connectivity=1)
            X = np.sum(L > 0)
            if X > 0 and flag1 == 0:
                flag1 = 1
                n += 1
                first1.append(i)
            if (X == 0 and flag1 != 0) or i == V2a_padded.shape[2] - 1:
                if i != V2a_padded.shape[2] - 1:
                    last1.append(i - 1)
                    flag1 = 0
                else:
                    last1.append(i)
                    flag1 = 0

        B = np.zeros((V2a_padded.shape[2], 2))
        for j in range(n):
            for i in range(first1[j], last1[j] + 1):
                B1 = V2a_padded[:, :, i]
                B1 = img_as_float(B1)
                B[i, 0] = np.sum(B1)
                B[i, 1] = i

        traina_law = []
        traina_haralick = []
        traina_gabor = []

        for j in range(n):
            for i in range(first1[j], last1[j] + 1):
                Aa = V1a_padded[:, :, i]
                Ba = V2a_padded[:, :, i].astype(bool)
                A2a, B2a = peritumoral(Aa, Ba)

                # Gabor Feature
                print('\nExtracting Gabor..')
                Gabor_features, _ = extract_gabor(A2a, B2a)
                traina_gabor.extend(Gabor_features)

                # Law Feature
                print('\nExtracting Law..')
                law_features, _ = extract_law(A2a, B2a)
                traina_law.extend(law_features)

                # Haralick Feature
                print('\nExtracting Haralick..')
                haralick_features, _ = extract_haralick(A2a, B2a)
                traina_haralick.extend(haralick_features)

        peri_gabor = stat_ring(np.array(traina_gabor))
        peri_law = stat_ring(np.array(traina_law))
        peri_haralick = stat_ring(np.array(traina_haralick))

        peri = np.hstack((peri_gabor, peri_law, peri_haralick))

        results.append((peri, mask_file[:-7]))

    return results


if __name__ == '__main__':
    start_time = time.time()  # Record the running time

    files = os.listdir(input_path_ct)
    files = [f for f in files if f.endswith('.nii.gz')]

    peri_features = []
    file_list = []

    with Pool() as pool:
        results = pool.map(process_file, files)

    for file_results in results:
        for result in file_results:
            peri_features.append(result[0])
            file_list.append([result[1]])

    # Convert intra_file_list to cell array
    file_list = np.array(file_list, dtype=object)

    # Save the results
    peri = np.array(peri_features)
    savemat(os.path.join(result_path, 'peri.mat'), {'peri': peri})
    savemat(os.path.join(result_path, 'peri_file_list.mat'), {'peri_file_list': file_list})

    end_time = time.time()  # Record the end time
    print(f'Total execution time: {end_time - start_time:.2f} seconds')