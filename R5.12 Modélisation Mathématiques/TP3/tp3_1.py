import os
import sys
sys.path.append(os.path.expanduser("~/py-packages/"))
import numpy as np
from skimage import data
from skimage.measure import block_reduce
import matplotlib.pyplot as plt
# Charge une image (par exemple, un cheval de la bibliothèque de données skimage)
image = data.horse()
# Affiche le nombre de pixels de l'image originale
print(f"Nombre de pixels de l'image originale : {image.size}")
# Affiche l'image d'origine
plt.imshow(image, cmap=plt.get_cmap('gray'))
plt.title('Image originale')
plt.show()
# Applique le max pooling avec différentes tailles de fenêtre
pooling_sizes = [2, 3, 4,10]
for size in pooling_sizes:
    # Utilise la fonction block_reduce de skimage pour effectuer le max pooling
    pooled_image = block_reduce(image, (size, size), np.max)
    # Affiche le nombre de pixels de l'image après max pooling
    print(f"Nombre de pixels après Max Pooling {size}x{size} : {pooled_image.size}")
    # Affiche l'image résultante avec le titre correspondant
    plt.imshow(pooled_image, cmap=plt.get_cmap('gray'))
    plt.title(f'Max Pooling {size}x{size}')
    plt.show()