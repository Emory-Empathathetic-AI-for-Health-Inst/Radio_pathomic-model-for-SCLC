from dependencies.computeBIFs import compute_bifs as computeBIFs
import numpy as np
import cv2
from skimage import measure, morphology
from PIL import Image
from dependencies.disorder_feat_extract import contrast_entropy as disorder_feat_extract
import math
import os
import pandas as pd
import matplotlib.pyplot as plt
import json 
winSizes = [200, 300, 400, 500, 600, 700, 800, 900, 1000]  # size of windows
filterScale = 3  # kernel size of the BIF model
orientCooccurScheme = 1
featureDescriptor = 5
orientBinInterval = 10
orientNum = 19
# will discard 0th bin in disorder_feat_extract.py, after discarding it will have 18 bins


patients_folder_path = "/media/himanshu/My Book/temp/"
temp_patches_folder_path = "/media/himanshu/My Book/temp/"
# # read json file
# with open("/home/himanshu/Documents/uh_patients_cleaned.json", "r") as f:
# 	patients_list = json.load(f)

	# TAKE A LOOK
patients_list= os.listdir(patients_folder_path)

column_names = ["patient"] + [f"cfod_{winSize}" for winSize in winSizes]
df = pd.DataFrame(columns=column_names)
# df = pd.DataFrame()

