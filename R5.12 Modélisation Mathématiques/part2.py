import os
os.environ["KERAS_BACKEND"] = "torch"
import keras
from keras import layers
from keras import Sequential
import matplotlib.pyplot as plt
import numpy as np
# Partie A. Données
# Fonction à approcher
def f(x):
    return np.cos(2*x) + x*np.sin(3*x) + x**0.5 - 2
a, b = 0, 5 # intervalle [a,b]
N = 100 # volume de données
X = np.linspace(a, b, N) # abscisses
Y = f(X) # ordonnées
# transforme X en une colonne, comportant le bon nombre de ligne (i.e. "-1"), idem pour Y
X_train = X.reshape(-1,1)
Y_train = Y.reshape(-1,1)
# Partie B. Réseau
# Modèle : 1 entrée -> 4 couches tanh, p neurones par couche, 1 sortie linéaire
p = 10
modele = Sequential([
layers.Input(shape=(1,)),
layers.Dense(p, activation='tanh'),
layers.Dense(p, activation='tanh'),
layers.Dense(p, activation='tanh'),
layers.Dense(p, activation='tanh'),
layers.Dense(1, activation='linear'), # linear par défaut, mais on explicite
])
# --- Compilation : descente de gradient
modele.compile(loss='mean_squared_error')
# --- Résumé ---
print(modele.summary())
#Entraînement du modèle ; verbose=1 affiche la progression et la loss à chaque epoch
history = modele.fit(X_train, Y_train, epochs=4000, batch_size=len(X_train), verbose=0)
# Attention ici comme batch_size=len(X_train) c'est une descente de gradient classique
# (non stochastique)
# Affichage de la fonction et de son approximation :
# A exécuter sur une cellule indépendante
Y_predict = modele.predict(X_train) # calcul de la prédiction
plt.plot(X_train, Y_train, color='blue')
plt.plot(X_train, Y_predict, color='red')
plt.show()
# Affichage de l'erreur au fil des époques
plt.plot(history.history['loss'])
plt.show()