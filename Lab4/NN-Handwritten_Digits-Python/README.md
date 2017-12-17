# NN-Handwritten_Digits-Python
a simple two-layer neural network for handwritten digits recognition

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
To use this code you need to install Python 2.7 with Numpy and Matplotlib libraries, clone all the files and download the [MNIST database files](http://yann.lecun.com/exdb/mnist/) to the folder `MNIST_data`. This project was tested in Windows 10. As Linux or OS X user you may need to adjust the path.

Then just run `main.py`. It works in following steps:

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

##Program Description
---
You can find the details in de [documentation](https://github.com/siyuan0103/NN-Handwritten_Digits-Python/blob/master/Documentation.md).

##License
---
It's open source code using MIT licence.
