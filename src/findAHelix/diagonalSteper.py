from src.doMat import matrixExecute
from src.funcs.dsspReader import readDSSP

from collections import deque
import numpy


class diaStep:
    def __init__(self, pdbID: str, overWrite=False):
        '''遍历矩阵中平行对角线的所有斜线上的Cα原子坐标。'''
        self.pdbID = pdbID.lower()
        mE = matrixExecute(self.pdbID)
        self.dR = readDSSP(self.pdbID)
        self.aR = self.dR.getAHelix()

        self.clrMaps = mE.mkPNG.colormaps  # mkPNG.colormaps
        self.disMatrix = mE.LASMat(overWrite=overWrite)
        self.CAAmount = mE.mkMat.CAAmount
        self.steps = [x for x in range(1, 5)]

    def stepDiaLine(self, step: int):
        '''提取dssp中，所有α螺旋所在结构中，每step个α残基之间的距离。'''
        diaLine = {}
        # aHR = dR.aHelixRange()
        for r in range(len(self.aR)):
            # 遍历所有α螺旋区段.

            if 6 >= (self.aR[r][1]-self.aR[r][0]):
                # 若step值 or 6大于该区段长度，跳过
                continue

            lineTmp = deque()
            for row in range(self.aR[r][0], self.aR[r][1]-step):
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


if __name__ == '__main__':
    dS = diaStep()
    # print(dS.stepClrDiaLines())
    # print(dS.disMatDiaLines())
