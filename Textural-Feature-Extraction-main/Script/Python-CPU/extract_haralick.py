import numpy as np
import mahotas
from skimage import exposure

from rescale_range import rescale_range


def extract_haralick(I, I_mask):

    haralickfun = mahotas.features.haralick
    nharalicks = 13  # the number of Haralick feature
    bg = -1; # Background
    ws = 5  # Window Size
    hardist = 1  # Distance in a window
    harN = 64  # Maximum number of quantitative levels

    # vol = I.astype(float)
    vol = np.double(I)
    volN, _ = rescale_range(vol, 0, harN - 1)  # Quantifying an image
    volN = volN.astype(int)  # Make sure it's integer

    # Initialize the feature array
    r, c = I.shape
    volfeats = np.zeros((r, c, nharalicks))  # Or add "dtype=np.double"
    # volfeats = np.zeros((r, c, nharalicks * 4))  # 4 directions

    # Calculate Haralick feature
    for i in range(r):
        for j in range(c):
            if I_mask[i, j] == 1:  # Calculated only for points within the mask
                # Extracting sub-windows and calculating Haralick features
                window = volN[max(i - ws // 2, 0):min(i + ws // 2 + 1, r), max(j - ws // 2, 0):min(j + ws // 2 + 1, c)]
                if window.size == 0:
                    continue  # If the windows size is zero, then skip

                # Notice: when extracting peri tumoral feature, causing the value error sometimes
                try:
                    # Try to calculate the Haralick features
                    features = haralickfun(window, distance=hardist, ignore_zeros=(bg == -1))
                    # Averaging the computed results as mahotas return features in each direction
                    volfeats[i, j, :] = features.mean(axis=0)
                except ValueError:
                    # If a ValueError is raised, assign a default feature vector
                    volfeats[i, j, :] = np.zeros(nharalicks)

                # # Calculate the haralick feature
                # features = haralickfun(window, distance=hardist, ignore_zeros=(bg == -1))
                #
                # # Averaging the computed results as mahotas return features in each direction
                # volfeats[i, j, :] = features.mean(axis=0)
                # # volfeats[i, j, :] = features.flatten()


    # Constructing feature vectors
    FV = []
    for i in range(r):
        for j in range(c):
            if I_mask[i, j] == 1:
                fv_con = volfeats[i, j, :]
                FV.append(fv_con)

    FV = np.array(FV)  # Convert the feature vector into Numpy array

    return FV, volfeats

