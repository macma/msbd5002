import os
import numpy as np


def readFile():
    file = open("Q2Q3_input.csv", "r")
    str = file.read()
    str1 = str.split('\n')[1:]
    str2 = str1[:len(str1) - 1]
    print str2
    return str2


def getDistance(ds, distType):
    distanceList = []
    for i in range(len(ds)):
        for j in range(i + 1, len(ds)):
            distance = 0.0
            for k in range(1, len(ds[0].split(','))):
                if(distType == 'l1'):
                    distance = distance + np.absolute(float(ds[i].split(',')[k]) - float(ds[j].split(',')[k]))
                else:
                    distance = distance + np.square(float(ds[i].split(',')[k]) - float(ds[j].split(',')[k]))
            
            if(distType == 'l1'):
                distanceList.append((i, j, distance))
            else:
                distanceList.append((i, j, np.sqrt(distance)))
    return distanceList


def getDistK(k, distanceList):
    k1 = []
    for i in range(len(ds)):
        c = 0
        k2 = []
        for j in range(len(distanceList)):
            if (distanceList[j][0] == i or distanceList[j][1] == i):
                c = c + 1
                slave = 0
                if(distanceList[j][0] == i):
                    slave = distanceList[j][1]
                else:
                    slave = distanceList[j][0]
                it = (slave, distanceList[j][2])
                k2.append(it)
        a = (i, sorted(k2, key=lambda x: x[1]))
        k1.append(a)
    return k1


def getReachdist(a, b, distK, k):
    d1 = distK[b][1][k - 1][1]  # dist k b
    d2 = 0.0
    for i in range(len(distK[a][1])):
        if (distK[a][1][i][0] == b):
            d2 = distK[a][1][i][1]
            break
    # return d1, d2
    return np.maximum(d1, d2)


def getNk(a, diskK, k):
    nd = 0
    rd = 0.0
    rdlist = []
    ndrd = 0.0
    for i in range(len(diskK)):
        if(a == diskK[i][0]):
            for j in range(len(diskK[i][1])):
                if(diskK[i][1][j][1] <= diskK[i][1][k - 1][1]):
                    nd = nd + 1
                    rdlist.append(diskK[i][1][j][0])
                    # if(a == 0):
                    rd = rd + getReachdist(a, diskK[i][1][j][0], diskK, k)
                else:
                    break
    return nd / rd, rd, nd, rdlist


def getLrd(distK, k):
    nk = []
    for i in range(len(distK)):
        nk.append(getNk(i, distK, k))
    # print nk
    return nk


def getLOF(lrd):
    ls = []
    for i in range(len(lrd)):
        lrdsum = 0.0
        for j in range(len(lrd[i][3])):
            lrdsum = lrdsum + lrd[lrd[i][3][j]][0]
        ls.append((i, lrdsum * lrd[i][1] / np.power(lrd[i][2], 2)))
    return ls


def initData():
    ds = readFile()
    # ds = ['1,0,0', '2,0,1', '3,1,1', '4,3,0']
    return ds


if (__name__ == '__main__'):
    ds = initData()
    #distanceList = getDistance(ds, 'l1')
    distanceList = getDistance(ds, 'euclidean')
    print 'getEuclideanDis', distanceList
    k = 2
    distk = getDistK(k, distanceList)
    lrd = getLrd(distk, k)
    lofresult = getLOF(lrd)
    # print len(lofresult)
    # # print lofresult[0]
    print sorted(lofresult, key=lambda x: x[1], reverse=True)
