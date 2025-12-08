import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import get_cmap
os.environ["KERAS_BACKEND"] = "torch"
from keras import layers, Sequential
from keras.datasets import mnist
import numpy as np
import os
os.environ["KERAS_BACKEND"] = "torch"
import keras
import os
os.environ["KERAS_BACKEND"] = "torch"
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dense
### Partie A - Les données
from keras.datasets import mnist
from keras.utils import to_categorical
# Téléchargement des données
(X_train_data,Y_train_data),(X_test_data,Y_test_data) = mnist.load_data()
N = X_train_data.shape[0] # N = 60 000 données
# Données d'apprentissage X
X_train = np.reshape(X_train_data,(N,784)) # vecteur image
X_train = X_train/255 # normalisation
# Données d'apprentissage Y vers une liste de taille 10
Y_train = to_categorical(Y_train_data, num_classes=10)
# Données de test
X_test = np.reshape(X_test_data,(X_test_data.shape[0],784))
X_test = X_test/255
Y_test = to_categorical(Y_test_data, num_classes=10)
### Partie B - Le réseau de neurones
p = 10
modele = Sequential()
# Première couche : p neurones (entrée de dimension 784 = 28x28)
modele.add(Dense(p, input_dim=784, activation='sigmoid'))
# Deuxième couche : p neurones
modele.add(Dense(p, activation='sigmoid'))
# Troiseme couche : p neurones
modele.add(Dense(p, activation='sigmoid'))
# Couche de sortie : 1O neurones (un par chiffre)
modele.add(Dense(10, activation='softmax'))
# La fonction d'activation 'softmax' sera décrite dans le paragraphe suivant.
# Choix de la méthode de descente de gradient
modele.compile(loss='categorical_crossentropy',
optimizer='sgd',
metrics=['accuracy'])
# La fonction d'erreur 'categorical_crossentropy' est décrite dans le paragraphe suivant.
# L'optimisation 'sgd' est décrite dans le paragraphe suivant.
# 'accuracy' est décrite dans le paragraphe suivant.
print(modele.summary())
### Partie C - Calcul des poids par descente de gradient
modele.fit(X_train, Y_train, batch_size=32, epochs=40)
### Partie D - Résultats
resultat = modele.evaluate(X_test, Y_test, verbose=0)
print('Valeur de l''erreur sur les données de test (loss):', resultat[0])
print('Précision sur les données de test (accuracy):', resultat[1])

# Prédiction sur les données de test
Y_predict = modele.predict(X_test)
# Un exemple
i = 8 # numéro de l'image
chiffre_predit = np.argmax(Y_predict[i]) # prédiction par le réseau
print("Sortie réseau", Y_predict[i])
print("Chiffre attendu :", Y_test_data[i])
print("Chiffre prédit :", chiffre_predit)
plt.imshow(X_test_data[i], cmap='Greys')
plt.show()

predictions = modele.predict(X_test)
predicted_labels = np.argmax(predictions, axis=1)
true_labels = np.argmax(Y_test, axis=1)

misclassified_indices = np.where(predicted_labels != true_labels)[0]
for idx in misclassified_indices[:5]:
    plt.imshow(X_test[idx].reshape(28, 28), cmap='gray')
    plt.title(f'Predicted: {predicted_labels[idx]}, True: {true_labels[idx]}')
    plt.show()