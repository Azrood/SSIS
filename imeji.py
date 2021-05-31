import numpy
import PIL

def extract_planes(img: PIL.Image.Image):
    planes = numpy.array(img)
    return *planes

def orthogonalize():
    numpy.qr
    # TODO : gram-schmidt orthogonalisation