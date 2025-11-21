import os
os.environ["KERAS_BACKEND"] = "torch"
import keras
from keras import layers
from keras import Sequential
from keras import optimizers 
import numpy as np
import matplotlib.pyplot as plt
def f(x):
    return np.cos(2*x) + x*np.sin(3*x) + x**0.5 - 2

#On ajoute un bruit selon une loi gaussienne
#de paramètres "mu" et "sigma" :
def gaussnoise(mu, sigma, size):
    return np.random.normal(mu, sigma, size)
import os
os.environ["KERAS_BACKEND"] = "torch"
import keras
# Création du jeu de données
a, b = 0, 5
N = 60
X = np.linspace(a, b, N)
#print(X)
Y = f(X)
Ynoisy=f(X)+gaussnoise(0,0.9,N)
#print(Y)
X_train = X.reshape(-1,1)
Y_train = Ynoisy.reshape(-1,1)
# Modèle : 1 entrée -> 4 couches tanh, p neurones par couche, 1 sortie linéaire
p = 10
modele = Sequential([
layers.Input(shape=(1,)),
layers.Dense(p, activation='tanh'),
layers.Dense(p, activation='tanh'),
layers.Dense(p, activation='tanh'),
layers.Dense(p, activation='tanh'),
layers.Dense(p, activation='tanh'),
layers.Dense(p, activation='tanh'),
layers.Dense(1, activation='linear'), # linear par défaut, mais on explicite
])
# --- Compilation : descente de gradient
modele.compile(optimizer=optimizers.Adam(learning_rate=0.01),loss='mean_squared_error')
# --- Résumé ---
print(modele.summary())
#Entraînement du modèle ; verbose=1 affiche la progression et la loss à chaque epoch
history = modele.fit(X_train, Y_train, epochs=4000, batch_size=len(X_train), verbose=0)
Y_predict = modele.predict(X_train) # calcul de la prédiction
# Tracer du nuage de points des données bruitées color='blue'
plt.plot(X_train, Y_train,"ob")
plt.plot(X_train, Y_predict, color='red')
plt.show()