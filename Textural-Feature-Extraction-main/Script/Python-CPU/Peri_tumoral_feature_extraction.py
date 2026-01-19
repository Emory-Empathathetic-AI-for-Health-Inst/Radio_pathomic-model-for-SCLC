import os
import numpy as np
import time
import nibabel as nib
from skimage.measure import label
from skimage.util import img_as_float
from multiprocessing import Pool
from scipy.io import savemat

from peritumoral import peritumoral
from extract_gabor import extract_gabor
from extract_law import extract_law
from extract_haralick import extract_haralick

# Set Path
input_path = 'E:/GT/Research/feature_extraction_evaluation/CCF'
result_path = 'E:/GT/Research/feature_extraction_evaluation/CCF_for_feature_extraction/peri_feature'

def process_file(args):
    file_index, files = args
    file_name = files[file_index]
    print(f'\n{file_name}\n')

    # Read CT image and CT mask
    ct_path = os.path.join(input_path, file_name, 'CT_T0.nii.gz')
    label_path = os.path.join(input_path, file_name, 'CT_T0-label.nii.gz')

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
            # print(f'Gabor features size: {[f.shape for f in Gabor_features]}')

            # Law Feature
            print('\nExtracting Law..')
            law_features, _ = extract_law(A2a, B2a)
            traina_law.extend(law_features)
            # print(f'Law features size: {law_features.shape}')

            # Haralick Feature
            print('\nExtracting Haralick..')
            haralick_features, _ = extract_haralick(A2a, B2a)
            traina_haralick.extend(haralick_features)
            # print(f'Haralick features size: {haralick_features.shape}')

    return traina_law, traina_haralick, traina_gabor, file_name


if __name__ == '__main__':
    start_time = time.time()  # Record the running time


    files = os.listdir(input_path)
    files = [f for f in files if os.path.isdir(os.path.join(input_path, f))]

    num_files = len(files)
    law_peri = [None] * num_files
    haralick_peri = [None] * num_files
    gabor_peri = [None] * num_files
    peri_file_list = [None] * num_files

    with Pool() as pool:
        results = pool.map(process_file, [(i, files) for i in range(num_files)])

    for i, result in enumerate(results):
        law_peri[i] = [result[0]]
        haralick_peri[i] = [result[1]]
        gabor_peri[i] = [result[2]]
        peri_file_list[i] = [result[3]]

    # Convert intra_file_list to cell array
    peri_file_list = np.array(peri_file_list, dtype=object)

    # Save the results
    savemat(os.path.join(result_path, 'law_peri.mat'), {'law_peri': law_peri})
    savemat(os.path.join(result_path, 'haralick_peri.mat'), {'haralick_peri': haralick_peri})
    savemat(os.path.join(result_path, 'gabor_peri.mat'), {'gabor_peri': gabor_peri})
    savemat(os.path.join(result_path, 'peri_file_list.mat'), {'peri_file_list': peri_file_list})

    end_time = time.time()  # Record the end time
    print(f'Total execution time: {end_time - start_time:.2f} seconds')

# NLST-Cohort1: Peri: 596.88 seconds

# NLST-Cohort2: Peri: 501.51 seconds

# CCF: Peri: 1669.61 seconds