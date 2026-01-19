import numpy as np
from scipy.ndimage import binary_dilation
from skimage.morphology import disk

def peritumoral(origImage, tumorMask):
    """
    To extract the peritumoral region of a nodule

    Parameters:
        origImage (numpy.ndarray): Original image
        tumorMask (numpy.ndarray): Tumor mask

    Returns:
        I (numpy.ndarray): Peritumoral region image
        B2 (numpy.ndarray): Dilated tumor mask - original tumor mask
    """

    # Looking at 7 pixels around the tumor
    # Create a disk-shaped structuring element with radius 7
    se = disk(7)

    B = binary_dilation(tumorMask, se)
    B2 = B ^ tumorMask  # Equivalent to B2 = B - tumorMask in MATLAB

    r, c = origImage.shape

    I = np.zeros((r, c))
    for i in range(r):
        for j in range(c):
            if B2[i, j] == 1:
                I[i, j] = origImage[i, j]
            else:
                I[i, j] = 0

    return I, B2