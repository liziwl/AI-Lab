# AI
## Lab1 - go
示例文件共有7个（train_0.txt, train_00.txt, train_1.txt ~ train_5.txt），其中每个示例文件存放一个围棋残局，存放格式为“行数 列数 颜色”，-1表示⿊色，1表示白色，
### 要求
1. train_0.txt和train_00.txt检测程序对围棋规则的判定
2. train_1.txt ~ train_4.txt的要求是“给出所有可以提子的位置”
3. train_5.txt的要求是“给出所有可以落子的位置”，

### numpy
* np.zeros((BOARD_SIZE, BOARD_SIZE))创建数组，参数为维度
* shape函数是numpy.core.fromnumeric中的函数,它的功能是读取矩阵的长度,比如shape[0]就是读取矩阵第一维度的长度。
* np.argwhere 条件查找，返回数组元素
* np.where  条件查找，返回下标

numpy additional materials：
1. [Doc](https://docs.scipy.org/doc/numpy/genindex.html)
2. [TutorialsPoint NumPy 教程](http://www.jianshu.com/p/57e3c0a92f3a)
