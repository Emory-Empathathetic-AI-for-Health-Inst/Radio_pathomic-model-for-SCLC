import readData
import master_df
import features
import os
import scipy.io as sio
import numpy as np


def process_patient_data(patient_id, nodule_file):
    ct_path = os.path.join(data_root_ct, patient_id, 'CT.nii.gz')
    nodule_path = os.path.join(data_root_mask, patient_id, nodule_file)
    data_obj = readData.read_data(ct_path, nodule_path)
    df = master_df.qvt(data_obj)
    f = features.compute_features(df)
    return f


if __name__ == '__main__':
    data_root_ct = r'E:\GT\Research\NLST\All_NLST\Data\3k\test\CT'
    data_root_mask = r'E:\GT\Research\NLST\All_NLST\Data\3k\test\Mask'
    result_path = r'E:\GT\Research\NLST\All_NLST\Data\3k\test\Results'

    patient_ids = [folder for folder in os.listdir(data_root_ct) if os.path.isdir(os.path.join(data_root_ct, folder))]

    all_features = []
    nodule_list = []

    for patient_id in patient_ids:
        print(f"Processing patient data: {patient_id}")
        try:
            mask_path = os.path.join(data_root_mask, patient_id)
            nodule_files = [f for f in os.listdir(mask_path) if f.startswith('CT_nodule_') and f.endswith('.nii.gz')]

            for nodule_file in nodule_files:
                nodule_id = nodule_file[:-7]  # Remove .nii.gz extension
                features_data = process_patient_data(patient_id, nodule_file)
                all_features.append(features_data.feat_vec.squeeze())
                nodule_list.append(f"{patient_id}_{nodule_id}")

            print(f"Finished processing patient data: {patient_id}")
        except Exception as e:
            print(f"Error processing patient data: {patient_id}")
            print(f"Error message: {str(e)}")

    # Combine the eigenvectors of all nodes into a matrix
    feature_matrix = np.vstack(all_features)

    # Save the feature matrix to a .mat file
    features_mat_file = os.path.join(result_path, 'QVT_features.mat')
    sio.savemat(features_mat_file, {'features': feature_matrix})
    print(f"Features saved to {features_mat_file}")

    # Save a list of nodes as a .mat file of the specified type
    nodule_list_array = np.array(nodule_list, dtype=object)
    save_path_ids = os.path.join(result_path, 'nodule_list.mat')
    sio.savemat(save_path_ids, {'nodule_list': nodule_list_array.reshape(-1, 1)})
    print(f"Nodule list saved to {save_path_ids}")