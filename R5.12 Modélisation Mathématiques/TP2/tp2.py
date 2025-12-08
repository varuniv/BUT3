import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import get_cmap
# Création d’une image 2x2
image = np.array([
    [0.9, 0.2],
    [0.1, 0.8]])
# Affichage
cmp = get_cmap('gray')
plt.imshow(image, cmap=cmp, vmin=0, vmax=1)
plt.show()
# Pour aplatir l’image on utilise la méthode flatten
image_flattened=image.flatten()
print(image_flattened)

x = np.array([1.2,0.5])

p1 = 1
p0 = 0

def softmax(x):
     return np.exp(x) / np.sum(np.exp(x))

print(softmax(x))

print(softmax(image_flattened))

def cross_entropy(p, q):
    return -np.sum(p * np.log(q))

ecc = -p1 * np.log(softmax(x)[0]) - p0 * np.log(softmax(x)[1])
ecc2 = cross_entropy([p1, p0], softmax(x))
print(ecc)
print(ecc2)



image1 = np.array([[0, 1],[1 ,0]])
image2 = np.array([[0, 1],[0, 1]])
p1 = [1,0] 
p2 = [0,1]    
image1_flat = image1.flatten()
image2_flat = image2.flatten() 
x1 = [1.5,0.2]
x2 = [0.3,1.1]

q1 = softmax(x1)
q2 = softmax(x2)
ce1 = cross_entropy(p1, q1)
ce2 = cross_entropy(p2, q2)
print(ce1)
print(ce2)



