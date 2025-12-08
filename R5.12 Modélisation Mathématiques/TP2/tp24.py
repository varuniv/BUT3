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
#  Partie A. Données
from keras.datasets import cifar10
(X_train_data,Y_train_data),(X_test_data,Y_test_data)=cifar10.load_data()
num_classes = 10
labels = ['airplane','automobile','bird','cat','deer',
'dog','frog','horse','ship','truck']
Y_train = keras.utils.to_categorical(Y_train_data, num_classes)
X_train = X_train_data.reshape(50000,32*32*3)
X_train = X_train.astype('float32')
X_train = X_train/255
# Partie B. Réseau
modele = Sequential()
p = 30
modele.add(Dense(p, input_dim=32*32*3, activation='sigmoid'))
modele.add(Dense(p, activation='sigmoid'))
modele.add(Dense(p, activation='sigmoid'))
modele.add(Dense(p, activation='sigmoid'))
modele.add(Dense(10, activation='softmax'))
modele.compile(loss='categorical_crossentropy',
optimizer='adam', metrics=['accuracy'])
modele.summary()
# Partie C. Apprentissage
modele.fit(X_train, Y_train, epochs=10, batch_size=32)
plt.figure(figsize=(10,10))
# Partie D. Résultats
for i in range(9):
    plt.subplot(3,3,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(X_test_data[i], cmap=plt.cm.binary)
    X_test = X_test_data.reshape(10000,32*32*3)
    X_test = X_test.astype('float32')
    X_test = X_test/255
    predictions = modele.predict(np.array([X_test[i]]))
    predicted_label = np.argmax(predictions[0])
    true_label = Y_test_data[i][0]
    color = 'blue' if predicted_label == true_label else 'red'
    plt.xlabel("Predicted: {} ({:2.0f}%)\nTrue: {}".format(
        labels[predicted_label],
        100*np.max(predictions),
        labels[true_label]),
        color=color)
plt.show()