import numpy as np
from scipy.ndimage import filters
from skimage.color import rgb2gray
import skimage
from lawskerns import laws_kernels
from scipy.signal import convolve2d
from scipy.signal import correlate2d

def lawsfilter(I):
    """
    Apply 2D Law's filters to an image.

    Args:
        I: 2D numpy array representing a grayscale image.

    Returns:
        laws_responses: A numpy array of shape (N, M, 25) containing the 25 filter responses from the Law's kernels.
    """
    # Ensure I is a 2D grayscale image
    if I.ndim != 2:
        raise ValueError("2D grayscale images only.")

    # Generate Law's kernels
    KK = laws_kernels()
    nkerns = KK.shape[2]


    nrows, ncols = I.shape[:2]
    laws_responses = np.zeros((nrows, ncols, nkerns))

    # Apply each of the Law's kernels to the image
    for i in range(nkerns):
        # laws_responses[:, :, i] = filters.convolve(I, KK[:, :, i])
        # laws_responses[:, :, i] = convolve2d(I, KK[:, :, i], mode='same')
        # Pay attention to the Methods for handling boundary cases
        laws_responses[:, :, i] = correlate2d(I, KK[:, :, i], mode='same')

    return laws_responses