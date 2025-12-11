import numpy as np
from skimage import data
import matplotlib as plt
from scipy import signal
from matplotlib.pyplot import imshow, get_cmap
import matplotlib.pyplot as plt
#La fonction suivante permet d’afficher des images côte à côte (dans le but de voir apparaître les transformations dues à des opérations de convolution).
def displayTwoBaWImages(img1, img2):
    _, axes = plt.subplots(ncols=2)
    axes[0].imshow(img1, cmap=plt.get_cmap('gray'))
    axes[1].imshow(img2, cmap=plt.get_cmap('gray'))


# Nous créons maintenant une image extrêmement simple et nous l’affichons :
image = np.array([[0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0],
                  [0,0,0.5,0.5,0.5,0,0,0],
                  [0,0,0.5,0.5,0.5,0,0,0],
                  [0,0,0.5,0.5,0.5,0,0,0],
                  [0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0],
])
cmp = get_cmap('gray')

kernel = np.ones((3,3), np.float32)/2
print(kernel)
imgconvol = signal.convolve2d(image,
                    kernel,
                    mode='same',
                    boundary='fill',
                    fillvalue=0)
displayTwoBaWImages(image, imgconvol)
plt.show()

