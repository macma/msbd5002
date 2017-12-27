import os
import numpy as np


def readFile():
    file = open("Q2Q3_input.csv", "r")
    str = file.read()
    str1 = str.split('\n')[1:]
    str2 = str1[:len(str1) - 1]
    print str2
    return str2


def iteration(ds, c1, c2):
    w1, w2, sse = calcC(ds, c1, c2)
    # print "w1, w2", w1, w2
    nc1, nc2 = calcE(w1, w2, c1, c2, ds)
    return nc1, nc2, sse

def calcC(ds, c1, c2):
    w1 = []
    w2 = []
    sse = 0.0
    for i in range(len(ds)):
        dc1 = getDistanceSquare(c1, ds[i].split(',')[1:])
        dc2 = getDistanceSquare(c2, ds[i].split(',')[1:])
        w1.append(dc2 / (dc1 + dc2))
        w2.append(1 - w1[i])
        sse = sse + dc1 * dc2 * 2 / (dc1 + dc2)
    print 'sse: ', sse
    return w1, w2, sse
    # calcE(w1, w2, c1, c2)


def calcE(w1, w2, c1, c2, ds):
    c1square = getCsquare(w1)
    c2square = getCsquare(w2)
    # print 'c1square',c1square, 'c2square',c2square
    cp1 = []
    cp2 = []
    nc1 = []
    nc2 = []
    for i in range(len(c1)):#6 iterations
        cp1.append(0.0)
        cp2.append(0.0)
        for j in range (len(w1)):#647 iterations
            cp1[i] = cp1[i] + np.power(w1[j], 2) * float((ds[j].split(',')[1:])[i])
            cp2[i] = cp2[i] + np.power(w2[j], 2) * float((ds[j].split(',')[1:])[i])
    for i in range(len(c1)):
        nc1.append(cp1[i] / c1square)
        nc2.append(cp2[i] / c2square)
    return nc1, nc2

def getCsquare(c):
    result = 0.0
    for i in range(len(c)):
        result = result + np.power(c[i], 2)
    return result


def getDistanceSquare(p1, p2):
    result = 0.0
    for i in range(len(p1)):
        result = result + np.power((float(p1[i]) - float(p2[i])), 2)
    return result

def getL1Distance(p1, p2):
    result = 0.0
    for i in range(len(p1)):
        result = result + np.absolute(p1[i]-p2[i])
    return result
def initData():
    
    c1 = (1, 1, 1, 1, 1, 1)
    c2 = (0, 0, 0, 0, 0, 0)
    ds = readFile()
    #c1 = (3,3)
    #c2 = (4,10)
    #ds = ['1,3,3','2,4,10','3,9,6','4,14,8','5,18,11','6,21,7']
    return c1, c2, ds
if (__name__ == '__main__'):
    c1, c2, ds = initData()
    # print c1
    counter = 0
    totalsse = 0.0
    while (counter <= 50):
        nc1, nc2, sse = iteration(ds, c1, c2)
        totalsse = totalsse + sse
        print (str(counter + 1), "SSE: ", sse, "iteration, new c1: ", str(nc1), "; new c2: ", nc2)
        counter = counter + 1
        if(getL1Distance(nc1, c1) < 0.001 and getL1Distance(nc2, c2) < 0.001):
            break;
        else:
            c1 = nc1
            c2 = nc2
