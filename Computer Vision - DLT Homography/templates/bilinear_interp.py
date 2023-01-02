import numpy as np
from numpy.linalg import inv

def bilinear_interp(I, pt):
    """
    Performs bilinear interpolation for a given image point.

    Given the (x, y) location of a point in an input image, use the surrounding
    four pixels to conmpute the bilinearly-interpolated output pixel intensity.

    Note that images are (usually) integer-valued functions (in 2D), therefore
    the intensity value you return must be an integer (use round()).

    This function is for a *single* image band only - for RGB images, you will 
    need to call the function once for each colour channel.

    Parameters:
    -----------
    I   - Single-band (greyscale) intensity image, 8-bit np.array (i.e., uint8).
    pt  - 2x1 np.array of point in input image (x, y), with subpixel precision.

    Returns:
    --------
    b  - Interpolated brightness or intensity value (whole number >= 0).
    """
    #--- FILL ME IN ---

    if pt.shape != (2, 1):
        raise ValueError('Point size is incorrect.')


    # Get points that surround the middle point
    x1 = int(np.floor(pt[0]))
    y1 = int(np.floor(pt[1]))
    x2 = x1 + 1
    y2 = y1 + 1

    # Bilinear Interpolation Algorithm as per Wikipedia multilinear polynomial https://en.wikipedia.org/wiki/Bilinear_interpolation
    # Get Intensities f(Q11)
    f11 = I[y1][x1]
    f12 = I[y2][x1]
    f21 = I[y1][x2]
    f22 = I[y2][x2]
    f = np.array([f11, f12, f21, f22])

    # Make the coefficient matrix C
    C = np.array([[1, x1, y1, x1*y1],
                [1, x1, y2, x1*y2],
                [1, x2, y1, x2*y1],
                [1, x2, y2, x2*y2]])

    # Compute weight matrix
    A = np.matmul(inv(C), f)
    # Interpolate Brigthness at position - f(x,y) ~= a00 + a10x + a01y + a11xy
    b = A[0] + A[1] * pt[0] + A[2] * pt[1] + A[3]*pt[0]*pt[1]
    b = b.item()
    b = int(round(b))
    #------------------
    return b