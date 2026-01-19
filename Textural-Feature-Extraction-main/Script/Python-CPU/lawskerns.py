import numpy as np

def laws_kernels():
    """
    Generate the 25 Law's 2D kernels from the 5 1D kernel bases.

    Returns:
    - KK: A 5-by-5-by-25 numpy array containing the Law's kernels.
    """
    # Define the 1D base kernels
    L = np.array([1, 4, 6, 4, 1])    # Level
    E = np.array([-1, -2, 0, 2, 1])  # Edge
    S = np.array([-1, 0, 2, 0, -1])  # Spot
    W = np.array([-1, 2, 0, -2, 1])  # Wave
    R = np.array([1, -4, 6, -4, 1])  # Ripple

    # List of base kernels
    base_kernels = [L, E, S, W, R]

    # Initialize the array to hold the 25 2D kernels
    KK = np.zeros((5, 5, 25))

    # Compute the outer product of each pair of base kernels
    for i, kernel_i in enumerate(base_kernels):
        for j, kernel_j in enumerate(base_kernels):
            # The outer product of two vectors results in a matrix
            KK[:, :, j + i * 5] = np.outer(kernel_i, kernel_j)

    return KK

