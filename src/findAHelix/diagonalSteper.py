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
        if type(self.disMatrix) != bool and self.mE.mkMat.CAAmount >= 800:
            print('该蛋白过大，已自动跳过并即将转移pdb文件及dssp文件。')
            return False
        elif type(self.disMatrix) == bool or self.aR == [] or self.CAAmount <= self.aR[-1][-1]:
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

            if 5 >= (self.aR[r][1]-self.aR[r][0]):
                # 若step值 or 5大于该区段长度，跳过
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
            row=area[0]
            while row<area[1]-step+1:
                # 遍历该step线, 连续5个以上距离相同的残基添加入同一组中，作为α螺旋候选。
                # if row < start:
                #     continue
                col = row+step

                if step in self.mE.mkPNG.getMyChecks(grayMat[row][col]):
                    row += 1
                else:
                    # end = row - 1
                    end = col - 2
                    if (end-start) >= 4:
                        # end = col - 1
                        choosenArea.append((start, end))
                    start = col
                    row = start

            if (col-start) >= 4:
                choosenArea.append((start, col))  # 结尾处理

        return choosenArea

    def stepClrDiaLine2(self, step: int, choosenAreas, grayMat):
        '''遍历灰度矩阵算法2.0'''
        choosenArea = []

        # print(choosenAreas)
        for area in choosenAreas:
            start = area[0]
            end = area[0]
            row=area[0]
            while row<area[1]-step+1:
                # 遍历该step线, 连续5个以上距离相同的残基添加入同一组中，作为α螺旋候选。
                # if row < start:
                #     continue
                col = row+step

                if step in self.mE.mkPNG.getMyChecks(grayMat[row][col]):
                    row+=1
                else:
                    # end = row - 1
                    end = col -1
                    if (end-start) >= 4:
                        # end = col - 1
                        choosenArea.append((start, end))
                        start = end-2
                        row = start
                    else:
                        start=end-1
                        row+=1

            if (col-start) >= 4:
                choosenArea.append((start, col))  # 结尾处理
        if len(choosenArea)>1:
            i=0
            tmp=list(choosenArea[0])
            tmps=[]
            while i<=len(choosenArea)-2:
                if tmp[1]>=choosenArea[i+1][0]:
                    tmp[1]=choosenArea[i+1][1]
                else:
                    tmps.append(tuple(tmp))
                    tmp=list(choosenArea[i+1])
                i+=1
            tmps.append(tuple(tmp))
            choosenArea=tmps
        return choosenArea

    def stepClrDiaLines1(self, overWrite=False) -> list:
        steps = [1, 2, 3]
        pickleName = self.pdbID+"_chosenArea1"
        try:
            choosenAreas = self.pickle.loadPickle(pickleName)
            if (bool(choosenAreas)) and (overWrite == False):
                return choosenAreas
            else:
                print('pickle存储为空或程序为覆盖写模式。')
                raise
        except:
            # grayMat = self.mE.mkPNG.grayMatrix(self.disMatrix, self.CAAmount)
            grayMat = self.mE.grayMat
            choosenAreas = [(0, self.CAAmount-1)]
        # tmp = choosenAreas
        for step in steps:
            choosenAreas = self.stepClrDiaLine1(step, choosenAreas, grayMat)
            if choosenAreas==[]:
                choosenAreas=tmp
            else:
                tmp=choosenAreas

        self.pickle.savePickle(choosenAreas, pickleName, overWrite=overWrite)
        return choosenAreas

    def stepClrDiaLines2(self, overWrite=False) -> list:
        steps = [1, 2, 3, 4]
        pickleName = self.pdbID+"_chosenArea2"
        try:
            choosenAreas = self.pickle.loadPickle(pickleName)
            if (bool(choosenAreas)) and (overWrite == False):
                return choosenAreas
            else:
                print('pickle存储为空或程序为覆盖写模式。')
                raise
        except:
            # grayMat = self.mE.mkPNG.grayMatrix(self.disMatrix, self.CAAmount)
            grayMat = self.mE.grayMat
            choosenAreas = [(0, self.CAAmount-1)]
        tmp = choosenAreas
        for step in steps:
            choosenAreas = self.stepClrDiaLine2(step, choosenAreas, grayMat)
            if choosenAreas==[]:
                choosenAreas=tmp
            else:
                tmp=choosenAreas
        self.pickle.savePickle(choosenAreas, pickleName, overWrite=overWrite)
        return choosenAreas


if __name__ == '__main__':
    dS = diaStep('1b55',)  # True
    print(dS.aR)
    print(dS.stepClrDiaLines1(overWrite=True))
    print(dS.stepClrDiaLines2(overWrite=True))
    # print(dS.stepDiaLines())
