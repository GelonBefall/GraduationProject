from src.doMat import matrixExecute
from src.funcs.dsspReader import readDSSP
from src.funcs.pickleOperater import pickleOP

from copyreg import pickle
from collections import deque

import numpy


class diaStep:
    def __init__(self, pdbID: str, overWrite=False):
        '''遍历矩阵中平行对角线的所有斜线上的Cα原子坐标。'''
        self.pdbID = pdbID.lower()

        self.mE = matrixExecute(self.pdbID)
        self.disMatrix = self.mE.LASMat(overWrite=overWrite)
        if type(self.disMatrix) == bool:
            return None

        self.dR = readDSSP(self.pdbID)
        self.pickle = pickleOP()
        self.aR = self.dR.getAHelix()

        self.clrMaps = self.mE.mkPNG.colormaps  # mkPNG.colormaps
        
        self.CAAmount = self.mE.mkMat.CAAmount
        self.steps = [x for x in range(1, 5)]

    def stepDiaLine(self, step: int):
        '''提取dssp中，所有α螺旋所在结构中，两个隔step个Cα残基的Cα残基之间的距离。'''
        diaLine = {}
        # aHR = dR.aHelixRange()
        for r in range(len(self.aR)):
            # 遍历所有α螺旋区段.

            if 6 >= (self.aR[r][1]-self.aR[r][0]):
                # 若step值 or 6大于该区段长度，跳过
                continue

            lineTmp = deque()
            for row in range(self.aR[r][0], self.aR[r][1]-step+1):
                # 遍历的是第r个区段.
                col = row+step
                lineTmp.append(self.disMatrix[row][col])

            diaLine[tuple(self.aR[r])] = numpy.array(lineTmp)
        return diaLine

    def stepDiaLines(self):
        diaLines = {}
        for step in self.steps:
            diaLine = self.stepDiaLine(step)
            if not bool(diaLine):
                break
            else:
                diaLines[step] = diaLine
        return diaLines

    def stepClrDiaLine(self, step: int, choosenAreas, grayMat):
        '''遍历灰度矩阵'''
        choosenArea = []

        # print(choosenAreas)
        for area in choosenAreas:
            start = area[0]
            end = area[0]
            for row in range(area[0], area[1]-step+1):
                # 遍历该step线, 连续七个以上距离相同的残基添加入同一组中，作为α螺旋候选。
                if row < start:
                    continue
                col = row+step
                if step in self.mE.mkPNG.getMyChecks(grayMat[row][col]):
                    continue
                else:
                    end = col - 1
                    if (end-start) > 7:
                        choosenArea.append((start, end))
                    start = col+1
            if (col-start) > 7:
                choosenArea.append((start, col))  # 结尾处理

        return choosenArea

    def stepClrDiaLines(self, overWrite=False):
        steps = [1, 2, 3]
        pickleName = self.pdbID+"_chosenArea"
        try:
            choosenAreas = self.pickle.loadPickle(pickleName)
            if (bool(choosenAreas)) and (overWrite == False):
                return choosenAreas
            else:
                raise print('pickle存储为空或程序为覆盖写模式。')
        except:
            grayMat = self.mE.mkPNG.grayMatrix(self.disMatrix, self.CAAmount)
            choosenAreas = [(0, self.CAAmount-1)]
        for step in steps:
            choosenAreas = self.stepClrDiaLine(step, choosenAreas, grayMat)

        self.pickle.savePickle(choosenAreas, pickleName, overWrite=overWrite)
        return choosenAreas


if __name__ == '__main__':
    dS = diaStep('1a4f',)  # True
    print(dS.stepClrDiaLines(overWrite=True))
    # print(dS.disMatDiaLines())
