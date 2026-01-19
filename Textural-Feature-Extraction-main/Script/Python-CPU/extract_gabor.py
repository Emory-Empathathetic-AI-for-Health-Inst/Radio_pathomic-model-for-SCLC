import numpy as np
# import cv2
from GaborFilter import gabor_filter
from skimage.color import rgb2gray

def extract_gabor(I, I_mask):
    """
    Extract Gabor filter based features from images

    Args:
        I: Input Image
        I_mask: Input Mask/Label

    Returns:
        FV: A list of feature vectors. Each feature vector corresponds to the Gabor features
        extracted at a pixel location in the I_mask where the value is 1.

        FV_tot: A list of Gabor output images. This is a list of multiple Gabor feature maps,
        each image are processed by a particular Gabor filter.

    """
    r, c = I.shape[:2]  # Because Color Image has three channel (height, width, channels)

    max_pixel_value = np.max(I)  # find the maximum
    min_pixel_value = np.min(I)  # find the minimum


    inputImg = I

    # Check for color images and convert to grayscale images
    if inputImg.ndim > 2:
        gray_input_Img = rgb2gray(inputImg)
    else:
        gray_input_Img = inputImg


    # Define frequency and direction
    f = [0, 2, 4, 8, 16, 32]
    theta = [0, np.pi/8, np.pi/4, 3*np.pi/8, np.pi/2, 5*np.pi/8, 3*np.pi/4, 7*np.pi/8]


    Gabor_output_image = []
    feat = []

    # Each frequency and direction combination is traversed and the output image
    # of the corresponding Gabor filter is computed and stored.
    # The characteristic parameters (frequency and direction) of each combination are also added to the feat list
    for f_index in f:
        for theta_index in theta:
            feat.append([f_index, theta_index])
            G_F, G_I, _, _ = gabor_filter(gray_input_Img, 2, 4, f_index, theta_index)
            Gabor_output_image.append(G_I)

    FV_tot = Gabor_output_image

    FV = []
    r, c = I_mask.shape  # r: row/height, c: column/wdith

    # Traverse the entire mask and select the place where pixel=1 to extract feature
    for i in range(r):
        for j in range(c):
            if I_mask[i, j] == 1:  # extract the feature when pixel = 1
                fv_con = [FV_temp[i, j] for FV_temp in FV_tot]
                FV.append(fv_con)

    FV = np.array(FV)  # Convert list of feature vectors to a numpy array for convenience

    return FV, FV_tot
