import os
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import cv2

from extract_haralick import extract_haralick
from extract_law import extract_law
from extract_gabor import extract_gabor
from peritumoral import peritumoral


def load_data(ct_path, mask_path, num_slice):
    """
     Load CT image and segmentation mask for a specified slice.

    :param ct_path: Path to the CT image file.
    :param mask_path: Path to the segmentation mask file.
    :param num_slice: The index of the desired slice.
    :return: A tuple containing the CT slice (A) and the corresponding binary mask (B).
    """
    V1a = nib.load(ct_path).get_fdata()
    V2a = nib.load(mask_path).get_fdata()
    A = V1a[:, :, num_slice]
    B = V2a[:, :, num_slice].astype(bool)
    return A, B


def extract_features(A, B, haralick_feature_index, gabor_feature_index, law_feature_index):
    """
    Extract Haralick, Gabor, and Law features from the given image and mask.

    :param A: The input image.
    :param B: The binary mask indicating the region of interest.
    :param haralick_feature_index: The index of the desired Haralick feature.
    :param gabor_feature_index: The index of the desired Gabor feature.
    :param law_feature_index: The index of the desired Law feature.
    :return: A tuple containing the extracted Haralick, Gabor, and Law features.
    """

    _, hara_list = extract_haralick(A, B)
    _, gab_list = extract_gabor(A, B)
    _, law_list = extract_law(A, B)

    hara_new = np.zeros((512, 512))
    gab_new = np.zeros((512, 512))
    law_new = np.zeros((512, 512))

    for i in range(512):
        for j in range(512):
            if B[i, j]:
                hara_new[i, j] = hara_list[i, j, haralick_feature_index]
                gab_new[i, j] = gab_list[gabor_feature_index][i, j]
                law_new[i, j] = law_list[i, j, law_feature_index]

    return hara_new, gab_new, law_new


def create_alpha_matrix(A, B, alpha_value):
    """
    Create an alpha matrix for transparency based on the binary mask.

    :param A: The input image (used to determine the matrix size).
    :param B: The binary mask indicating the region of interest.
    :param alpha_value: transparency
    :return: The alpha matrix.
    """
    alpha = np.zeros_like(A)
    alpha[B] = alpha_value
    return alpha


def plot_heatmap(A, feat_new, B, feat_name, alpha):
    """
    Plot a heatmap of the extracted feature overlaid on the CT image.

    :param A: The input CT image.
    :param feat_new: The extracted feature map.
    :param B: The binary mask indicating the region of interest.
    :param feat_name: The name of the feature being plotted.
    :param alpha: The alpha matrix for transparency.
    """
    plt.figure(figsize=(8, 8))
    plt.imshow(np.rot90(A, 1), cmap='gray')
    im = plt.imshow(np.rot90(feat_new, 1), cmap='jet', alpha=np.rot90(alpha, 1))
    im.set_clim(np.min(feat_new[B]), np.max(feat_new[B]))

    cbar = plt.colorbar(im, label=f'{feat_name} Feature Value')
    plt.title(f'{feat_name} Feature Heatmap Overlaid on CT Image (Tumor Region Only)')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def plot_contour(A, B):
    """
    Plot the contour of the tumor on the CT image.

    :param A: The input CT image.
    :param B: The binary mask indicating the tumor region.
    """
    plt.figure(figsize=(8, 8))
    plt.imshow(np.rot90(A, 1), cmap='gray')
    # Find the contour of the mask and plot it
    contours, _ = cv2.findContours(np.rot90(B, 1).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        plt.plot(contour[:, 0, 0], contour[:, 0, 1], linewidth=2, color='r')
    plt.title(f'Contour of the tumor')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def main(ct_path, mask_path, num_slice, haralick_feature_index, gabor_feature_index, law_feature_index, alpha_value, peritumoral_flag=False, contour_flag=False):
    """
    main function: Plot (1) contour of the tumor (2) Intra features HeatMap (3) Peri features HeatMap

    :param ct_path: Path to the CT image file.
    :param mask_path: Path to the segmentation mask file.
    :param num_slice: The index of the desired slice.
    :param haralick_feature_index: The index of the desired Haralick feature.
    :param gabor_feature_index: The index of the desired Gabor feature.
    :param law_feature_index: The index of the desired Law feature.
    :param alpha_value: The alpha value for transparency.
    :param peritumoral_flag: Flag indicating whether to plot peritumoral features (default: False).
    :param contour_flag: Flag indicating whether to plot the tumor contour (default: False).
    """
    A, B = load_data(ct_path, mask_path, num_slice)

    if contour_flag: # Plot the contour of the tumor
        plot_contour(A, B)
    else:
        if peritumoral_flag:  # Plot the peri tumor features HeatMap
            A_peri, B_peri = peritumoral(A, B)
            hara_new, gab_new, law_new = extract_features(A_peri, B_peri, haralick_feature_index, gabor_feature_index,
                                                          law_feature_index)
            alpha = create_alpha_matrix(A, B_peri, alpha_value)

            plot_heatmap(A, gab_new, B_peri, 'Gabor', alpha)
            plot_heatmap(A, law_new, B_peri, 'Law', alpha)
            plot_heatmap(A, hara_new, B_peri, 'Haralick', alpha)
        else:  # Plot the intra tumor features HeatMap
            hara_new, gab_new, law_new = extract_features(A, B, haralick_feature_index, gabor_feature_index, law_feature_index)
            alpha = create_alpha_matrix(A, B, alpha_value)

            plot_heatmap(A, gab_new, B, 'Gabor', alpha)
            plot_heatmap(A, law_new, B, 'Law', alpha)
            plot_heatmap(A, hara_new, B, 'Haralick', alpha)


if __name__ == '__main__':
    ct_path = 'E:\\GT\\Research\\NLST\\Cohort1_T1_Cohort2_T2(flip_mask)\\Cohort2_for_feature_extraction\\106553\\CT_T2.nii.gz'
    mask_path = 'E:\\GT\\Research\\NLST\\Cohort1_T1_Cohort2_T2(flip_mask)\\Cohort2_for_feature_extraction\\106553\\CT_T2-label.nii.gz'
    num_slice = 102
    haralick_feature_index = 5
    gabor_feature_index = 8
    law_feature_index = 0
    alpha_value = 1
    peritumoral_flag = False
    contour_flag = False

    main(ct_path, mask_path, num_slice, haralick_feature_index, gabor_feature_index, law_feature_index, alpha_value, peritumoral_flag, contour_flag)