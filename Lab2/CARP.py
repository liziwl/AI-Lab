# encoding: utf-8
import re


# 修改列表为数字存储

def readData(filename):
    # 0-7行，数据定义
    # 8行开始，数据本体
    f = open(filename, 'r')
    Pattern = ["NAME : (.*)", "VERTICES : ([0-9]*)",
               "DEPOT : ([0-9]*)",
               "REQUIRED EDGES : ([0-9]*)",
               "NON-REQUIRED EDGES : ([0-9]*)",
               "VEHICLES : ([0-9]*)",
               "CAPACITY : ([0-9]*)",
               "TOTAL COST OF REQUIRED EDGES : ([0-9]*)"]
    data = f.readlines()
    count = 0
    fData = []
    for it in data:
        if count == 0:
            fData.append(re.findall(Pattern[count], it)[0])
            count += 1
        elif count <= 7:
            # print count
            # print it
            # print re.findall(Pattern[count],it)
            fData.append(int(re.findall(Pattern[count], it)[0]))
            count += 1
        elif count == 8:
            count += 1
        elif 'END' in it:
            break
        else:
            temp = it.split()
            for i in range(0, len(temp)):
                temp[i] = int(temp[i])
            fData.append(temp)
    return fData


def matrixTran(data):
    vmap = {}

    for it in range(8, len(data)):
        # print data[it]
        if data[it][0] in vmap:
            temp = vmap[data[it][0]]
            temp[data[it][1]] = (data[it][2], data[it][3])
        else:
            temp = {}
            temp[data[it][1]] = (data[it][2], data[it][3])
            vmap[data[it][0]] = temp

        if data[it][1] in vmap:
            temp = vmap[data[it][1]]
            temp[data[it][0]] = (data[it][2], data[it][3])
        else:
            temp = {}
            temp[data[it][0]] = (data[it][2], data[it][3])
            vmap[data[it][1]] = temp
    return vmap


if __name__ == '__main__':
    # print readData("CARP_samples\\egl-e1-A.dat")
    # print readData("CARP_samples\\egl-s1-A.dat")
    # print readData("CARP_samples\\gdb1.dat")
    # print readData("CARP_samples\\gdb10.dat")
    # print readData("CARP_samples\\val1A.dat")
    # print readData("CARP_samples\\val4A.dat")
    # print readData("CARP_samples\\val7A.dat")

    sample = readData("CARP_samples\\egl-e1-A.dat")
    print sample

    vmap = matrixTran(sample)
    print vmap
