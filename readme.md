# Artificial intelligence
CS303 of SUSTech

## Environment
Lab 1-3: Python2
Lab 4: Python3 

## Lab1 - go
### [Report](./Lab1/doc/ProjectReport.pdf)

示例文件共有7个（train_0.txt, train_00.txt, train_1.txt ~ train_5.txt），其中每个示例文件存放一个围棋残局，存放格式为“行数 列数 颜色”，-1表示⿊色，1表示白色，
### 要求
1. train_0.txt和train_00.txt 检测程序对基本围棋规则的判定。
2. train_1.txt ~ train_4.txt的要求是列出落一子使得可以提对方子的位置，并绘出该位置，以及提子后的结果。
3. train_5.txt的要求是给出下一步所有可以落子的位置。

### numpy
* np.zeros((BOARD_SIZE, BOARD_SIZE))创建数组，参数为维度
* shape函数是numpy.core.fromnumeric中的函数,它的功能是读取矩阵的长度,比如shape[0]就是读取矩阵第一维度的长度。
* np.argwhere 条件查找，返回数组元素
* np.where  条件查找，返回下标

numpy additional materials：
1. [numpy official doc](https://docs.scipy.org/doc/numpy/genindex.html)
2. [TutorialsPoint NumPy 教程](http://www.jianshu.com/p/57e3c0a92f3a)

## Lab2 - Capacitated Arc Routing Problem (CARP)
### [Report](./Lab2/report/ProjectReport.pdf)

### Data Format

1st line: NAME : \<string> i.e., the name of the instance;

2nd line: VERTICES : \<number> i.e., the number of vertices;

3rd line: DEPOT : \<number>        i.e., the depot vertex;

4th line: REQUIRED EDGES : \<number>    i.e., the number of required edges (tasks);

5th line: NON-REQUIRED EDGES : \<number>      i.e., the number of non-required edges;

6th line: VEHICLES : \<number>      i.e., the number of vehicles;

7th line: CAPACITY : \<number>     i.e., the vehicle capacity;

8th line: TOTAL COST OF REQUIRED EDGES : \<number>   i.e., the total cost of all tasks;

9th line: NODES    COST    DEMAND

### Implement Path

1. Using Regular expression to read data and store them in format
2. Path scanning[1] generates initial solution.

    ![image](https://github.com/liziwl/AI-Lab/blob/master/Lab2/picture/path_scanning.JPG?raw=true)

    The `better()` function is using the following rules:

    ![image](https://github.com/liziwl/AI-Lab/blob/master/Lab2/picture/rule.JPG?raw=true)

3. Mutation[2] reproduct new generation.

#### Reference
[1] A. C. C. Corberán and G. Laporte, *Arc routing: problems, methods*, and applications. Philadelphia: Society for Industrial and Applied Mathematics, 2014.

[2] K. Tang, Y. Mei, and X. Yao, “Memetic algorithm with extended neighborhood search for capacitated arc routing problems,” *IEEE Transactions on Evolutionary Computation*, vol. 13, no. 5, pp. 1151–1166, 2009.

3. [Benchmarks of Vector Packing Problem](http://logistik.bwl.uni-mainz.de/benchmarks.php)

## Lab3 - Influence Maximization Problem
### [Report](./Lab3/report/Lab3.pdf)

Influence Maximization Problem is the problem of finding a small subset of nodes(seed nodes) in a social network,that could maximize the spread of influence. The IMP is NP-hard and the influence spread computation is \#P -hard under the definitions shown in the introduction. I improve **Degree Discount IC** Algorithm [1], which can pick up the parent of high impact node. Besides, I also implement influence spread estimator with **independent cascade** (IC) and **linear threshold** (LT) models.

#### Reference
[1] W. Chen, Y. Wang, and S. Yang, “Efficient influence maximization in social networks,” *Proceedings of the 15th ACM SIGKDD international conference on Knowledge discovery and data mining* - KDD 09, 2009.

## Lab4 - Handwritten digit recognition
### [Report](./Lab4/report/Lab4.pdf)

> implementing back propagation neural network
### Layer Size
* Inputer layer 784 nodes
* Hidden layer1 300 nodes
* Hidden layer2 100 nodes
* Output layer 10 nodes

### Data set
* [MNIST DATA](http://yann.lecun.com/exdb/mnist/)
