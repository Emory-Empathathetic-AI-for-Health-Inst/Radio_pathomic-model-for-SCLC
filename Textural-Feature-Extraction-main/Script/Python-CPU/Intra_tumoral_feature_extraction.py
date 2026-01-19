import os
import numpy as np
import time
import nibabel as nib
from scipy.io import savemat
from skimage.measure import label
from skimage.util import img_as_float
from multiprocessing import Pool

from extract_gabor import extract_gabor
from extract_law import extract_law
from extract_haralick import extract_haralick

# Set the path
input_path = 'E:/GT/Research/feature_extraction_evaluation/CCF'
result_path = 'E:/GT/Research/feature_extraction_evaluation/CCF_for_feature_extraction/intra_feature'


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
        if X == 0 and flag1 != 0:
            last1.append(i - 1)
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
        if last1[j] > first1[j] + 10:
            for i in range(first1[j], last1[j] + 1, 2):
                Aa = V1a[:, :, i]
                Ba = V2a[:, :, i].astype(bool)
                A2a = Aa
                B2a = Ba

                # Gabor Feature
                print('\nExtracting Gabor..')
                Gabor_features, _ = extract_gabor(A2a, B2a)
                traina_gabor.extend(Gabor_features)
                # print(f'Gabor features size: {Gabor_features.shape}')

                # Law Feaature
                print('\nExtracting Law..')
                law_features, _ = extract_law(A2a, B2a)
                traina_law.extend(law_features)
                # print(f'Law features size: {law_features.shape}')

                # Haralick Feature
                print('\nExtracting Haralick..')
                haralick_features, _ = extract_haralick(A2a, B2a)
                traina_haralick.extend(haralick_features)
                # print(f'Haralick features size: {haralick_features.shape}')
        else:
            for i in range(first1[j], last1[j] + 1):
                Aa = V1a[:, :, i]
                Ba = V2a[:, :, i].astype(bool)
                A2a = Aa
                B2a = Ba

                # Gabor Feature
                print('\nExtracting Gabor..')
                Gabor_features, _ = extract_gabor(A2a, B2a)
                traina_gabor.extend(Gabor_features)
                # print(f'Gabor features size: {Gabor_features.shape}')

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
    start_time = time.time()   # Record the running time

    files = os.listdir(input_path)
    files = [f for f in files if os.path.isdir(os.path.join(input_path, f))]

    num_files = len(files)
    law_intra = [None] * num_files
    haralick_intra = [None] * num_files
    gabor_intra = [None] * num_files
    intra_file_list = [None] * num_files

    with Pool() as pool:
        results = pool.map(process_file, [(i, files) for i in range(num_files)])

    for i, result in enumerate(results):
        law_intra[i] = [result[0]]
        haralick_intra[i] = [result[1]]
        gabor_intra[i] = [result[2]]
        intra_file_list[i] = [result[3]]

    # Convert intra_file_list to cell array
    intra_file_list = np.array(intra_file_list, dtype=object)

    # Save the results
    savemat(os.path.join(result_path, 'law_intra.mat'), {'law_intra': law_intra})
    savemat(os.path.join(result_path, 'haralick_intra.mat'), {'haralick_intra': haralick_intra})
    savemat(os.path.join(result_path, 'gabor_intra.mat'), {'gabor_intra': gabor_intra})
    savemat(os.path.join(result_path, 'intra_file_list.mat'), {'intra_file_list': intra_file_list})

    end_time = time.time()  # Record the end time
    print(f'Total execution time: {end_time - start_time:.2f} seconds')

# NLST-Cohort1: Intra: 431.40 seconds

# NLST-Cohort2: Intra: 310.82 seconds

# CCF: Intra: 890.74 seconds