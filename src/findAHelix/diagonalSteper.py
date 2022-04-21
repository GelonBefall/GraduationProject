import numpy

from src.doMat import matrixExecute
from src.funcs.dsspReader import readDSSP
from src.funcs.pickleOperater import pickleOP

from collections import deque


class diaStep:
    def __init__(self, pdbID: str, overWrite=False, dsspPath=None):
        '''遍历矩阵中平行对角线的所有斜线上的Cα原子坐标。'''
        self.pdbID = pdbID.lower()

        self.mE = matrixExecute(self.pdbID)
        self.disMatrix = self.mE.LASMat(overWrite=overWrite)

        self.dR = readDSSP(self.pdbID, dsspPath)
        self.aR = self.dR.getAHelix()
        self.CAAmount = self.mE.mkMat.CAAmount
        if self.__bool__ == False:
            return None

        self.pickle = pickleOP()
        self.clrMaps = self.mE.mkPNG.colormaps  # mkPNG.colormaps

    def __bool__(self):
        if type(self.disMatrix) != bool and self.mE.mkMat.CAAmount >= 1000:
            print('该蛋白过大，已自动跳过并即将转移pdb文件及dssp文件。')
            return False
        elif type(self.disMatrix) == bool or self.aR == [] or self.CAAmount < self.aR[-1][-1]:
            print('该蛋白DSSP或PDB文件错误，或该蛋白没有Cα原子或α螺旋，已自动跳过并即将删除该文件。')
            return False
        else:
            return True

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
        steps = [1, 2, 3]
        for step in steps:
            diaLine = self.stepDiaLine(step)
            if not bool(diaLine):
                break
            else:
                diaLines[step] = diaLine
        return diaLines

    def stepClrDiaLine1(self, step: int, choosenAreas, grayMat):
        '''遍历灰度矩阵算法1.0'''
        choosenArea = []

        # print(choosenAreas)
        for area in choosenAreas:
            start = area[0]
            end = area[0]
            for row in range(area[0], area[1]-step+1):
                # 遍历该step线, 连续5个以上距离相同的残基添加入同一组中，作为α螺旋候选。
                if row < start:
                    continue
                col = row+step

                if step in self.mE.mkPNG.getMyChecks(grayMat[row][col]):
                    continue
                else:
                    # end = row - 1
                    end = col - 1
                    if (end-start) >= 5:
                        # end = col - 1
                        choosenArea.append((start, end))
                    start = col+1

            if (col-start) >= 5:
                choosenArea.append((start, col))  # 结尾处理

        return choosenArea

    def stepClrDiaLine2(self, step: int, choosenAreas, grayMat):
        '''遍历灰度矩阵算法2.0'''
        choosenArea = []

        # print(choosenAreas)
        for area in choosenAreas:

            length = 0
            notChoosenArea = []
            for row in range(area[0], area[1]-step+1):
                # 遍历该step线, 如果是两个以内距离不同的残基，可以视作α螺旋内。
                # if row<
                col = row + step

                if step not in self.mE.mkPNG.getMyChecks(grayMat[row][col]):
                    if length == 0:
                        start = row
                    else:
                        end = row
                    length += 1
                else:
                    if length > 2:
                        notChoosenArea.append((start, end))
                        length = 0
                    else:
                        length = 0

            start = area[0]
            end = area[1]
            if len(notChoosenArea) != 0:
                for notArea in notChoosenArea:
                    head = start
                    tail = notArea[0]-1

                    if tail <= head:
                        start = notArea[1]+1
                        continue

                    else:
                        if (tail-head) > 7:
                            choosenArea.append((head, tail))
                            start = notArea[1]+1
                if (end-start) > 7:
                    choosenArea.append((start, end))

            else:
                choosenArea.append(area)

        return choosenArea

    def stepClrDiaLines(self, overWrite=False):
        steps = [1, 2, 3]
        pickleName = self.pdbID+"_chosenArea"
        try:
            choosenAreas = self.pickle.loadPickle(pickleName)
            if (bool(choosenAreas)) and (overWrite == False):
                return choosenAreas
            else:
                print('pickle存储为空或程序为覆盖写模式。')
                raise
        except:
            # grayMat = self.mE.mkPNG.grayMatrix(self.disMatrix, self.CAAmount)
            grayMat = self.mE.loadGrayMat()
            choosenAreas = [(0, self.CAAmount-1)]
        for step in steps:
            choosenAreas = self.stepClrDiaLine1(step, choosenAreas, grayMat)

        self.pickle.savePickle(choosenAreas, pickleName, overWrite=overWrite)
        return choosenAreas


if __name__ == '__main__':
    dS = diaStep('12ca',)  # True
    print(dS.stepClrDiaLines(overWrite=True))
    # print(dS.disMatDiaLines())
