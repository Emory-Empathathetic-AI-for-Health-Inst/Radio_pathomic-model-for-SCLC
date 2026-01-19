import readData
import master_df
import features
import os
import scipy.io as sio
import numpy as np

def process_patient_data(patient_folder):
    data_obj = readData.read_data(patient_folder)
    df = master_df.qvt(data_obj)
    # df.plot_region() # For some plots
    # df.plot_graph() # For some plots
    f = features.compute_features(df)
    # f.plot_feature('tortuosity')
    return f


if __name__ == '__main__':
    test_samples_folder = r'E:\GT\Research\NLST\sample_test\C1'
    patient_folders = [os.path.join(test_samples_folder, folder) for folder in os.listdir(test_samples_folder)]

    all_features = []
    patient_ids = []

    for patient_folder in patient_folders:
        patient_id = os.path.basename(patient_folder)
        print(f"Processing patient data: {patient_id}")
        try:
            features_data = process_patient_data(patient_folder)
            all_features.append(features_data.feat_vec.squeeze())
            patient_ids.append(patient_id)
            print(f"Finished processing patient data: {patient_id}")
        except Exception as e:
            print(f"Error processing patient data: {patient_id}")
            print(f"Error message: {str(e)}")

    # 将所有患者的特征向量组合成一个矩阵
    feature_matrix = np.vstack(all_features)

    # 将特征矩阵保存到 .mat 文件中
    data_root = r'E:\GT\Research\NLST\sample_test\Results'
    features_mat_file = os.path.join(data_root, 'QVT_features.mat')
    sio.savemat(features_mat_file, {'features': feature_matrix})
    print(f"Features saved to {features_mat_file}")

    # 将 patientID 保存为指定类型的 .mat 文件
    patient_ids_array = np.array(patient_ids, dtype=object)
    save_path_ids = os.path.join(data_root, 'patientID.mat')
    sio.savemat(save_path_ids, {'patientID': patient_ids_array})
    print(f"Patient IDs saved to {save_path_ids}")
