import os
import sys
from collections import deque
from pathlib import Path

from src.funcs.pdbReader import readPDB


class readDSSP:
    def __init__(self, pdbID: str, dsspPath=None):
        self.dsspID = pdbID.lower()

        if dsspPath:
            self.__dsspPath = dsspPath
        else:
            self.__dsspPath = self.__dsspFinder()

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

    def __dsspFinder(self):
        __dsspPath = "./materials/dssp/"
        dsspPath = Path(__dsspPath)
        dsspFile = self.dsspID+'.dssp'

        result = list(dsspPath.rglob(dsspFile))

        dsspPath = __dsspPath+result[0]._cparts[2]
        return dsspPath

    def dsspDeleter(self):
        os.remove(self.__dsspFile)
        print("已成功删除{}的dssp文件！".format(self.dsspID))

    def getAHelix(self):
        '''返回α螺旋位置，下标从0开始。例如[1, 3]为第二个到第四个α残基。'''
        rPDB = readPDB(self.dsspID)
        residueCount = rPDB.residuesCount()
        ids = list(residueCount.keys())  # 收集链ID

        idCount = 0
        idtmp = 0

        with open(self.__dsspFile, mode='r') as dF:
            aHelix = deque()
            tmp = []
            idCount = 0

            for line in dF.readlines():
                # 逐行读取dssp文件，line存储每行所有内容
                line = line.split(" ")

                # 如果某一行没有"H"标识，查看tmp是否已经暂存了α螺旋范围。
                if "H" not in line:
                    if len(tmp) == 2:
                        # if tmp[1]-tmp[0]>6:
                        tmp[0] -= 1
                        tmp[1] -= 1
                        if tmp[1] <= tmp[0] or tmp[1] >= rPDB.CAAmount:
                            return []
                        else:
                            for a in aHelix:
                                if tmp[0] <= a[1]:
                                    return []
                        aHelix.append(tmp)  # 将暂存范围存入结果
                        tmp = []
                    continue

                for _ in range(len(line)):
                    if '' in line:
                        line.remove('')
                    else:
                        break

                if line[4] == 'H':
                    if line[2] in ids:

                        ids.remove(line[2])  # 去除该chain ID
                        idCount += idtmp  # 读取上一条chain的Cα原子数量
                        idtmp = residueCount[line[2]]  # 将本chain的Cα原子数量读入暂存

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
    dR = readDSSP('1a0n')
    print(dR.getAHelix())
    # print(dR.aHelixRange())
    # print(dR.dsspFinder())
