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
input_path = r'E:\GT\Research\NLST\Cohort1_T1_Cohort2_T2(flip_mask)\test\Data'
result_path = r'E:\GT\Research\NLST\Cohort1_T1_Cohort2_T2(flip_mask)\test\Peri'

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

def process_file(args):
    file_index, files = args
    file_name = files[file_index]
    print(f'\n{file_name}\n')

    # Read CT image and CT mask
    ct_path = os.path.join(input_path, file_name, 'CT_T1.nii.gz')
    label_path = os.path.join(input_path, file_name, 'CT_T1-label.nii.gz')

    V1a = nib.load(ct_path).get_fdata()
    V2a = nib.load(label_path).get_fdata()

    # Make sure the last slice is not split
    V1a = np.dstack((V1a, np.zeros((V1a.shape[0], V1a.shape[1], 1))))
    V2a = np.dstack((V2a, np.zeros((V2a.shape[0], V2a.shape[1], 1))))

    # Find the section with the tumor
    flag1 = 0
    first1 = []
    last1 = []
    n = 0
    for i in range(V2a.shape[2]):
        B1 = V2a[:, :, i]
        B1 = B1.astype(bool)
        L = label(B1, connectivity=1)
        X = np.sum(L > 0)
        if X > 0 and flag1 == 0:
            flag1 = 1
            n += 1
            first1.append(i)
        if (X == 0 and flag1 != 0) or i == V2a.shape[2] - 1:
            if i != V2a.shape[2] - 1:
                last1.append(i - 1)
                flag1 = 0
            else:
                last1.append(i)
                flag1 = 0

    B = np.zeros((V2a.shape[2], 2))
    for j in range(n):
        for i in range(first1[j], last1[j] + 1):
            B1 = V2a[:, :, i]
            B1 = img_as_float(B1)
            B[i, 0] = np.sum(B1)
            B[i, 1] = i

    traina_law = []
    traina_haralick = []
    traina_gabor = []

    for j in range(n):
        for i in range(first1[j], last1[j] + 1):
            Aa = V1a[:, :, i]
            Ba = V2a[:, :, i].astype(bool)
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

    return peri, file_name


if __name__ == '__main__':
    start_time = time.time()  # Record the running time

    files = os.listdir(input_path)
    files = [f for f in files if os.path.isdir(os.path.join(input_path, f))]

    num_files = len(files)
    peri_features = [None] * num_files
    peri_file_list = [None] * num_files

    with Pool() as pool:
        results = pool.map(process_file, [(i, files) for i in range(num_files)])

    for i, result in enumerate(results):
        peri_features[i] = result[0]
        peri_file_list[i] = [result[1]]

    # Convert peri_file_list to cell array
    peri_file_list = np.array(peri_file_list, dtype=object)

    # Save the results
    peri = np.array(peri_features)
    savemat(os.path.join(result_path, 'peri.mat'), {'peri': peri})
    savemat(os.path.join(result_path, 'peri_file_list.mat'), {'peri_file_list': peri_file_list})

    end_time = time.time()  # Record the end time
    print(f'Total execution time: {end_time - start_time:.2f} seconds')