for idx_patient, patient in enumerate(patients_list):
# for idx_patient, patient in enumerate([605, 607]):

	# write the patient name to the df
	patient = str(patient)
	print(patient)
	# if patient != "1000947":
	# 	print("skipping")
	# 	continue
	patient = patient.split("/")[-1]
	# df.loc[idx_patient, "patient"] = patient	

	# patches_folder = f"{patients_folder_path}/{patient}/{patient}/"
	# patches_folder = f"{temp_patches_folder_path}/{patient}/"
	patches_folder = f"{temp_patches_folder_path}/{patient}/images/"

	stroma_mask_folder = f"{patients_folder_path}/{patient}/stromal_masks_images/"
	
	# tumor_mask_folder = f"{patients_folder_path}/{patient}/masks/"
	collagen_mask = f"{patients_folder_path}/{patient}/collagen_mask/"
	if not os.path.exists(patches_folder):
		print(f"Patient {patient} does not have patches")
		continue	
	# if (not os.path.exists(stroma_mask_folder) or not os.path.exists(collagen_mask)): 
	# 	if not os.path.exists(stroma_mask_folder):
	# 		print(f"Patient {patient} does not have stroma mask")
	# 		continue
	# 	if os.path.exists(collagen_mask):
	# 		if len(os.listdir(collagen_mask)) != len(os.listdir(patches_folder)):
	# 				print(f"Patient {patient} already has collagen mask")
	# 				continue

	patches_files = os.listdir(patches_folder)
	if len(patches_files) == 0:
		print(f"Patient {patient} has no patches")
		continue
	stroma_mask_files = os.listdir(stroma_mask_folder)
	
	# tumor_mask_files = os.listdir(tumor_mask_folder)

	parent_collagen_mask_path_prefix = f"{patients_folder_path}/{patient}/collagen_mask"
	os.makedirs(parent_collagen_mask_path_prefix, exist_ok=True)

	cfod_features_path = f"{patients_folder_path}/{patient}/cfod_features"
	os.makedirs(cfod_features_path, exist_ok=True)
	IMAGE_EXTENSION = ".png"


	# remove non image files from the list
	# patches_files = [file for file in patches_files if file.endswith(IMAGE_EXTENSION)]
	patches_files = [file for file in patches_files]
	stroma_mask_files = [file for file in stroma_mask_files if file.endswith(IMAGE_EXTENSION)]
	
	# tumor_mask_files = [file for file in tumor_mask_files if file.endswith(IMAGE_EXTENSION)]
	count_patches = 0
	feature_dict = {}
	for key in [f"cfod_{winSize}" for winSize in winSizes]:
		feature_dict[key] = []
	feature_dict["patient"] = patient
	# some files can be empty (its how it is)
	for file in patches_files:
		# file = file + IMAGE_EXTENSION
		# file_ = file + IMAGE_EXTENSION
		# tumor_file_path = os.path.join(patches_folder, file, file_)
		# stroma_mask_file_path = os.path.join(stroma_mask_folder, file_)
		# # file_ = file.replace("patch", "mask")
		# tumor_mask_file_path = os.path.join(tumor_mask_folder, file_)


		# file_ = file.replace("patch", "mask")
		# print(f"file: {file_}")
		tumor_file_path = os.path.join(patches_folder, file)

		file_s = file
		# print(file)
		# file_ = file.split("/")[0]
		# file_s = file.split("_")[1:]
		# file_s = "_".join(file_s) 

		# file_s = file.replace("patch_", "")
		# file_s = file_s.replace(".png", "_stroma.png")
		stroma_mask_file_path = os.path.join(stroma_mask_folder, file_s)


		
		# file_ = file.replace("patch", "mask")
		# tumor_mask_file_path = os.path.join(tumor_mask_folder, file_)
		

		# break
		# parameters setting
		# print(tumor_file_path)
		# check if the file exists
		if not os.path.exists(stroma_mask_file_path) or not os.path.exists(tumor_file_path):
			print(f"File does not exist: {tumor_file_path} or {stroma_mask_file_path}")
			continue
		stroma_mask = cv2.imread(stroma_mask_file_path, cv2.IMREAD_GRAYSCALE)
		stroma_mask = (stroma_mask > 0).astype(np.uint8)
		percentage_stroma = np.sum(stroma_mask) / (stroma_mask.shape[0] * stroma_mask.shape[1])
		if percentage_stroma < 0.30:
			print(f"Stroma percentage : {percentage_stroma}")
			continue
		
		# tumor_mask = cv2.imread(tumor_mask_file_path, cv2.IMREAD_GRAYSCALE)
		tumorSample = cv2.imread(tumor_file_path)
		tumorSample = cv2.cvtColor(tumorSample, cv2.COLOR_BGR2RGB)
		count_patches += 1
		# extract collagen fiber mask
		fragThresh = filterScale * 10
		bifs, jet = computeBIFs(tumorSample, filterScale, 0.1, 1)

		collagenMask = bifs == featureDescriptor
		collagenMask = collagenMask * stroma_mask


		collagenMask = morphology.remove_small_objects(collagenMask.astype(bool), min_size=fragThresh)
		collagenMask_name = file.split(".")[0] + "_collagen_mask.png"
		collagenMask_path = os.path.join(parent_collagen_mask_path_prefix, collagenMask_name)

		# NEVER USE plt.imsave TO SAVE BINARY IMAGES
		collagenMask = Image.fromarray(collagenMask)
		collagenMask.save(collagenMask_path)
		collagenMask = np.array(collagenMask)
		collagenMask = collagenMask.astype(np.uint16)
		collagenMask_np_u8 = collagenMask.copy().astype(np.uint8)
		contours, hierarchy = cv2.findContours(collagenMask_np_u8, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		# Iterate over the contours and assign a unique value to each polygon
		for i, contour in enumerate(contours):
			cv2.drawContours(collagenMask, [contour], -1, color=(i+1), thickness=-1)

		# collagen centroid and orientation information extraction
		properties = ('centroid', 'orientation', 'area')
		collogenProps = measure.regionprops_table(collagenMask, properties=properties)


		colgCenter = np.array([collogenProps['centroid-1'], collogenProps['centroid-0']]).T
		colgArea = collogenProps['area']
		colgOrient = collogenProps['orientation']

		
		colgOrient = np.array([math.degrees(orient) for orient in colgOrient])
		# colgOrientBin = np.fix(colgOrient / orientBinInterval) + 9
		# round will separate 9.9 and -9.9 into different bins 
		# haojia's np.fix makes the the same bin for between -9.99 and 9.99, 
		colgOrientBin = np.round(colgOrient / orientBinInterval) + 9

		
		stepSize = winSize // 2
		# stepSize = winSize
		for winSize in winSizes:
			cfodMap = np.zeros((int((tumorSample.shape[0] - winSize) / stepSize) + 1, int((tumorSample.shape[1] - winSize) / stepSize) + 1, 13))

			height, width = collagenMask.shape
		
			for win_x in range(0, width - winSize + 1, stepSize):
					for win_y in range(0, height - winSize + 1, stepSize):
							in_window_indices = np.where(
									(colgCenter[:, 0] >= win_x) & 
									(colgCenter[:, 0] < win_x + winSize) & 
									(colgCenter[:, 1] >= win_y) & 
									(colgCenter[:, 1] < win_y + winSize)
							)
							in_window_indices = in_window_indices[0]
							if len(in_window_indices) >= 5:
									inwinColgOrient = colgOrientBin[in_window_indices]
									inwinColgArea = colgArea[in_window_indices]
									orientOccurFeats = disorder_feat_extract(inwinColgOrient, inwinColgArea, orientNum, orientCooccurScheme)
									if orientOccurFeats is not None:
										cfodMap[win_y // stepSize, win_x // stepSize, :] = np.array(list(orientOccurFeats.values()))
			
			contrast_entropy = cfodMap[:,:,4]
			# remove nan values
			contrast_entropy = np.nan_to_num(contrast_entropy)
			
			# save the cfodMap[:,:,4] to a numpy file
			prefix_folder_path = f"{cfod_features_path}/{winSize}/"
			# if not os.path.exists(prefix_folder_path):
			# 	os.makedirs(prefix_folder_path)
			# np.save(prefix_folder_path + collagenMask_name.split(".")[0] + "_cfod.npy", contrast_entropy.T)
			contrast_entropy = contrast_entropy.flatten()
			contrast_entropy = contrast_entropy.tolist()
			feature_dict[f"cfod_{winSize}"].append(contrast_entropy)
			
	# make a pandas dataframe from the feature_dict
	# dump the feature_dict to a json file
	with open(f"{patients_folder_path}{patient}/cfod_features/cfod_features.json", "w") as f:
		json.dump(feature_dict, f)
	# df = pd.concat([df, pd.DataFrame(feature_dict)], ignore_index=True)
	# df.to_csv(f"{patients_folder_path}TCGA_Peri.csv", index=False)


	# 		mean = 0
	# 		max_val = 0
	# 		current_feature_ = cfodMap[:,:,4]
	# 		current_feature_ = np.nan_to_num(current_feature_)
	# 		mean += np.mean(current_feature_)
	# 		max_val = max(max_val, np.max(current_feature_))

	# patient_mean = mean / len(patches_files)
	# patient_max = max_val
	# print(f"Patient mean: {patient_mean}", f"Patient max: {patient_max}")
	# df.loc[idx_patient, "mean"] = patient_mean
	# df.loc[idx_patient, "max"] = patient_max

			# create a histogram of the cfodMap[:,:,4] and save it to df with patient name
	# 		entropy_map = cfodMap[:,:,4]
	# 		entropy_map = entropy_map.flatten()
			
	# 		entropy_map = entropy_map / np.max(entropy_map)
	# 		bins = np.arange(0, 1.1, 0.1)

	# 		hist, bin_edges = np.histogram(entropy_map, bins=bins, range=(0, 1))
			
	# 		# add the hist values to the old hist values
	# 		df.iloc[idx_patient, 1:] += hist
	# df.iloc[idx_patient, 1:] = df.iloc[idx_patient, 1:] // len(patches_files)
	

# save the df to a csv file
# df.to_csv("cfod_features_mean_max.csv", index=False)


