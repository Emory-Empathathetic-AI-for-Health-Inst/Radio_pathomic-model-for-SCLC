import numpy as np


def rescale_range(I, N1, N2, rangedata=None):
    """
    Rescale the input array to a specified range [N1, N2].

    Parameters:
    - I: Input array.
    - N1: Lower bound of the target range.
    - N2: Upper bound of the target range.
    - rangedata: Optional, the range of data to consider for scaling. If not provided, the range of I is used.

    Returns:
    - Iout: Rescaled array.
    - N2high: The maximum value in the rescaled array.
    """
    # Ensure input is float for division to work correctly
    I = I.astype(float)

    # Determine the range of the data
    if rangedata is not None:
        datarange = np.max(rangedata) - np.min(rangedata)
    else:
        datarange = np.max(I) - np.min(I)

    # Avoid division by zero or near-zero values
    if datarange > np.finfo(float).eps:
        wantedrange = N2 - N1
        Iout = N1 + (I - np.min(I)) / (datarange / wantedrange)
    else:
        Iout = I

    # Optionally return the maximum value of the output array
    N2high = np.max(Iout)

    return Iout, N2high

# Example usage:
# I = np.random.rand(100, 100)  # Example input array
# N1, N2 = 0, 255  # Desired output range
# Iout, N2high = rescale_range(I, N1, N2)
