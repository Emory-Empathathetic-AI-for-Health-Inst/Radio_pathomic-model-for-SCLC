# Textural-Feature-Extraction

Please use the code in `Script/Python-CPU/` folder

## Multiple Nodules Case

Run `Intra_tumoral_feature_extraction_new.py` and `Peri_tumoral_feature_extraction_new.py` (The output format is .mat)

If you want .csv output format, please run `Intra_tumoral_feature_extraction_csv.py` and `Peri_tumoral_feature_extraction_csv.py`


Set the ct/mask and save path:

```
input_path_ct = ''
input_path_mask = ''
result_path = ''
```

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
```

### Results

- **intra.mat**: feature matrix (Nx430)
- N means the number of samples. Each row represents a sample, and each column represents a feature
- **intra_nodule_list.mat**: the list of patients name (Nx1)

- **peri.mat**: feature matrix (Nx430)
- N means the number of samples. Each row represents a sample, and each column represents a feature
- **peri_nodule_list.mat**: the list of patients name (Nx1)

## One Nodule Case

Run `Intra_tumoral_feature_extraction_v2.py` and `Peri_tumoral_feature_extraction_v2.py`

Set the input path and save path:

```
input_path = ''
result_path = ''
```

### Data Structure

```
Dataset
│
├── patientID_folder1
│   ├── CT_T0.nii.gz
│   └── CT_T0-label.nii.gz
│
├── patientID_folder2
│   ├── CT_T0.nii.gz
│   └── CT_T0-label.nii.gz
│
└── patientID_folderN
```

You could change the name of input CT & SG in `process_file` function in `Intra_tumoral_feature_extraction_v2.py` and `Peri_tumoral_feature_extraction_v2.py`:

```
ct_path = os.path.join(input_path, file_name, 'CT_T0.nii.gz')
label_path = os.path.join(input_path, file_name, 'CT_T0-label.nii.gz')
```


## Requirement
Run in `python 3.10` version. 
Install the requirements:  \
`pip install -r requirements.txt`
```
numpy==1.26.4
nibabel==5.2.1
scipy==1.11.4
scikit-image==0.22.0
mahotas==1.4.13
opencv-python==4.9.0.80
matplotlib==3.8.0
```

## Performance Comparison

**Intra_tumoral_feature_extraction**

|      Version      |   Time    | Performance |
| :---------------: | :-------: | :---------: |
| MATLAB - original | 14378.6 s |     1x      |
| MATLAB - parallel | 3256.9 s  |    4.4x     |
|   Python - CPU    |  431.4 s  |    33.3x    |
|   Python - GPU    |     -     |      -      |

**Peri_tumoral_feature_extraction**

|      Version      |   Time    | Performance |
| :---------------: | :-------: | :---------: |
| MATLAB - original | 45659.8 s |     1x      |
| MATLAB - parallel | 12795.5 s |    3.6x     |
|   Python - CPU    |  596.8 s  |    76.5x    |
|   Python - GPU    |     -     |      -      |

**Test Condition:**\
Dataset: NLST-Cohort1 (249 patients)\
CPU: i9-13900H (14 cores 20 threads)


## Visualization

Run `heatmap_plot.py`\
(1) Plot the HeatMap of intra tumoral feature\
(2) Plot the HeatMap of Peri tumoral feature\
(3) Plot the Contour of the tumor

### Setting

```
ct_path = ''
mask_path = ''
num_slice = 103 # the index of slice
haralick_feature_index = 5   # the index of haralick features
gabor_feature_index = 8   # the index of gabor features
law_feature_index = 0   # the index of law features
alpha_value = 1   # Transparency of heatmap
peritumoral_flag = False   # Plot the heatmap of peritumoral
contour_flag = False   # Plot the contour of the tumor
```

### Example of Results

<img src="https://github.com/Emory-Empathathetic-AI-for-Health-Inst/Textural-Feature-Extraction/assets/114343446/83e79157-236e-4f85-a984-09b941bceb45" width="500" height="500">
<img src = "https://github.com/Emory-Empathathetic-AI-for-Health-Inst/Textural-Feature-Extraction/assets/114343446/1807afde-cc95-403a-aeed-436e76f63bec" width="500" height="500">
<img src = "https://github.com/Emory-Empathathetic-AI-for-Health-Inst/Textural-Feature-Extraction/assets/114343446/3b9e9a65-cb2d-4ebc-b264-8e72491ee7ef" width="400" height="400">


## Feature Name

Run `generate_feature_name.py` to get the csv file of 430 feature Name

In this project, we extract three types of texture features from medical images: Gabor features, Law's features, and Haralick features. For each feature, we compute five statistical measures to comprehensively characterize the feature distribution:


- Mean
- Standard Deviation (std)
- Skewness
- Kurtosis
- Median


**1. Gabor Features** (6 * 8 = 48 features)

Gabor features are obtained by applying Gabor filters to the image. Gabor filters are linear filters whose frequency and orientation representations are similar to those of the human visual system.

**f**: Frequency of the Gabor filter, taking values from [0, 2, 4, 8, 16, 32]. The frequency determines the filter's sensitivity to texture details.

**theta**: Orientation of the Gabor filter, taking values from [0, π/8, π/4, 3π/8, π/2, 5π/8, 3π/4, 7π/8]. The orientation determines the filter's sensitivity to texture direction.

**Example**
```
Gabor_f1_theta1_mean:
f1: f = 2
theta1: theta = π/8
statistical measures: Mean
```

**2. Law's Features** （5 * 5 = 25）

Law's features are obtained by applying a set of predefined filters (Law's filters) to the image. Law's filters are generated by multiplying all possible combinations of five one-dimensional filters (L5, E5, S5, W5, and R5).

- L5 (Level): [1, 4, 6, 4, 1]
- E5 (Edge): [-1, -2, 0, 2, 1]
- S5 (Spot): [-1, 0, 2, 0, -1]
- W5 (Wave): [-1, 2, 0, -2, 1]
- R5 (Ripple): [1, -4, 6, -4, 1]

The combinations like LL, LE, LS, LW, LR in Law's features represent the two-dimensional filters formed by multiplying different one-dimensional filters. For example, LL represents the product of L5 and L5, LE represents the product of L5 and E5, and so on.

**Example**
```
Laws_LE_skewness:
LE: L * E
statistical measures: Skewness
```

**3. Haralick Features** (13 features)

Haralick features are a set of texture features extracted from the Gray-Level Co-occurrence Matrix (GLCM) of an image. GLCM describes the spatial correlation of pixel intensities in the image. Haralick et al. defined 14 statistical measures to describe the GLCM, but usually only 13 of them are used.

- Haralick_1: Angular Second Moment (ASM)
- Haralick_2: Contrast
- Haralick_3: Correlation
- Haralick_4: Sum of Squares: Variance
- Haralick_5: Inverse Difference Moment (IDM)
- Haralick_6: Sum Average
- Haralick_7: Sum Variance
- Haralick_8: Sum Entropy
- Haralick_9: Entropy
- Haralick_10: Difference Variance
- Haralick_11: Difference Entropy
- Haralick_12: Information Measure of Correlation 1 (IMC1)
- Haralick_13: Information Measure of Correlation 2 (IMC2)

**Example**
```
Haralick_1_mean:
1:  Angular Second Moment (ASM)
statistical measures: Mean
```
## Contact

Aotian Chen - achen653@gatech.edu / achen41@emory.edu

