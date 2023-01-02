import numpy as np

def histogram_eq(I):
    """
    Histogram equalization for greyscale image.

    Perform histogram equalization on the 8-bit greyscale intensity image I
    to produce a contrast-enhanced image J. Full details of the algorithm are
    provided in the Szeliski text.

    Parameters:
    -----------
    I  - Single-band (greyscale) intensity image, 8-bit np.array (i.e., uint8).

    Returns:
    --------
    J  - Contrast-enhanced greyscale intensity image, 8-bit np.array (i.e., uint8).
    """
    #--- FILL ME IN ---

    # Verify I is grayscale.
    if I.dtype != np.uint8:
        raise ValueError('Incorrect image format!')

    

    # Look through the image and first create a histogram with current intensities
    image = I.flatten()
    print(np.shape(I))
    print(np.size(I))

    # 8 bit images = 256 'buckets' and intensities range from 0 to 255
    num_bins = 256 
    num_range = (0,255)
    hist, bin_edges = np.histogram(image, bins=num_bins, range=num_range)
    pdf = hist/np.sum(hist)
    cdf = np.cumsum(pdf)
    c = np.round(255*cdf).astype('uint8')

    # map f(i) = c(i)
    J = np.empty(image.shape)
    for i in range(0,image.shape[0]):
        J[i] = c[image[i]]
    J = J.reshape(I.shape)
    #------------------

    return J