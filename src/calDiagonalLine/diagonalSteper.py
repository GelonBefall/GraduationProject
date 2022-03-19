from copyreg import pickle
from src.MatrixAndPNG.matrixMaker import makeMatrix
from src.MatrixAndPNG.pngMaker import makePNG
from src.MatrixAndPNG import matrixExecute
from src.funcs.dsspReader import dsspRead
from src.funcs.pickleOperater import pickleOP
from src.funcs.listModer import listMode

from collections import deque
import numpy
import os

class diaStep:
    def __init__(self, steps:list=[0], pdbID='1a4f'):
        '''When the step=0, the program will return 0.'''
        self.steps=steps
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

    def featureExtract(self):
        lM=listMode()
        for step in self.steps:

    
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
            # diaLine[str(tuple(aR[r]))]=list(lineTmp)
        return diaLine

    def stepclrMatDiaLine(self, step:int):
        # diaLine={}
        lineTmp=deque()
        for row in range(self.CAAmount-step):
            col=step+row
            lineTmp.append(self.clrMat[row][col])
            
        diaLine=numpy.array((lineTmp))
        # return len(diaLine[step])
        return diaLine

    def disMatDiaLines(self):
        pickleName=self.pdbID+"_MatDiaLines"
        try:
            diaLines=self.pickle.loadPickle(pickleName)
            return diaLines
        except:
            diaLines={}
            for step in self.steps:
                diaLines[step]=self.stepdisMatDiaLine(step)
            # jsonName=self.pdbID+"_MatDiaLines"+".json"
            
            self.pickle.savePickle(diaLines, pickleName)
            return diaLines

if __name__=='__main__':
    dS=diaStep(steps=[1,2,3])
    # print(dS.stepDiaLine(1))
    print(dS.disMatDiaLines())