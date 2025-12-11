import os
import sys
sys.path.append(os.path.expanduser("~/py-packages/"))
import numpy as np
from skimage import data
from skimage.measure import block_reduce
import matplotlib.pyplot as plt
import numpy as np
from skimage import data
import matplotlib as plt
from scipy import signal
from matplotlib.pyplot import imshow, get_cmap
import matplotlib.pyplot as plt
# Charge une image (par exemple, un cheval de la bibliothèque de données skimage)
image = data.checkerboard()

# Affiche le nombre de pixels de l'image originale
print(f"Nombre de pixels de l'image originale : {image.size}")


def displayTwoBaWImages(img1, img2):
    _, axes = plt.subplots(ncols=2)
    axes[0].imshow(img1, cmap=plt.get_cmap('gray'))
    axes[1].imshow(img2, cmap=plt.get_cmap('gray'))
kernel = np.array([[1,0,-1],[1,0,-1],[1,0,-1]])
print(kernel)



# Affiche l'image d'origine
plt.imshow(image, cmap=plt.get_cmap('gray'))
plt.title('Image originale')
plt.show()
# Applique le max pooling avec différentes tailles de fenêtre
pooling_sizes = [2, 3, 4,10]
for size in pooling_sizes:
    image_normalized = (image - np.min(image)) / (np.max(image) - np.min(image))
    # Utilise la fonction block_reduce de skimage pour effectuer le max pooling
    pooled_image = block_reduce(image, (size, size), np.max)
    # Affiche le nombre de pixels de l'image après max pooling
    print(f"Nombre de pixels après Max Pooling {size}x{size} : {pooled_image.size}")
    # Affiche l'image résultante avec le titre correspondant
    imgconvol = signal.convolve2d(pooled_image,
                    kernel,
                    mode='same',
                    boundary='fill',
                    fillvalue=0)
    displayTwoBaWImages(pooled_image, image)
    #plt.imshow(pooled_image, cmap=plt.get_cmap('gray'))
    plt.title(f'Max Pooling {size}x{size}')
    plt.show()

