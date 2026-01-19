import os
import numpy as np
import time
import nibabel as nib
import pandas as pd
from scipy.stats import skew, kurtosis
from skimage.measure import label
from skimage.util import img_as_float
from multiprocessing import Pool

from extract_gabor import extract_gabor
from extract_law import extract_law
from extract_haralick import extract_haralick

# Set the path
input_path_ct = r'E:\GT\Research\NLST\small_test\CT'
input_path_mask = r'E:\GT\Research\NLST\small_test\Mask'
result_path = r'E:\GT\Research\NLST\small_test\TEX\intra'


def generate_feature_names():
    """Generate feature names for all extracted features"""
    stats = ['mean', 'median', 'std', 'skewness', 'kurtosis']

    # Gabor feature names
    gabor_features = [f'Intra_Gabor_f{f}_theta{t}_{s}'
                      for f in [0, 2, 4, 8, 16, 32]
                      for t in range(8)
                      for s in stats]

    # Law's feature names
    laws_bases = ['L', 'E', 'S', 'W', 'R']
    laws_features = [f'Intra_Laws_{a}{b}_{s}'
                     for a in laws_bases
                     for b in laws_bases
                     for s in stats]

    # Haralick feature names
    haralick_features = [f'Intra_Haralick_{i}_{s}'
                         for i in range(1, 14)
                         for s in stats]

    return gabor_features + laws_features + haralick_features


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


def process_patient(patient_id):
    print(f'\nProcessing Patient: {patient_id}\n')

    # Read CT image
    ct_path = os.path.join(input_path_ct, patient_id, 'CT.nii.gz')
    V1a = nib.load(ct_path).get_fdata()

    # Find corresponding mask files
    mask_path = os.path.join(input_path_mask, patient_id)
    mask_files = [f for f in os.listdir(mask_path)
                  if f.startswith('CT_nodule_') and f.endswith('.nii.gz')]

    print("Patient ID:", patient_id)
    print("Mask Files:", mask_files)

    results = []

    for mask_file in mask_files:
        print(f'Processing mask file: {mask_file}')

        # Read CT mask
        mask_file_path = os.path.join(mask_path, mask_file)
        V2a = nib.load(mask_file_path).get_fdata()

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
            if X == 0 and flag1 != 0:
                last1.append(i - 1)
                flag1 = 0

        traina_law = []
        traina_haralick = []
        traina_gabor = []

        for j in range(n):
            if last1[j] > first1[j] + 10:
                slice_range = range(first1[j], last1[j] + 1, 2)
            else:
                slice_range = range(first1[j], last1[j] + 1)

            for i in slice_range:
                try:
                    Aa = V1a_padded[:, :, i]
                    Ba = V2a_padded[:, :, i].astype(bool)
                    A2a = Aa
                    B2a = Ba

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
                except IndexError as e:
                    print(f'Error processing {patient_id} at index {i}: {e}')
                    break

        intra_gabor = stat_ring(np.array(traina_gabor))
        intra_law = stat_ring(np.array(traina_law))
        intra_haralick = stat_ring(np.array(traina_haralick))

        intra = np.hstack((intra_gabor, intra_law, intra_haralick))

        results.append((intra, f"{patient_id}_{mask_file[:-7]}"))

    return results


if __name__ == '__main__':
    start_time = time.time()

    patient_ids = os.listdir(input_path_ct)

    intra_features = []
    nodule_ids = []

    # Process all patients using multiprocessing
    with Pool() as pool:
        results = pool.map(process_patient, patient_ids)

    # Collect results
    for patient_results in results:
        for result in patient_results:
            intra_features.append(result[0])
            nodule_ids.append(result[1])

    # Create DataFrame with feature names
    feature_names = generate_feature_names()
    df = pd.DataFrame(intra_features, columns=feature_names)

    # Add nodule ID column
    df.insert(0, 'nodule_id', nodule_ids)

    # Save to CSV
    output_csv_path = os.path.join(result_path, 'intra_features.csv')
    df.to_csv(output_csv_path, index=False)

    end_time = time.time()
    print(f'Total execution time: {end_time - start_time:.2f} seconds')
    print(f'Results saved to: {output_csv_path}')