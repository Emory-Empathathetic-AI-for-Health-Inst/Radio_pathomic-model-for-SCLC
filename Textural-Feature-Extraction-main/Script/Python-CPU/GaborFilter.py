import numpy as np
from scipy.signal import convolve2d



def gabor_filter(I, Sx, Sy, Scale, Orientation):
    """
    Gabor Filter

    Args:
        I: Input image (original image)
        (Sx,Sy: control the size of the Gaussian envelope part of the Gabor function)
        Sx: Variances along the x-axis
        Sy: Variances along the y-axis
        Scale:scale parameter, control the filter's sensitivity to details
        Orientation: orientation parameter, defines the orientation of the Gabor filter

    Returns:
        G: Gabor Filter, a two-dimensional filter matrix
        gabout: Filtered Image Magnitude, the magnitude of the result
        gaboutReal: Real Part of Filtered Image, convolve the image with the cosine part of the Gabor filter
        gaboutImg: Imaginary Part of Filtered Image, convolve the image with the sine part of the Gabor filter
    """

    # Use float64 to ensure calculation accuracy
    if I.dtype != np.float64:
        I = I.astype(np.float64)

    m_dSigma = 2 * np.pi
    m_dfrequency = np.sqrt(2)
    m_dKmax = np.pi / 2

    HeightBottom = -int(Sy / 2)
    HeightTop = int(Sy / 2)

    WidthBottom = -int(Sy / 2)
    WidthTop = int(Sy / 2)

    postConstant = np.exp(-m_dSigma * m_dSigma / 2)

    preConstant_Kuv = (m_dKmax / m_dfrequency ** Scale) ** 2
    Phi = Orientation
    Kv = m_dKmax / (m_dfrequency ** Scale)

    m_dSigmaY = 2 * np.pi
    m_dSigmaX = 2 * np.pi

    G = np.zeros((WidthTop - WidthBottom + 1, HeightTop - HeightBottom + 1), dtype=np.complex_)  # np.complex128

    for x in range(WidthBottom, WidthTop + 1):
        for y in range(HeightBottom, HeightTop + 1):
            exppart = np.exp(-1 * preConstant_Kuv / 2 * (
                        x ** 2 / (m_dSigmaX ** 2) + y ** 2 / (m_dSigmaY ** 2))) * preConstant_Kuv / (
                                  m_dSigmaX * m_dSigmaY)
            G[x - WidthBottom, y - HeightBottom] = exppart * (
                        np.cos(Kv * (np.cos(Phi) * x + np.sin(Phi) * y)) - postConstant) + 1j * exppart * (
                                                       np.sin(Kv * (np.cos(Phi) * x + np.sin(Phi) * y)))

            # equivalent expression
            # G[WidthTop + x, HeightTop + y] = exppart * (
            #             np.cos(Kv * (np.cos(Phi) * x + np.sin(Phi) * y)) - postConstant) + 1j * exppart * np.sin(
            #     Kv * (np.cos(Phi) * x + np.sin(Phi) * y))


    Imgabout = convolve2d(I, np.imag(G), mode='same')
    Regabout = convolve2d(I, np.real(G), mode='same')

    gabout = np.sqrt(Imgabout ** 2 + Regabout ** 2)
    gaboutImg = Imgabout
    gaboutReal = Regabout

    return G, gabout, gaboutReal, gaboutImg

