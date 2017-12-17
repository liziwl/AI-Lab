# NN-Handwritten Digits-Python
---
## Overview
---
It's my "Hello World" project of neural network written in Python2. A 2-layer neural network with backpropagation is programmed for handwritten digits recognition. The handwritten digits database comes from [Yann LeCun](http://yann.lecun.com/exdb/mnist/), with 60,000 training sets and 10,000 testing sets. The accuracy of this neural network is about 87% after 100 iterations of training, and 91.5% after 300 iterations.

The project includes three parts:

* mnist.py contains the class `MNIST()` for the loading of MNIST database.
* nn2.py contains the class `NN2()` as a 2-layer neural network.
* main.py shows how to use the `MNIST()` and `NN2()` to train and test the neural network for digits recognition.

Besides there is a hms.py file to support main.py, with a simple function to convert seconds into HH:MM:SS.

## How To Use
---
main.py is a simple example for this project. It works in following steps:

* Load the MNIST database.
	* `imagelib = MNIST('MNIST_data')`: create a instance of class 'MNIST()', with the MNIST database files in \MNIST_data folder

	* `n_train = 60000`, `n_test = 10000`: set the amouts of examples for training (max. 60000) and testing (max.10000). More training examples brings certainly higher accuracy, and costs also significantly more time.

	* pass the images and labels of  training and testing examples into `X_train`, `y_train`, `X_test`, `y_test`

* Train and test neural network with randomly initialized weight matrices.

	* `myNN = NN2()`: create a instance of class `NN2()` with the default sizes of input-, hidden- and output-layers.
	
	* `myNN.CheckGradient(Lambda=1)`: check the correctness of backpropagation with regularization parameters of cost function `Lambda = 1`, if the difference of two groups of partial derivatives is small enough, continue.

	* `theta1, theta2 = myNN.Train(X_train, y_train, max_iter=100, alpha=0.3)`: train the neural network with the training set. The trained weight matrices will passed into array `theta1` and `theta2`. The weight matrices are randomly initialized with parameter `randinit` as default value `True`. If the initial weight matrices are given, first use method `myNN.InitTheta(theta1, theta2)` to initialize them and then set the parameter `randinit=False` here.

	* `myNN.Test(X_test, y_test)`: test the trained neural network with testing set, and print the accuray.

	* Visualize the result. Use method  `myNN.Display()` to display the first 10 images of testing set and try to recognize what they are.

	* Storage the trained weight matrices into files `theta1.dat` and `theta2.dat`.

##  Program Description
---

## mnist.py：class `MNIST()`

This class is coded for reading MNIST database. 
### Variables:
#### `self.path`: string:

&emsp;path of the folder, which contains MNIST dataset files. Initialized with parameter `path=''`. When the MNIST data files are located in the same folder, just leave `path` parameter as default. Else, set the relative path with the `path` parameter.

#### `self.train_img` and `self.test_img`: 2D-array:

&emsp;image arrays of training and testing set.

#### `self.train_lab` and `self.test_lab`: 1D-array:

&emsp;label array of training and testing set.

### Public Method:

#### `display(self, tag='train', idx=0)`

