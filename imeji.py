import numpy as np
import PIL

def extract_planes(img: PIL.Image.Image):
    """Return a n x m x 3 array, each n x m array is a plane R,G,B"""
    planes = np.array(img)
    R, G, B = planes[..., 0], planes[..., 1], planes[..., 2]
    return R, G, B

def orthogonalize(matrix: np.array) -> np.array:
    """Orthogonalizes a matrix into Q and R and return the orthogonal matrix Q"""
    q, r = np.linalg.qr(matrix)
    return q