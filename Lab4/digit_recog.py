# encoding: utf-8
import os
import numpy as np
import pickle
import matplotlib
import time
import math

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Definition of functions and parameters
EPOCH = 100
BATCHSIZE = 100
ITERATION = 100
lambd = 0.0005


def soft_max(x):
    """Compute softmax values for each sets of scores in x."""
    # print(x[0])
    return np.exp(x) / np.sum(np.exp(x), axis=0)


def add_w_b(w, b):
    # print("wb",w.shape,b.shape)
    out = np.zeros_like(w)
    for i in range(len(w)):
        out[i] = w[i] + b
    return out


def forward(x, w1, w2, w3, b1, b2, b3):
    a1 = add_w_b(np.dot(x, w1), b1)  # Layer 1 input 100,300
    # print(a1)
    z1 = np.maximum(0, a1)  # Rectified Linear Unit
    # print(z1)
    a2 = add_w_b(np.dot(z1, w2), b2)  # Layer 2 input 100,100
    # print(a2)
    z2 = np.maximum(0, a2)  # Rectified Linear Unit
    # print(z2)
    a3 = add_w_b(np.dot(z2, w3), b3)  # Layer 3 input 100,10

    y = soft_max(a3.T)
    return a1, z1, a2, z2, a3, y.T


def back(x, y, t, w2, w3):
    delta3 = y - t
    dw3 = np.dot(delta3.T, z2)
    db3 = np.mean(delta3.T, axis=1)
    # print(dw3.shape, db3.shape)

    df2 = np.copy(a2)
    df2 = np.where(df2 > 0, df2, 0)  # 小于等于0，设为0
    df2 = np.where(df2 <= 0, df2, 1)  # 大于0，设为1
    delta2 = np.dot(delta3, w3.T) * df2
    dw2 = np.dot(delta2.T, z1)
    db2 = np.mean(delta2.T, axis=1)
    # print(dw2.shape, db2.shape)

    df1 = np.copy(a1)
    df1 = np.where(df1 > 0, df1, 0)  # 小于等于0，设为0
    df1 = np.where(df1 <= 0, df1, 1)  # 大于0，设为1
    delta1 = np.dot(delta2, w2.T) * df1
    dw1 = np.dot(delta1.T, x)
    db1 = np.mean(delta1.T, axis=1)
    # print(dw1.shape, db1.shape)

    return dw3, db3, dw2, db2, dw1, db1


# Read all data from .pkl
(train_images, train_labels, test_images, test_labels) = pickle.load(open('./mnist_data/data.pkl', 'rb'),
                                                                     encoding='latin1')

### 1. Data preprocessing: normalize all pixels to [0,1) by dividing 256
train_images = train_images / 255
test_images = test_images / 255

### 2. Weight initialization: Xavier

input_layer_size = 784
layer1_size = 300
layer2_size = 100
output_size = 10

w1 = np.random.uniform(-math.sqrt(6) / math.sqrt(input_layer_size + layer1_size),
                       math.sqrt(6) / math.sqrt(input_layer_size + layer1_size),
                       (input_layer_size, layer1_size))
b1 = np.zeros(layer1_size)
w2 = np.random.uniform(-math.sqrt(6) / math.sqrt(layer1_size + layer2_size),
                       math.sqrt(6) / math.sqrt(layer1_size + layer1_size),
                       (layer1_size, layer2_size))
b2 = np.zeros(layer2_size)
w3 = np.random.uniform(-math.sqrt(6) / math.sqrt(layer2_size + output_size),
                       math.sqrt(6) / math.sqrt(layer2_size + output_size),
                       (layer2_size, output_size))
b3 = np.zeros(output_size)

onehot_labels = np.zeros((len(train_labels), 10))
for i in range(len(train_labels)):
    onehot_labels[i][train_labels[i]] = 1

onehot_labels_test = np.zeros((len(test_labels), 10))
for i in range(len(test_labels)):
    onehot_labels_test[i][test_labels[i]] = 1

### 3. training of neural network
loss = []
accuracy = []

for epoch in range(0, EPOCH):
    print("Epoch", epoch)
    if epoch < 50:
        eta = 0.1  # 学习率，后50epoch，降一个数量级
    else:
        eta = 0.01
    for i in range(ITERATION):
        x = train_images[i * BATCHSIZE:(i + 1) * BATCHSIZE]
        t = onehot_labels[i * BATCHSIZE:(i + 1) * BATCHSIZE]

        # Forward propagation
        a1, z1, a2, z2, a3, y = forward(x, w1, w2, w3, b1, b2, b3)
        # print("ITERATION", i)

        # Back propagation
        dw3, db3, dw2, db2, dw1, db1 = back(x, y, t, w2, w3)
        # print(db3.shape,db2.shape,db1.shape)

        # Gradient update
        N = BATCHSIZE
        w3 = w3 - eta * dw3.T / N - eta * lambd * w3
        b3 = b3 - eta * db3.T
        # print(dw3.T.shape)

        # N = dw2.T.shape[0]
        w2 = w2 - eta * dw2.T / N - eta * lambd * w2
        b2 = b2 - eta * db2.T
        # print(dw2.T.shape)

        # N = dw1.T.shape[0]
        w1 = w1 - eta * dw1.T / N - eta * lambd * w1
        b1 = b1 - eta * db1.T
        # print(dw1.T.shape)

    # Testing for loss
    a1, z1, a2, z2, a3, y = forward(x, w1, w2, w3, b1, b2, b3)
    iloss = -(np.log(y) * t).sum()
    print("loss after", iloss)
    loss.append(iloss)

    # Testing for accuracy
    x = test_images
    a1, z1, a2, z2, a3, estimate = forward(x, w1, w2, w3, b1, b2, b3)
    out = []
    for i in range(len(estimate)):
        out.append(np.argmax(estimate[i]))
    counter = 0
    for i in range(len(out)):
        if out[i] == test_labels[i]:
            counter += 1
    print("accuracy", counter / len(out))
    accuracy.append(counter / len(out))

    print(loss)
    print(accuracy)

### 4. Plot
plt.figure(figsize=(6, 5))

ax1 = plt.subplot(211)
ax1.plot(loss, '.-')
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel("Epoch", fontsize=16)
plt.ylabel("Loss", fontsize=16)
plt.grid()
plt.tight_layout()

ax2 = plt.subplot(212)
ax2.plot(accuracy, '.-')
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel("Epoch", fontsize=16)
plt.ylabel("Accuracy", fontsize=16)
plt.grid()
plt.tight_layout()

plt.savefig('figure.png', dpi=600)
plt.savefig('figure.eps', dpi=600)
plt.show()
