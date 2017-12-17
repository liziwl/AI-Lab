import os
import numpy as np
import pickle
import matplotlib
import time
import math

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Definition of functions and parameters
# for example
EPOCH = 100

# Read all data from .pkl
(train_images, train_labels, test_images, test_labels) = pickle.load(open('./mnist_data/data.pkl', 'rb'),
                                                                     encoding='latin1')

### 1. Data preprocessing: normalize all pixels to [0,1) by dividing 256
train_images = train_images / 256
test_images = test_images / 256

### 2. Weight initialization: Xavier
input_layer_size = 784
layer1_size = 300
layer2_size = 100
output_size = 10

w1 = np.random.uniform(-math.sqrt(6) / math.sqrt(input_layer_size + layer1_size),
                       math.sqrt(6) / math.sqrt(input_layer_size + layer1_size),
                       (input_layer_size, layer1_size))
w2 = np.random.uniform(-math.sqrt(6) / math.sqrt(layer1_size + layer2_size),
                       math.sqrt(6) / math.sqrt(layer1_size + layer1_size),
                       (layer1_size, layer2_size))
w3 = np.random.uniform(-math.sqrt(6) / math.sqrt(layer2_size + output_size),
                       math.sqrt(6) / math.sqrt(layer2_size + output_size),
                       (layer2_size, output_size))

### 3. training of neural network
# loss = np.zeros((EPOCH))
# accuracy = np.zeros((EPOCH))
#
# for epoch in range(0, EPOCH):
#     print(epoch)


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
