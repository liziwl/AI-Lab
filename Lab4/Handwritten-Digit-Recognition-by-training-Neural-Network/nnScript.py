import numpy as np
from scipy.optimize import minimize
from scipy.io import loadmat
from math import sqrt
import time
import pickle

def initializeWeights(n_in,n_out):
    """
    # initializeWeights return the random weights for Neural Network given the
    # number of node in the input layer and output layer

    # Input:
    # n_in: number of nodes of the input layer
    # n_out: number of nodes of the output layer
       
    # Output: 
    # W: matrix of random initial weights with size (n_out x (n_in + 1))"""
    
    epsilon = sqrt(6) / sqrt(n_in + n_out + 1);
    W = (np.random.rand(n_out, n_in + 1)*2* epsilon) - epsilon;
    return W
    
    
    
def sigmoid(z):
    
    """# Notice that z can be a scalar, a vector or a matrix
    # return the sigmoid of input z"""
    sigmoid_result = 1.0 / (1.0 + np.exp(-1.0 * z));
    return  sigmoid_result
    
    

def preprocess():
    """ Input:
     Although this function doesn't have any input, you are required to load
     the MNIST data set from file 'mnist_all.mat'.

     Output:
     train_data: matrix of training set. Each row of train_data contains 
       feature vector of a image
     train_label: vector of label corresponding to each image in the training
       set
     validation_data: matrix of training set. Each row of validation_data 
       contains feature vector of a image
     validation_label: vector of label corresponding to each image in the 
       training set
     test_data: matrix of training set. Each row of test_data contains 
       feature vector of a image
     test_label: vector of label corresponding to each image in the testing
       set

     Some suggestions for preprocessing step:
     - divide the original data set to training, validation and testing set
           with corresponding labels
     - convert original data set from integer to double by using double()
           function
     - normalize the data to [0, 1]
     - feature selection"""
    
    mat = loadmat('mnist_all.mat')
    # Dividing the data into training, test and Validation data
    data_train=np.empty((0,784))
    trn_lab=np.empty((0,1))
    data_test=np.empty((0,784))
    tes_lab=np.empty((0,1))
    data_val=np.empty((0,784))
    val_lab=np.empty((0,1))
    for i in range(10):
        m1 = mat.get('test'+str(i))
        m2 = mat.get('train'+str(i))
        num1 = m1.shape[0]
        num2 = m2.shape[0]
        num3 = int(0.83342*num2)
        num4 = num2 - num3
        b = range(m2.shape[0])
        permut_b = np.random.permutation(b)
        Z1 = m2[permut_b[0:num3],:]
        Z2 = m2[permut_b[num3:],:]
        data_train = np.vstack([data_train,Z1])
        data_val = np.vstack([data_val,Z2])
        data_test = np.vstack([data_test,m1])
        for p in range(num3):
            trn_lab = np.append(trn_lab,i)
        for q in range(num4):
            val_lab = np.append(val_lab,i)
        for r in range(num1):
            tes_lab = np.append(tes_lab,i)
                    
    # normalizing the data to values between to 0-1.
    data_test = data_test /255
    data_train = data_train / 255
    data_val = data_val / 255

    
    #Your code here
    train_data = data_train
    train_label = trn_lab
    validation_data = data_val
    validation_label = val_lab
    test_data = data_test
    test_label = tes_lab
    
    print(train_data.shape)
    
    print(train_label.shape) 
    print(validation_data.shape)
    print(validation_label.shape)
    print(test_data.shape) 
    print(test_label.shape)
    
    
    return train_data, train_label, validation_data, validation_label, test_data, test_label

    
    
    

def nnObjFunction(params, *args):
    """% nnObjFunction computes the value of objective function (negative log 
    %   likelihood error function with regularization) given the parameters 
    %   of Neural Networks, thetraining data, their corresponding training 
    %   labels and lambda - regularization hyper-parameter.

    % Input:
    % params: vector of weights of 2 matrices w1 (weights of connections from
    %     input layer to hidden layer) and w2 (weights of connections from
    %     hidden layer to output layer) where all of the weights are contained
    %     in a single vector.
    % n_input: number of node in input layer (not include the bias node)
    % n_hidden: number of node in hidden layer (not include the bias node)
    % n_class: number of node in output layer (number of classes in
    %     classification problem
    % training_data: matrix of training data. Each row of this matrix
    %     represents the feature vector of a particular image
    % training_label: the vector of truth label of training images. Each entry
    %     in the vector represents the truth label of its corresponding image.
    % lambda: regularization hyper-parameter. This value is used for fixing the
    %     overfitting problem.
       
    % Output: 
    % obj_val: a scalar value representing value of error function
    % obj_grad: a SINGLE vector of gradient value of error function
    % NOTE: how to compute obj_grad
    % Use backpropagation algorithm to compute the gradient of error function
    % for each weights in weight matrices.

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % reshape 'params' vector into 2 matrices of weight w1 and w2
    % w1: matrix of weights of connections from input layer to hidden layers.
    %     w1(i, j) represents the weight of connection from unit j in input 
    %     layer to unit i in hidden layer.
    % w2: matrix of weights of connections from hidden layer to output layers.
    %     w2(i, j) represents the weight of connection from unit j in hidden 
    %     layer to unit i in output layer."""
    
    n_input, n_hidden, n_class, training_data, training_label, lambdaval = args
    
    w1 = params[0:n_hidden * (n_input + 1)].reshape( (n_hidden, (n_input + 1)))
    w2 = params[(n_hidden * (n_input + 1)):].reshape((n_class, (n_hidden + 1)))
    obj_val = 0  
    
    #
    training_label = np.array(training_label)
    rows = training_label.shape[0];
    rowsIndex=np.arange(rows,dtype="int")
    # 
    tempLabel = np.zeros((rows,10))
    tempLabel[rowsIndex,training_label.astype(int)]=1
    training_label = tempLabel
    
    # nnFeedForwardward propogation
	# adding bias to the input data
    training_data = np.column_stack((training_data,np.ones(training_data.shape[0])))
    number_of_samples = training_data.shape[0]

    # passing the input data to the Hidden layer
    zj = sigmoid(np.dot(training_data,w1.T))
    # adding bias to the hidden layer
    zj = np.column_stack((zj,np.ones(zj.shape[0])))
    # passing the hidden layer data to the output layer
    ol = sigmoid(np.dot(zj,w2.T))
    
    # Back propogation
    deltaOutput = ol - training_label
    error = np.sum(-1*(training_label*np.log(ol)+(1-training_label)*np.log(1-ol)))
    error = error/number_of_samples

    gradient_of_w2 = np.dot(deltaOutput.T,zj)
    gradient_of_w2 = gradient_of_w2/number_of_samples
	
    gradient_of_w1 = np.dot(((1-zj)*zj* (np.dot(deltaOutput,w2))).T,training_data)
    gradient_of_w1 = gradient_of_w1/number_of_samples	
    gradient_of_w1 = np.delete(gradient_of_w1, n_hidden,0)
    
    #obj_grad = np.array([])
    obj_grad = np.concatenate((gradient_of_w1.flatten(), gradient_of_w2.flatten()),0)
    
    # obj_val
    error = error + (lambdaval/(2*number_of_samples))* ( np.sum(np.square(w1)) + np.sum(np.square(w2)))    
    obj_val = error
    
    return (obj_val,obj_grad)


