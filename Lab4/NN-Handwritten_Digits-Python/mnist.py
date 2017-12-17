# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 19:24:02 2016
PythonVersion: 2.7.12
@author: Siyuan Wang

Read image and label data from MNIST hand writing digits data set.
MNIST is downloaded from http://yann.lecun.com/exdb/mnist/

Inspired by https://gist.github.com/akesling/5358964
and https://github.com/sorki/python-mnist

"""
import os
import struct
import numpy as np

class MNIST(object):
    def __init__(self, path = ''):
        self.path = path
        self.train_img_file =\
            os.path.join(self.path, 'train-images.idx3-ubyte')
        self.train_lab_file =\
            os.path.join(self.path, 'train-labels.idx1-ubyte')
        self.test_img_file = \
            os.path.join(self.path, 't10k-images.idx3-ubyte')
        self.test_lab_file = \
            os.path.join(self.path, 't10k-labels.idx1-ubyte')
        self.train_img, self.train_lab, self.rows, self.columns= \
            self.__load(self.train_img_file, self.train_lab_file)
        self.test_img, self.test_lab = \
            self.__load(self.test_img_file, self.test_lab_file)[0:2]

    def __load(self, img_file, lab_file):           
        with open(img_file, 'rb') as f:
            magic, num, rows, columns = struct.unpack('>IIII', f.read(16))
            if magic != 2051:
                raise ValueError('The file "',img_file, 
                '" is not a image file')
            img = np.fromfile(f, dtype = np.uint8).reshape(num, rows*columns)
            
        with open(lab_file, 'rb') as f:
            magic, num = struct.unpack('>II', f.read(8))
            if magic != 2049:
                raise ValueError('The file "', lab_file, 
                '" is not a label file')
            lab = np.fromfile(f, dtype = np.int8)
        return img, lab, rows, columns
    
    def display(self, tag='train', idx = '0'):
        import matplotlib.cm as cm
        import matplotlib.pyplot as plt
        
        if tag == 'train':
            image = self.train_img[idx].reshape(self.rows, self.columns)
            label = self.train_lab[idx]
        
        if tag == 'test':
            image = self.test_img[idx].reshape(self.rows, self.columns)
            label = self.test_lab[idx]

        plt.imshow(image, cmap=cm.gray)
        plt.title(label)
        plt.show()
