import os
import numpy as np
import pickle
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Definition of functions and parameters
# for example
EPOCH = 100

# Read all data from .pkl
(train_images, train_labels, test_images, test_labels) = pickle.load(open('./mnist_data/data.pkl', 'rb'), encoding='latin1')

### 1. Data preprocessing: normalize all pixels to [0,1) by dividing 256


### 2. Weight initialization: Xavier



### 3. training of neural network
loss = np.zeros((EPOCH))
accuracy = np.zeros((EPOCH))

for epoch in range(0, EPOCH):
    print(epoch)


    # Forward propagation


    # Back propagation

    # Gradient update


    # Testing for accuracy


### 4. Plot
# for example
# plt.figure(figsize=(12,5))
# ax1 = plt.subplot(111)
# ax1.plot(......)
# plt.xlabel(......)
# plt.ylabel(......)
# plt.grid()
# plt.tight_layout()
# plt.savefig('figure.pdf', dbi=300)