##### Parameter:
`tag`: = {'train' (default), 'test}:

&emsp; choose the dataset.

`idx`: int, default 0:

&emsp; choose the example.

##### Description:
This method is used for plotting the image and print the label of an example.

### Private Method:

#### `load(img_file, lab_file)`
##### Parameters:

`img_file`: string:&emsp; path of image file.

`lab_file`: string:&emsp; path of label file.

##### Returns:
`img`: 2D numpy array, size (n_example, n_row*n_column), uint8:&emsp; array of images.

`lab`: 1D numpy array, size(n_example), int8:&emsp; array of labels.

`rows`: int32:&emsp; number of vertical pixels of an image.

`columns`: int32:&emsp; number of horizontal pixels of an image.
##### Description:
The `load` method is used to convert the image and label files of MNIST database into numpy arrays:

**File format of image files(idx3-ubyte):**

|offset|type|value|description|
|------|-----|------|------------|
|0000|int32|0x00000803(2051) magic number|(MSB first)|
|0004|int32|60000(train_set) or 10000(test_set)|number of images|
|0008|int32|28|number of rows|
|0012|int32|28|number of columns|
|0016|uint8|??|pixel|
|0017|uint8|??|pixel|
|...|...|...|...|

**File format of label files(idx1-ubyte):**

|offset|type|value|description|
|------|-----|------|------------|
|0000|int32|0x00000801(2049) magic number|(MSB first)|
|0004|int32|60000(train_set) or 10000(test_set)|number of labels|
|0008|uint8|??|label|
|0011|uint8|??|label|
|...|...|...|...|

**converted numpy arrays:**

Variable|Type|Size|description
---|---|---|---
`self.train_img`|uint8|60000*784|training images
`self.train_lab`|int8|60000|training labels
`self.test_img`|uint8|10000*784|testing images
`self.test_lab`|int8|10000|testing labels


## nn2.py: class `NN2()`
This class define a 2-layer neural network with backpropagation. 
###  Variables:

 #### `self.iu`: int, default 784: 

&emsp;Number of units in the input-layer (input-layer-size). The default value is the number of pixels of an image from MNIST database.

#### `self.hu1`: int, default 300: 

&emsp;Number of units in the hidden-layer (hidden-layer-size).

#### `self.iu`: int, default 10: 

&emsp;Number of units in the ouput-layer (ouput-layer-size).

#### `self.theta1`: numpy array of float, size: (hu1, (iu+1)):

&emsp;Weight matrix from input-layer to hidden-layer

#### `self.theta2`: numpy array of float, size: (ou, (hu1+1)):

&emsp;Weight matrix from hidden-layer to output-layer

### Public methods:
#### `CheckGradient(Lambda=0)`
##### Parameters:
`Lambda`: optional, float.
&emsp;The regularization parameter of the cost function
##### Description:
Check if the backpropagation is correctly programmed by the following setps:

* A small neural network will be randomly created.
* Implement the forward propagation with`Forward()`.
* Use the backpropagation `Back()` and the numerial gradient method `NumGradient()` to compute the partial derivatives of weight metrices separately.
* Compare the two sets of partial derivatives.
With a small enough difference, we can say that the backpropagation works well.

#### `Train(self, X, y, max_iter=50, Lamda=1, alpha=0.3, randinit=True)`
##### Parameters:

`X`: 2D-array, size (n_example, n_feature):&emsp;array of  examples.

`y`: 1D-array, size (n_example):&emsp;array of labels.

`max_iter`: int, default 50:&emsp;maximal iteration times of training.

`Lambda`: float, defaut 1:&emsp;regularization parameter of cost function. The algorithm tend to be underfitting with large lambda, and overfitting with small lambda.

`alpha`: float, default 0.3:&emsp; learning rate to minize the cost function. 

`randint`: bool, default True:&emsp; weight metrices will be randomly initialized if True, or read from `self.theta1` and `self.theta2` if False.
##### Returns:
`theta1`: 2D-numpy array, size (self.hu1,(self.iu+1)), float:&emsp; trained weight matrices from input layer to hidden layer.

`theta2`: 2D-numpy array, size (self.ou,(self.hu1+1)), float:&emsp; trained weight matrices from hidden layer to output layer.
##### Description:
In every iteration will the forward propagation and backpropagation implemented to get the partical derivatives of the cost function J(theta), then use a simple gradient method to minimize the cost function. Iteration stops when the maximal times are arrived, or the difference of J from the last iteration is small than 0.0001.

#### `Test(X, y)`
##### Parameters:
`X`: 2D numpy array , size (n_example, n_feature):&emsp;input array of test set.
`y`: 1D numpy array, size (n_example): label array of test set.
##### Return:
`accuracy`: float: &emsp; accuray of test, (number of correct predicted examples)/(total number of test examples)
##### Description:
This method is used for evaluating the training quality of the neural network. All the examples in test set are predicted by the trained neural network and the results will be compared with the labels. If a neural network with very small cost function J(theta) in the training get a low accuracy here, the overfitting problem should be considered.

#### `Predict(X, theta1=[], theta2=[])`
##### Parameters:
`X`: 2D numpy array, size (n_example, n_feature):&emsp;input array of test set.

`theta1`: 2D numpy array, size (self.hu1, (self.iu+1)), optional, default self.theta1:&emsp;weight matrices from input layer to hidden layer.

`theta2`: 2D numpy array, size (self.ou, (self.hu+1)), optional, default self.theta2:&emsp;weight matrices from hidden layer to output layer.
##### Return:
`y` : 1D numpy array, size (n_example), int:&emsp;predicted value of the input image.
##### Description:
This method receives a group of images and uses the trained neural network to recognize them. We can also input fremd weight matrices.

#### `Display(X, theta1=[], theta2=[])`
##### Discription
This method is similar to the `Predict(X, theta1=[], theta2[])` method. But for one time we can only input one image. Then this image will be plotted and recognized.

#### `InitTheta(theta1, theta2)`
##### Parameters:
`theta1`: 2D numpy array, size (self.hu1, (self.iu+1)), optional, default self.theta1:&emsp;given weight matrices from input layer to hidden layer.

`theta2`: 2D numpy array, size (self.ou, (self.hu+1)), optional, default self.theta2:&emsp;given weight matrices from hidden layer to output layer.
##### Description:
With this method we can initialize the neural network with some given weight matrices, so the training can be continued from the last time.
### Private Methods:
#### `__Forward(...)`
Forward propagation is the basic algorithm of a neural network.
#### `__Back(...)`
Backpropagation method for the rapid calculation of partial derivatives of cost function.
#### `__CostFunction(...)`
To compute the cost function of the neural network.
#### `__NumGradient(...)`
Use the numerical method to calculate the approximate values of partial derivatives. This method is very slow but reliable.
#### `__GradientDescent(...)`
This is the gradient descent method to minimize cost function J(theta).
#### `__Randinitial`
Randomly initialize the weight matrices.
#### `__Sigmoid`
The sigmoid function evaluates the activity of each neural cells.
#### `__SigmoidGradient`
To compute the gradient of a sigmoid function. 
