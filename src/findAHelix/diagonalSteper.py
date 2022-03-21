from copyreg import pickle
from src.MatrixAndPNG.matrixMaker import makeMatrix
from src.MatrixAndPNG.pngMaker import makePNG
from src.MatrixAndPNG import matrixExecute
from src.funcs.dsspReader import dsspRead
from src.funcs.pickleOperater import pickleOP
# from src.funcs.listModer import listMode

from collections import deque
import numpy

class diaStep:
    def __init__(self, pdbID='1a4f'):
        '''When the step=0, the program will return 0.'''
        
        # sample
        mkPNG=makePNG()
        mE=matrixExecute(pdbID)
        mM=makeMatrix(pdbID)
        # dR=dsspRead(pdbID)
        self.pickle=pickleOP()

        self.pdbID=pdbID
        self.clrMaps=mkPNG.colormaps
        self.disMatrix=mE.LASMat()
        self.clrMat=mM.grayMatrix(self.disMatrix, self.clrMaps)
        self.CAAmount=mM.CAAmount
        self.steps=[x for x in range(1,self.CAAmount)]

    def stepAHelixDiaLine(self,step:int):
        '''提取dssp中，所有α螺旋所在结构中，每n个α残基之间的距离。'''
        dR=dsspRead(self.pdbID)
        
        diaLine={}
        aR=dR.getAHelix()
        aHR=dR.aHelixRange()
        for r in range(len(aR)):
            '''遍历所有α螺旋区段.'''
            lineTmp=deque()
            for row in aHR[r]:
                '''遍历的是该区段.'''
                col=row+step
                if col <= aR[r][1]:
                    lineTmp.append(self.disMatrix[row][col])
                else:
                    break
            if len(lineTmp)==0:
                continue
            else:
                diaLine[tuple(aR[r])]=numpy.array(lineTmp)
            # diaLine[str(tuple(aR[r]))]=list(lineTmp)
        return diaLine

    def stepAHelixDiaLines(self):
        diaLines={}
        for step in self.steps:
            diaLines[step]=self.stepAHelixDiaLine(step)
        return diaLines

    def stepDisDiaLine(self):
        pass
    
    def stepDisDiaLines(self):
        pickleName=self.pdbID+"_DiaLines"
        try:
            diaLines=self.pickle.loadPickle(pickleName)
            return diaLines
        except:
            diaLines={}

            for step in self.steps:
                diaLines[step]=self.stepAHelixDiaLine(step)
        
            self.pickle.savePickle(diaLines, pickleName)
        return diaLines

    def clrAHelixDiaLine(self, step:int):
        # diaLine={}
        lineTmp=deque()
        for row in range(self.CAAmount-step):
            col=step+row
            lineTmp.append(self.clrMat[row][col])
            
        diaLine=numpy.array((lineTmp))
        # return len(diaLine[step])
        return diaLine



if __name__=='__main__':
    dS=diaStep()
    # print(dS.stepDiaLine(1))
    # print(dS.disMatDiaLines())