def nnFeedForward(data,w1,w2):
	a=np.dot(data,w1.T)
	z=sigmoid(a);
	z = np.append(z,np.zeros([len(z),1]),1)
	b=np.dot(z,w2.T)
	o=sigmoid(b);
	index=np.argmax(o, axis=1);
	label=np.zeros((o.shape[0],10))
	for i in range(label.shape[0]):
		label[i][index[i]]=1
	return (z,o)
	
def nnPredict(w1,w2,data):
	"""% nnPredict predicts the label of data given the parameter w1, w2 of Neural
	% Network.
	% Input:
	% w1: matrix of weights of connections from input layer to hidden layers.
	% w1(i, j) represents the weight of connection from unit i in input
	% layer to unit j in hidden layer.
	% w2: matrix of weights of connections from hidden layer to output layers.
	% w2(i, j) represents the weight of connection from unit i in input
	% layer to unit j in hidden layer.
	% data: matrix of data. Each row of this matrix represents the feature
	% vector of a particular image
	% Output:
	% label: a column vector of predicted labels"""
	data = np.append(data,np.zeros([len(data),1]),1)
	n=data.shape[0]
	z,o=nnFeedForward(data,w1,w2);
	label=np.empty((0,1))
	for i in range(n):
		index=np.argmax(o[i]);
		label=np.append(label,index);
	return label

    



"""**************Neural Network Script Starts here********************************"""

start_Time = time.time()
train_data, train_label, validation_data,validation_label, test_data, test_label = preprocess();


#  Train Neural Network

# set the number of nodes in input unit (not including bias unit)
n_input = train_data.shape[1]; 

# set the number of nodes in hidden unit (not including bias unit)
n_hidden = 50;
				   
# set the number of nodes in output unit
n_class = 10;				   

# initialize the weights into some random matrices
initial_w1 = initializeWeights(n_input, n_hidden);
initial_w2 = initializeWeights(n_hidden, n_class);

# unroll 2 weight matrices into single column vector
initialWeights = np.concatenate((initial_w1.flatten(), initial_w2.flatten()),0)

# set the regularization hyper-parameter
lambdaval = 0.2;


args = (n_input, n_hidden, n_class, train_data, train_label, lambdaval)

#Train Neural Network using fmin_cg or minimize from scipy,optimize module. Check documentation for a working example

opts = {'maxiter' : 50}    # Preferred value.

nn_params = minimize(nnObjFunction, initialWeights, jac=True, args=args,method='CG', options=opts)

#In Case you want to use fmin_cg, you may have to split the nnObjectFunction to two functions nnObjFunctionVal
#and nnObjGradient. Check documentation for this function before you proceed.
#nn_params, cost = fmin_cg(nnObjFunctionVal, initialWeights, nnObjGradient,args = args, maxiter = 50)


#Reshape nnParams from 1D vector into w1 and w2 matrices
w1 = nn_params.x[0:n_hidden * (n_input + 1)].reshape( (n_hidden, (n_input + 1)))
w2 = nn_params.x[(n_hidden * (n_input + 1)):].reshape((n_class, (n_hidden + 1)))


#Test the computed parameters

predicted_label = nnPredict(w1,w2,train_data)

#find the accuracy on Training Dataset

print('\n Training set Accuracy:' + str(100*np.mean((predicted_label == train_label).astype(float))) + '%')

predicted_label = nnPredict(w1,w2,validation_data)

#find the accuracy on Validation Dataset

print('\n Validation set Accuracy:' + str(100*np.mean((predicted_label == validation_label).astype(float))) + '%')


predicted_label = nnPredict(w1,w2,test_data)

#find the accuracy on Validation Dataset

print('\n Test set Accuracy:' + str(100*np.mean((predicted_label == test_label).astype(float))) + '%')

total_Time = time.time() - start_Time

pickle.dump((n_hidden, w1, w2, lambdaval), open('params.pickle', 'wb'))
pickle_data = pickle.load(open('params.pickle','rb'))
print(pickle_data)
print(total_Time)