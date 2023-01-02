# Billboard hack script file.
from msilib.schema import Billboard
import numpy as np
from matplotlib.path import Path
from matplotlib import pyplot as plt
from imageio import imread, imwrite

from dlt_homography import dlt_homography
from bilinear_interp import bilinear_interp
from histogram_eq import histogram_eq


def billboard_hack():
    """
    Hack and replace the billboard!

    Parameters:
    ----------- 

    Returns:
    --------
    Ihack  - Hacked RGB intensity image, 8-bit np.array (i.e., uint8).
    """
    # Bounding box in Y & D Square image - use if you find useful.
    bbox = np.array([[404, 490, 404, 490], [38,  38, 354, 354]])

    # Point correspondences.
    Iyd_pts = np.array([[416, 485, 488, 410], [40,  61, 353, 349]])
    Ist_pts = np.array([[2, 218, 218, 2], [2, 2, 409, 409]])

    Iyd = imread('../images/yonge_dundas_square.jpg')
    Ist = imread('../images/uoft_soldiers_tower_light.png')

    Ihack = np.asarray(Iyd)
    Ist = np.asarray(Ist)

    #--- FILL ME IN ---

    # Let's do the histogram equalization first.
    enhanced_Ist = histogram_eq(Ist)
    # Compute the perspective homography we need...
    H, A = dlt_homography(Iyd_pts, Ist_pts)
    # Main 'for' loop to do the warp and insertion - 
    # this could be vectorized to be faster if needed!

    # for loop for the bounding box of the Billboard
    # Use path to ensure that pixels are etnirely within region defined by homography
    billboard = Path(Iyd_pts.T)
    # iterate through x
    for x in range(np.min(bbox[0]), np.max(bbox[0])+1):
    # iterate through y
        for y in range (np.min(bbox[1]), np.max(bbox[1])+1):
    #   if billboard Path has points x,y then we will go ahead and transform the point from the soldier image
            if billboard.contains_points(np.array([[x,y]])):
    #       set point 
                point = np.array([x,y,1])
    #       transform point via homolgraphy
                new_point = np.matmul(H,point)
    #       normalize to rid c coefficient
                new_point = new_point/new_point[2]
    #       then get value based on bilinear interp
                brightness = bilinear_interp(enhanced_Ist, new_point[:-1].reshape((2,1)))
    #       Add this point to the image 
                Ihack[point[1],point[0]] = brightness
            

    #------------------

    # Visualize the result, if desired...
    # plt.imshow(Ihack)
    # plt.show()
    # imwrite(Ihack, 'billboard_hacked.png')

    return Ihack
