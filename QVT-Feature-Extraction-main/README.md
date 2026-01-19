Please run the `main_multi_nodules.py` for multiple nodules cases. (The output format is .mat)

If you want the .csv output format, please run `main_multi_nodules_csv.py`

### Data Structure

```
CT
│
├── patientID_folder1
│   └── CT.nii.gz
│
├── patientID_folder2
│   └── CT.nii.gz
│
└── patientID_folderN
```

```
Mask
│
├── patientID_folder1
│   ├── CT_nodule_1.nii.gz
│   ├── CT_nodule_2.nii.gz
│   ...
│   └── CT_nodule_n.nii.gz
|   
│
├── patientID_folder2
│   ├── CT_nodule_1.nii.gz
│   └── CT_nodule_2.nii.gz
│
└── patientID_folderN
