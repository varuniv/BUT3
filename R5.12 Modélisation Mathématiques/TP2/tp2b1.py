import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import get_cmap
os.environ["KERAS_BACKEND"] = "torch"
from keras import layers, Sequential
from keras.datasets import mnist


(X_train_data,Y_train_data),(X_test_data,Y_test_data) = mnist.load_data()
i = 5
plt.imshow(X_train_data[i], cmap='Greys')

plt.show()
