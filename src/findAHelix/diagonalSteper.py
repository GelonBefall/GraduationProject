from src.doMat import matrixExecute
from src.funcs.dsspReader import readDSSP
from src.funcs.pickleOperater import pickleOP


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
        if type(self.disMatrix) != bool and self.disMatrix.shape[0] >= 1000:
            print('该蛋白过大，已自动跳过并即将转移pdb文件及dssp文件。')
            return False
        elif type(self.disMatrix) == bool or self.aR == [] or self.CAAmount < self.aR[-1][-1]:
            print('该蛋白DSSP或PDB文件错误，或该蛋白没有Cα原子或α螺旋，已自动跳过并即将删除该文件。')
            return False
        else:
            return True

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
                print('pickle存储为空或程序为覆盖写模式。')
                raise
        except:
            # grayMat = self.mE.mkPNG.grayMatrix(self.disMatrix, self.CAAmount)
            grayMat = self.mE.loadGrayMat()
            choosenAreas = [(0, self.CAAmount-1)]
        for step in steps:
            choosenAreas = self.stepClrDiaLine(step, choosenAreas, grayMat)

        self.pickle.savePickle(choosenAreas, pickleName, overWrite=overWrite)
        return choosenAreas


if __name__ == '__main__':
    dS = diaStep('117e',)  # True
    print(dS.stepClrDiaLines(overWrite=True))
    # print(dS.disMatDiaLines())
