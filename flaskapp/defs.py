import pandas as pd
import numpy as np
import os
import sys
from PIL import Image
import scipy.ndimage.interpolation as interp

from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt

def resize_image(path, height, width):
    image = Image.open(path)
    image_array = np.array(image)

    image_array = interp.zoom(image_array, (height, width, 1))

    height, width, _ = image_array.shape

    image = Image.fromarray(image_array.astype('uint8'), 'RGB')
    image.save(path[:-14] + '_resized.png')

    return height, width

def GRAPHS(path, root, name):
    from skimage import io
    import matplotlib.pyplot as plt
    image = io.imread(path)

    _ = plt.hist(image.ravel(), bins = 64, color = 'Orange', )
    _ = plt.hist(image[:, :, 0].ravel(), bins = 64, color = 'Red', alpha = 0.7)
    _ = plt.hist(image[:, :, 1].ravel(), bins = 64, color = 'Green', alpha = 0.7)
    _ = plt.hist(image[:, :, 2].ravel(), bins = 64, color = 'Blue', alpha = 0.7)
    _ = plt.xlabel('Intensity Value')
    _ = plt.ylabel('Count')
    _ = plt.legend(['Total', 'Red Channel', 'Green Channel', 'Blue Channel'])
    _ = plt.title(name)

    plt.savefig(root)
