import os
os.environ["KERAS_BACKEND"] = "torch"
import keras
from keras import layers
from keras import Sequential
import matplotlib.pyplot as plt
import numpy as np

# # Architecture du réseau
# modele = Sequential()
# # Couches de neurones
# modele.add(layers.Input(shape=(1,)))
# modele.add(layers.Dense(2, activation="relu"))
# modele.add(layers.Dense(1, activation="relu"))
# # Pour vérifier l'achitecture du réseau
# modele.summary()

# # Couche 0 (1->2)
# coeff = np.array([[1., -0.5]]) # (1, 2)
# biais = np.array([-1, 1]) # (2,)
# modele.layers[0].set_weights([coeff, biais])


# # Poids de la deuxième couche (2->1)
# coeff2 = np.array([[1], [1]]) # (2, 1)
# biais2 = np.array([0]) # (1,)
# modele.layers[1].set_weights([coeff2, biais2])

# entree = np.array([[3.0]])
# sortie = modele.predict(entree)
# print(sortie)



# liste_x = np.linspace(-2, 3, num=100)
# entree = np.array([[x] for x in liste_x])
# sortie = modele.predict(entree)
# liste_y = np.array([y[0] for y in sortie])
# plt.plot(liste_x,liste_y)
# plt.show()


#Partie 1.6

Test = Sequential()
Test.add(layers.Input(shape=(2,)))
Test.add(layers.Dense(3, activation="sigmoid"))
Test.add(layers.Dense(1, activation="sigmoid"))

Test.summary()

coeff = np.array([[1,3,-5], [2,-4,-6]]) # (1, 2)
biais = np.array([-1, 0, 1]) # (2,)
Test.layers[0].set_weights([coeff, biais])

coeff2 = np.array([[1], [1], [1]]) # (2, 1)
biais2 = np.array([-3]) # (1,)
Test.layers[1].set_weights([coeff2, biais2])


entree = np.array([[7.,-5.]])
sortie = Test.predict(entree)
print(sortie)


liste_x = np.linspace(-2, 3, num=100)
entree = np.array([[x,x] for x in liste_x])
sortie = Test.predict(entree)
liste_y = np.array([y[0] for y in sortie])
plt.plot(liste_x,liste_y)
plt.show()