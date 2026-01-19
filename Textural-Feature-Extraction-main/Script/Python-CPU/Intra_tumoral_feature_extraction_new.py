import os
import numpy as np
import time
import nibabel as nib
from scipy.io import savemat
from skimage.measure import label
from skimage.util import img_as_float
from multiprocessing import Pool
from scipy.stats import skew, kurtosis

from extract_gabor import extract_gabor
from extract_law import extract_law
from extract_haralick import extract_haralick

# Set the path
input_path_ct = r'/users/PCON0521/achen653/6254/VA/benign_first_timepoint_200/benign_first_timepoint_200/CT'
input_path_mask = r'/users/PCON0521/achen653/6254/VA/benign_first_timepoint_200/benign_first_timepoint_200/Mask'
result_path = r'/users/PCON0521/achen653/6254/VA/benign_first_timepoint_200/benign_first_timepoint_200/Results/TEX/intra'

# Record the error
error_log = os.path.join(result_path, 'error_log_intra.txt')



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
    try:
        print(f'\nProcessing Patient: {patient_id}\n')
    
        # Read CT image
        ct_path = os.path.join(input_path_ct, patient_id, 'CT.nii.gz')
        V1a = nib.load(ct_path).get_fdata()
    
        # Find corresponding mask files
        mask_path = os.path.join(input_path_mask, patient_id)
        mask_files = [f for f in os.listdir(mask_path) if f.startswith('CT_nodule_') and f.endswith('.nii.gz')]
    
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
                if last1[j] > first1[j] + 10:
                    for i in range(first1[j], last1[j] + 1, 2):
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
                else:
                    for i in range(first1[j], last1[j] + 1):
                        try:
                            Aa = V1a_padded[:, :, i]
                        except IndexError as e:
                            print(f'Error processing {patient_id} at index {i}: {e}')
                            break
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
    
            intra_gabor = stat_ring(np.array(traina_gabor))
            intra_law = stat_ring(np.array(traina_law))
            intra_haralick = stat_ring(np.array(traina_haralick))
    
            intra = np.hstack((intra_gabor, intra_law, intra_haralick))
    
            results.append((intra, f"{patient_id}_{mask_file[:-7]}"))
    
        return results

    except Exception as e:
        # 1) 记录失败的 patient_id 和错误信息
        with open(error_log, 'a') as fout:
            fout.write(f'{patient_id}\t{str(e)}\n')
        # 2) 跳过：返回空列表，后续会被忽略
        return []


if __name__ == '__main__':
    
    os.makedirs(result_path, exist_ok=True)
    
    open(error_log, 'w').close()

    start_time = time.time()  # Record the running time

    patient_ids = os.listdir(input_path_ct)

    intra_features = []
    nodule_list = []

    # with Pool() as pool:
    with Pool(processes=40) as pool:
        results = pool.map(process_patient, patient_ids)

    # 只保留非空的
    valid_results = [r for r in results if r]

    for patient_results in valid_results:
        for intra, name in patient_results:
            intra_features.append(intra)
            nodule_list.append([name])

    # Convert nodule_list to cell array
    nodule_list = np.array(nodule_list, dtype=object)

    # Save the results
    intra = np.array(intra_features)
    savemat(os.path.join(result_path, 'intra.mat'), {'intra': intra})
    savemat(os.path.join(result_path, 'intra_nodule_list.mat'), {'intra_nodule_list': nodule_list})

    end_time = time.time()  # Record the end time
    print(f'Total execution time: {end_time - start_time:.2f} seconds')
