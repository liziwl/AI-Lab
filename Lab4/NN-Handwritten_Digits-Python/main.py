# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 18:14:07 2016

@author: Siyuan Wang

the main program for handwritten digits regcognition use 2-layer neural network
with backpropagation
"""
# digit recognition with 2-Layer NeuralNetwork
#import os
#import numpy as np
from time import clock
from mnist import MNIST
from nn2 import NN2
from hms import hms
import random

# load MNIST database, the MNIST data files should be already in \MNIST_data folder
imagelib = MNIST('MNIST_data')
n_train = 60000
X_train, y_train = imagelib.train_img[:n_train,:], imagelib.train_lab[:n_train]
n_test = 10000
X_test, y_test = imagelib.test_img[:n_test,:], imagelib.test_lab[:n_test]

# create a neural network object
myNN = NN2()

# use the numerical gradient check to verify the backpropagation
myNN.CheckGradient(Lambda=1)

# use train_set to train the neural network with backpropagation
start = clock()
theta1, theta2 = myNN.Train(X_train,y_train,max_iter=100, alpha=0.3)
finish = clock()
print "The training costs %d H, %d Min, %f S" %(hms(finish-start))

# use the test_set to check the accuracy of the neural network
myNN.Test(X_test,y_test)

# and display 10 examples from test_set 
for i in range(10):
    random.seed()
    myNN.Display(X_test[random.randrange(0,n_test)])

# save weights matrics
with open('theta1.dat','wb') as f:
    f.write(theta1)
with open('theta2.dat','wb') as f:
    f.write(theta2)
