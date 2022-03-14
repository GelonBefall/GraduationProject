from matplotlib import collections
from src.MatrixAndPNG.matrixMaker import makeMatrix
from src.MatrixAndPNG.pngMaker import makePNG
from src.MatrixAndPNG import matrixExecute
from src.DSSP.dsspReader import dsspRead

from collections import deque
import numpy

class diaStep:
    def __init__(self, steps:list=[0], pdbID='1a4f'):
        '''When the step=0, the program will '''
        self.steps=steps
        # sample
        mkPNG=makePNG()
        mE=matrixExecute(pdbID)
        mM=makeMatrix(pdbID)
        # dR=dsspRead(pdbID)

        self.pdbID=pdbID
        self.clrMaps=mkPNG.colormaps
        self.disMatrix=mE.LASMat()
        self.clrMat=mM.grayMatrix(self.disMatrix, self.clrMaps)
        self.CAAmount=mM.CAAmount

    def stepdisMatDiaLine(self,step:int):
        dR=dsspRead(self.pdbID)
        
        diaLine={}
        aR=dR.getAHelix()
        for r in range(len(aR)):
            lineTmp=deque()
            for row in dR.aHelixRange()[r]:
                col=step+row
                lineTmp.append(self.disMatrix[row][col])
            diaLine[tuple(aR[r])]=numpy.array(lineTmp)
        return diaLine


    def stepclrMatDiaLine(self, step:int):
        diaLine={}
        lineTmp=deque()
        for row in range(self.CAAmount-step):
            col=step+row
            lineTmp.append(self.clrMat[row][col])
            
        diaLine[step]=numpy.array((lineTmp))
        # return len(diaLine[step])
        return diaLine

if __name__=='__main__':
    dS=diaStep()
    # print(dS.stepDiaLine(1))
    print(dS.stepdisMatDiaLine(1))