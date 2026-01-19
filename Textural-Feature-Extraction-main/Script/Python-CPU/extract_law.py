from lawsfilter import lawsfilter
import numpy as np

def extract_law(I, I_mask):
    """
    Extracts Law's features from an image, given a mask.

    Args:
        I: 2D numpy array representing a grayscale image.
        I_mask: 2D numpy array of the same shape as I, where each pixel is either 1 (to include in FV) or 0 (to exclude).

    Returns:
        FV: Feature vectors for pixels where I_mask is 1.
        law_res: The responses from applying Law's filters to the image.
    """
    law_res = lawsfilter(I)
    r, c = I.shape
    FV = []

    # Iterate over each pixel in the image
    for i in range(r):
        for j in range(c):
            fv_con = []
            # If the mask at this pixel is 1, collect the feature vector
            if I_mask[i, j] == 1:
                for k in range(25):  # Assuming 25 filter responses from lawsfilter
                    fv = law_res[i, j, k] # the response value obtained after processing the pixel at the ith row and jth column of the image with the kth Law's filter.
                    fv_con.append(fv)
                FV.append(fv_con)

    FV = np.array(FV)  # Convert list of feature vectors to a numpy array for convenience

    return FV, law_res
