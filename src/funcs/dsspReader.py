import os
import sys
from collections import deque

from sympy import residue
from src.funcs.pdbReader import readPDB


class readDSSP:
    def __init__(self, pdbID: str):
        self.dsspID = pdbID.lower()
        self.__dsspPath = "./materials/dssp/"
        self.__dsspFile = os.path.join(
            self.__dsspPath, "{}.dssp".format(self.dsspID))
        self.__dsspExist()

    def __str__(self):
        return str(self.getAHelix())

    def __dsspExist(self):
        if os.path.exists(self.__dsspFile):
            # print("DSSP file exist!")
            return 0
        else:
            sys.exit("DSSP file doesn't exist!")

    def getAHelix(self):
        '''返回α螺旋位置，下标从0开始。例如[1, 3]为第二个到第四个α残基。'''
        rPDB = readPDB(self.dsspID)
        residueCount = rPDB.residuesCount()
        ids = []
        for id in residueCount:
            ids.append(id)
        idCount = 0
        idtmp = 0
        with open(self.__dsspFile, mode='r') as dF:
            aHelix = deque()
            tmp = []
            idCount = 0
            for line in dF.readlines():

                line = line.split(" ")
                if "H" not in line:
                    if tmp != []:
                        # if tmp[1]-tmp[0]>6:
                        tmp[0] -= 1
                        tmp[1] -= 1
                        aHelix.append(tmp)
                        tmp = []
                    continue

                for _ in range(len(line)):
                    if '' in line:
                        line.remove('')
                    else:
                        break

                if line[4] == 'H':
                    if line[2] in ids:
                        ids.remove(line[2])
                        idCount = idtmp
                        idtmp = residueCount[line[2]]

                    if len(tmp) < 2:
                        tmp.append(int(line[1])+idCount)

                    elif len(tmp) == 2:
                        tmp[1] = int(line[1])+idCount

        aHelix = list(aHelix)
        # print(aHelix)
        return aHelix

    def aHelixRange(self):
        '''返回range列表.'''
        aHRange = []
        rangeList = self.getAHelix()
        for i in rangeList:
            aHRange.append(range(i[0], i[1]+1))
        return aHRange


if __name__ == '__main__':
    dR = readDSSP('6vw1')
    print(dR.getAHelix())
    print(dR.aHelixRange())
