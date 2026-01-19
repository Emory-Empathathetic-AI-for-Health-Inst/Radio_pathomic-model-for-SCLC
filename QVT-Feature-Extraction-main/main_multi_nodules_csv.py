import readData
import master_df
import features
import os
import numpy as np
import pandas as pd


def get_feature_names():
    """Generate feature names based on the exact order in overall_features.csv"""
    stats = ['mean', 'median', 'std', 'iqr', 'min', 'max', 'skew', 'kurt']

    # Basic features (first level)
    basic_features = ['diameter', 'length', 'tortuosity']

    # Curvature and torsion features (second level stats)
    second_level_features = ['curvature', 'torsion']
    second_level_stats = ['mean', 'median', 'std', 'iqr', 'min', 'max', 'skew', 'kurt']

    # Direction angle features
    direction_features = ['direction_angle' + stat for stat in [
        'mean', 'median', 'std', 'iqr', 'min', 'max', 'skew', 'kurt'
    ]]

    # Global features
    global_features = [
        'num_tumorfeeding',
        'prop_tumorfeeding',
        'fractal_mask',
        'fractal_skel',
        'meshvol',
        'voxelvol',
        'surfacearea',
        'surfvolumeratio'
    ]

    feature_names = []

    # Add basic features with their stats
    for feat in basic_features:
        for stat in stats:
            feature_names.append(f"{feat}_{stat}")

    # Add second level features (curvature and torsion) with their compound stats
    for feat in second_level_features:
        for first_stat in second_level_stats:
            for second_stat in stats:
                feature_names.append(f"{feat}_{first_stat}_{second_stat}")

    # Add direction angle features with their stats
    for feat in direction_features:
        for stat in stats:
            feature_names.append(f"{feat}_{stat}")

    # Add global features (no additional stats needed)
    feature_names.extend(global_features)

    # Add QVT_ prefix to all features
    feature_names = [f"{name}" for name in feature_names]

    return feature_names


def process_patient_data(patient_id, nodule_file):
    """Process data for a single patient and nodule"""
    try:
        ct_path = os.path.join(data_root_ct, patient_id, 'CT.nii.gz')
        nodule_path = os.path.join(data_root_mask, patient_id, nodule_file)

        # Read and process data
        data_obj = readData.read_data(ct_path, nodule_path)
        df = master_df.qvt(data_obj)
        f = features.compute_features(df)

        return f

    except Exception as e:
        print(f"Error processing {patient_id} - {nodule_file}: {str(e)}")
        return None


if __name__ == '__main__':
    # Set paths
    data_root_ct = r'E:\GT\Research\NLST\small_test\CT'
    data_root_mask = r'E:\GT\Research\NLST\small_test\Mask'
    result_path = r'E:\GT\Research\NLST\small_test\QVT'

    # Get all patient IDs
    patient_ids = [folder for folder in os.listdir(data_root_ct)
                   if os.path.isdir(os.path.join(data_root_ct, folder))]

    all_features = []
    nodule_ids = []

    # Process each patient
    for patient_id in patient_ids:
        print(f"Processing patient data: {patient_id}")
        try:
            # Get all nodule files for this patient
            mask_path = os.path.join(data_root_mask, patient_id)
            nodule_files = [f for f in os.listdir(mask_path)
                            if f.startswith('CT_nodule_') and f.endswith('.nii.gz')]

            # Process each nodule
            for nodule_file in nodule_files:
                nodule_id = nodule_file[:-7]  # Remove .nii.gz extension
                features_obj = process_patient_data(patient_id, nodule_file)

                if features_obj is not None:
                    # Extract feature vector - 修改这里以正确获取特征值
                    features_data = features_obj.feat_vec.iloc[0].values  # 使用iloc[0]因为feat_vec是转置的
                    all_features.append(features_data)
                    nodule_ids.append(f"{patient_id}_{nodule_id}")

            print(f"Finished processing patient data: {patient_id}")

        except Exception as e:
            print(f"Error processing patient data: {patient_id}")
            print(f"Error message: {str(e)}")

    # Create DataFrame with features
    feature_names = get_feature_names()
    df = pd.DataFrame(all_features, columns=feature_names)

    # Add nodule ID column
    df.insert(0, 'nodule_id', nodule_ids)

    # Save to CSV
    output_csv_path = os.path.join(result_path, 'qvt_features.csv')
    df.to_csv(output_csv_path, index=False)

    print(f"\nResults saved to: {output_csv_path}")
    print(f"Total features extracted: {len(feature_names)}")
    print(f"Total nodules processed: {len(nodule_ids)}")