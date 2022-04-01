from copyreg import pickle
# from src.doMat.matrixMaker import makeMatrix
# from src.funcs.pngMaker import makePNG
from src.doMat import matrixExecute
from src.funcs.dsspReader import readDSSP
from src.funcs.pickleOperater import pickleOP
# from src.funcs.listModer import listMode

from collections import deque
import numpy


class diaStep:
    def __init__(self, pdbID='1a4f'):
        '''When the step=0, the program will return 0.'''
        self.pdbID = pdbID.lower()
        # sample
        # mkPNG = makePNG()
        # mM = makeMatrix(self.pdbID)
        # dR=readDSSP(pdbID)
        mE = matrixExecute(self.pdbID)

        self.pickle = pickleOP()

        self.clrMaps = mE.mkPNG.colormaps  # mkPNG.colormaps
        self.disMatrix = mE.LASMat()
        self.clrMat = mE.mkMat.grayMatrix(self.disMatrix, self.clrMaps)
        self.CAAmount = mE.mkMat.CAAmount
        # self.residuesCount=mM.residuesCount()
        self.steps = [x for x in range(1, 6)]

    def stepAHelixDiaLine(self, step: int):
        '''提取dssp中，所有α螺旋所在结构中，每step个α残基之间的距离。'''
        dR = readDSSP(self.pdbID)

        diaLine = {}
        aR = dR.getAHelix()
        # aHR = dR.aHelixRange()
        for r in range(len(aR)):
            # 遍历所有α螺旋区段.

            if step >= (aR[r][1]-aR[r][0]):
                # step值大于该区段长度
                continue

            lineTmp = deque()
            for row in range(aR[r][0], aR[r][1]-step):
                # 遍历的是第r个区段.
                col = row+step
                lineTmp.append(self.disMatrix[row][col])

            diaLine[tuple(aR[r])] = numpy.array(lineTmp)
        return diaLine

    def stepAHelixDiaLines(self):
        diaLines = {}
        for step in self.steps:
            diaLine = self.stepAHelixDiaLine(step)
            if not bool(diaLine):
                break
            else:
                diaLines[step] = diaLine
        return diaLines

    def stepClrDiaLine(self, step: int, choosenAreas):
        choosenArea = deque()
        print(choosenAreas)
        for area in choosenAreas:
            if 4 <= area[1]-area[0] < step:
                choosenArea.append(area)
                continue
            areaTemp = []
            temp = None
            for col in range(area[0], area[1]-step):
                # 遍历该step线, 连续四个以上距离相同的残基添加入同一组中，作为α螺旋候选。
                row = col+step

                if len(areaTemp) == 0:
                    temp = self.clrMat[col][row]
                    areaTemp.append(col)

                elif len(areaTemp) == 1:
                    if all(temp == self.clrMat[col][row]):
                        areaTemp.append(col)
                    else:
                        areaTemp[0] = col
                        temp = self.clrMat[col][row]

                elif 1 <= (areaTemp[1]-areaTemp[0]) < 4:
                    if all(temp == self.clrMat[col][row]):
                        areaTemp[1] = col
                    else:
                        areaTemp.clear()
                        temp = self.clrMat[col][row]
                        areaTemp.append(col)
                else:
                    if all(temp == self.clrMat[col][row]):
                        areaTemp[1] = row
                    else:
                        areaTemp[1] += 1
                        choosenArea.append(areaTemp)
                        areaTemp = []
                        temp = self.clrMat[col][col+step]
                        areaTemp.append(col)
            if (len(areaTemp) == 2) and ((areaTemp[1]-areaTemp[0]) >= 4):
                areaTemp[1] += 1
                choosenArea.append(areaTemp)
                areaTemp = []

        choosenArea = list(choosenArea)
        return choosenArea

    def stepClrDiaLines(self):
        # pickleName = self.pdbID+"_DiaLines"
        # try:
        #     diaLines = self.pickle.loadPickle(pickleName)
        #     return diaLines
        # except:
        choosenAreas = [[0, self.CAAmount]]
        for step in self.steps:
            if step >= 40:
                break
            choosenAreas = self.stepClrDiaLine(step, choosenAreas)

        # self.pickle.savePickle(diaLines, pickleName)
        return choosenAreas

    def clrAHelixDiaLine(self, step: int):
        # diaLine={}
        lineTmp = deque()
        for row in range(self.CAAmount-step):
            col = step+row
            lineTmp.append(self.clrMat[row][col])

        diaLine = numpy.array((lineTmp))
        # return len(diaLine[step])
        return diaLine


if __name__ == '__main__':
    dS = diaStep()
    print(dS.stepClrDiaLines())
    # print(dS.disMatDiaLines())
