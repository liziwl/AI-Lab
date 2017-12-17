# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 19:55:44 2016
PythonVersion: 2.7.12
@author: Siyuan Wang

2-layer Neural Network with backpropagation

Inspired by the neural network learning exercise of Machine Learning@Coursera
https://www.coursera.org/learn/machine-learning/programming/AiHgN/neural-network-learning

default size: input layer:784=28*28, hidden layer: 300, output layer:10
"""
import numpy as np

class NN2(object):
    def __init__(self, iu = 784, hu1 = 300, ou = 10):
        # define the number of input-, hidden- and output units.
        self.iu = iu
        self.hu1 = hu1
        self.ou = ou
        # weights matrices of the input and hidden layers
        self.theta1 = []
        self.theta2 = []

    # backpropagation
    def __Back(self, X, y, theta1, theta2, Lambda, ou, h, a1, a2, z2, z3, m):     
        Delta1 = np.zeros(np.shape(theta1))
        Delta2 = np.zeros(np.shape(theta2))
        for i in range(m):
            yi = np.zeros(ou)
            yi[y[i]] = 1
            delta3 = h[i,:] - yi
            delta2 = np.matmul(theta2[:,1:].T, delta3) * self.__SigmoidGradient(z2[i,:])
            Delta1 = Delta1 + \
                np.matmul(delta2.reshape((-1,1)), a1[i,:].reshape((1,-1)))
            Delta2 = Delta2 + \
                np.matmul(delta3.reshape((-1,1)), a2[i,:].reshape((1,-1)))
        # compute partial derivatives
        theta1_grad = 1./m * Delta1
        theta1_grad[:,1:] = theta1_grad[:,1:] + Lambda/m * theta1[:,1:]
        theta2_grad = 1./m * Delta2
        theta2_grad[:,1:] = theta2_grad[:,1:] + Lambda/m * theta2[:,1:]
        return theta1_grad, theta2_grad

    # check the gradient descent computed using backpropagation vs. using
    # numerical estimate of gradient of J(theta)
    def CheckGradient(self, Lambda=0):
        # build a smaller NN
        iu, hu1, ou = 3, 5, 3
        m = 5
        X = self.__Randinitial(m, iu, debug=1)
        y = np.mod(np.arange(m), ou)
        theta1 = self.__Randinitial(hu1, iu+1)
        theta2 = self.__Randinitial(ou, hu1+1)
        # implement forward propagation
        h, a1, a2, z2, z3, m = self.__Forward(X, theta1, theta2)
        # compute the gradient with backpropagation
        theta1_grad, theta2_grad = \
            self.__Back(X, y, theta1, theta2, Lambda, ou, h, a1, a2, z2, z3, m)
        # compute the gradient with numerical methode
        theta1_grad_num, theta2_grad_num = \
            self.__NumGradient(X, y, theta1, theta2, Lambda, ou)
        # flatten the gradients and compare them one by one
        theta_grad = np.append(np.ravel(theta1_grad),np.ravel(theta2_grad))
        theta_grad_num = \
            np.append(np.ravel(theta1_grad_num),np.ravel(theta2_grad_num))
        print "backpropagation vs. numerial gradient:"
        for i in range(theta_grad.size):
            print "%f vs. %f" %(theta_grad[i], theta_grad_num[i])
        # compute the normalized difference
        grad_norm = np.linalg.norm(theta_grad - theta_grad_num) / \
                    np.linalg.norm(theta_grad + theta_grad_num)
        print "the normalized difference is %f" %grad_norm
        
    # cost function J(theta1, theta2)
    def __CostFunction(self, X, y, h, theta1, theta2, m, ou, Lambda=0):
        J = 0.
        # compute J num_label by num_label
        for k in range(ou):
            yk = y==k
            J = J - \
                1./m * np.sum(yk * np.log(h[:,k]) + (1-yk) * np.log(1-h[:,k]))
        # add regularization item
        J = J + \
            Lambda/2./m * (np.sum(theta1[:,1:]**2) + np.sum(theta2[:,1:]**2))
        return J
    
    # display the tested image and the predicted result
    def Display(self, X, theta1=[], theta2=[]):
        import matplotlib.cm as cm
        import matplotlib.pyplot as plt
        image = X.reshape((28,28))
        plt.imshow(image, cmap=cm.gray)
        plt.show()
        print "It's predicted to be %d" \
            %self.Predict(X.reshape((-1,28*28)), theta1, theta2)
            
    # forward propagation
    def __Forward(self, X, theta1, theta2):
        m = int(X.shape[0])
        bias = np.ones([m,1])
        a1 = np.column_stack((bias, X))
        z2 = np.matmul(a1, theta1.T)
        a2 = np.column_stack((bias, self.__Sigmoid(z2)))
        z3 = np.matmul(a2, theta2.T)
        h = self.__Sigmoid(z3)       
        return h, a1, a2, z2, z3, m
 
    # gradient descent methode to minimize costf function
    def __GradientDescent(self, theta, theta_grad, alpha):
        theta_new = theta - alpha * theta_grad
        return theta_new
                         
    # initalize weight matrices theta1 and theta2
    def InitTheta(self, theta1, theta2):
        self.theta1 = theta1
        self.theta2 = theta2
                         
    # compute numerial gradient with +- epsilon
    def __NumGradient(self, X, y, theta1, theta2, Lambda, ou, epsilon = 0.0001):
        theta1_grad_num = np.zeros(np.shape(theta1))
        theta2_grad_num = np.zeros(np.shape(theta2))
        # compute theta1_grad_num
        for i in range(np.shape(theta1)[0]):
            for j in range(np.shape(theta1)[1]):
                theta1_ijplus = np.copy(theta1)
                theta1_ijminus = np.copy(theta1)
                theta1_ijplus[i,j] = theta1[i,j] + epsilon
                theta1_ijminus[i,j] = theta1[i,j] - epsilon
                hp, a1p, a2p, z2p, z3p, mp = \
                    self.__Forward(X, theta1_ijplus, theta2)
                hm, a1m, a2m, z2m, z3m, mm = \
                    self.__Forward(X, theta1_ijminus, theta2)
                theta1_grad_num[i,j] = \
                  (self.__CostFunction(X,y,hp,theta1_ijplus,theta2,mp,ou,Lambda) -\
                  self.__CostFunction(X,y,hm,theta1_ijminus,theta2,mm,ou,Lambda))/\
                   (2.*epsilon)
        # compute theta2_grad_num
        for i in range(np.shape(theta2)[0]):
            for j in range(np.shape(theta2)[1]):
                theta2_ijplus = np.copy(theta2)
                theta2_ijminus = np.copy(theta2)
                theta2_ijplus[i,j] = theta2[i,j] + epsilon
                theta2_ijminus[i,j] = theta2[i,j] - epsilon
                hp, a1p, a2p, z2p, z3p, mp = \
                    self.__Forward(X, theta1, theta2_ijplus)
                hm, a1m, a2m, z2m, z3m, mm = \
                    self.__Forward(X, theta1, theta2_ijminus)
                theta2_grad_num[i,j] = \
                  (self.__CostFunction(X,y,hp,theta1,theta2_ijplus,mp,ou,Lambda) -\
                  self.__CostFunction(X,y,hm,theta1,theta2_ijminus,mm,ou,Lambda))/\
                   (2.*epsilon)
        return theta1_grad_num, theta2_grad_num
   
    # use the trained neural network to identify images(m*n)
    def Predict (self, X, theta1=[], theta2=[]):
        if theta1 == []: theta1 = self.theta1
        if theta2 == []: theta2 = self.theta2
        h = self.__Forward(X, theta1, theta2)[0]
        y = np.argmax(h,axis=1).astype(int)
        return y
        
    # random initalize weight matrices theta1 and theta2, debug-mode for CheckGradient
    def __Randinitial(self, output_size, input_size, debug = 0, epsilon = 0.1):
        if debug == 1:
            W = np.arange(output_size*input_size).reshape([output_size, input_size])
            W = np.sin(W)*128
        else:
            W = np.random.random([output_size, input_size])*epsilon*2 - epsilon
        return W

    # logistic function for classification
    def __Sigmoid(self, z):
        return (np.exp(-z)+1)**-1

    # derivative of sigmoid function
    def __SigmoidGradient(self, z):
        g = self.__Sigmoid(z)
        return g * (1-g)

    # use the test_set to calculate the accuracy of the trained neural network
    def Test(self, X, y):
        pred = self.Predict(X)
        right_num = np.sum(pred == y)
        accuracy = float(right_num) / y.size
        print "the accuracy of test set is %f" %accuracy
        return accuracy
    
    # use the train_set to train the neural network
    def Train(self, X, y, max_iter=50, Lambda=1, alpha=0.3, randinit = True):
        if randinit == True:
            # random initialize theta1, theta2
            theta1 = self.__Randinitial(self.hu1, self.iu+1)
            theta2 = self.__Randinitial(self.ou, self.hu1+1)
        else:
            theta1 = self.theta1
            theta2 = self.theta2
        J_array = []
        # training before maximale iteration, or the gradient is small enough
        for i in range(max_iter):
            # implement forward propagation
            h, a1, a2, z2, z3, m = self.__Forward(X, theta1, theta2)
            # implement backpropagation
            theta1_grad, theta2_grad = \
                self.__Back(X, y, theta1, theta2, Lambda, self.ou, h, a1, a2, z2, z3, m)
            # compute cost function
            Ji = self.__CostFunction(X, y, h, theta1, theta2, m, self.ou, Lambda)
            if i == 0:
                delta_J = 0
            else:
                delta_J = J_array[i-1]-Ji
                if abs(delta_J) < 1e-6:
                    print "No.%d: J = %f, delta_J = %f, iteration stop because\
                    the difference is small enough" %(i+1, Ji, delta_J)
                    break
            print "No.%d: J = %f, and the improvement from last iteration is %f" \
                %(i+1, Ji, delta_J)
            J_array.append(Ji)
            # update theta1, theta2
            theta1 = self.__GradientDescent(theta1, theta1_grad, alpha)
            theta1 = self.__GradientDescent(theta1, theta1_grad, alpha)
        self.theta1 = theta1
        self.theta2 = theta2
        import matplotlib.pyplot as plt
        plt.plot(J_array)
        plt.xlabel('Iteration times')
        plt.ylabel('J')
        plt.show()
        return theta1, theta2
