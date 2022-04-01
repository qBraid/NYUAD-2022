from itertools import count
from unittest import result
from utils import (callImage, imageResize, grover)

def classify(path):
    result=False
    data_img = callImage(path)
    image = imageResize(data_img,16) # Can be printed with plt.imshow(image)
    image.flatten()
    count=grover(5, image)
    #Processing 

    #Save data to file

    return result