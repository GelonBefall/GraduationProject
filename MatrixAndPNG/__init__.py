# import sys
# import numpy as np

from matrixMaker import makeMatrix
from sqlOperate import sqlOP
from pngMaker import makePNG


class matrixExecute:
    def __init__(self, pdbID='2erk', database='atomdistance'):
        self.pdbID=pdbID
        self.sql=sqlOP(pdbID=self.pdbID, database=database)
        self.mkMat=makeMatrix(pdbID=self.pdbID)
        self.mkPNG=makePNG(colorFilename="gray.rgb")

    def checkSQL(self):
        CACount=self.mkMat.CAAmount
        entryCount = self.sql.entryAmount
        if CACount==entryCount:
            return 0
        else:
            return 1

    def saveMat(self,disMatrix):
        self.sql.saveToDB(disMatrix)

    def loadMat(self):
        isTableExist=self.sql.tableExist()
        if isTableExist == 1:
            self.mkMat.calMatrix()
            # disMatrix=self.mkMat.disMatrix
            return self.mkMat.disMatrix

        else:
            checkRes=self.checkSQL()
            if checkRes==0:
                disMatrix=self.sql.loadFrDB()
                return disMatrix
            else:
                self.mkMat.calMatrix()
                # disMatrix=self.mkMat.disMatrix
                return self.mkMat.disMatrix

    def LASMat(self, dropMode=False):
        '''LAS means load martix and save the matrix to database.
           If dropMode==False, Production will drop the table of database first.'''
        if dropMode==True:
            self.sql.dropTable()
        disMatrix=self.loadMat()
        self.saveMat(disMatrix)
        return disMatrix

    def mkGrayPNG(self):
        disMatrix=self.loadMat()
        clrmaps=self.mkPNG.colormaps
        clrMat=self.mkMat.grayMatrix(disMatrix,clrmaps)
        self.mkPNG.pngPlot(clrMat, self.mkMat.CAAmount, self.pdbID)

    
        
if __name__ == '__main__':
    matEXE = matrixExecute() # pdbID='6vw1'
    # print(op.createTable())
    # print(op.saveToDB())
    # print(matEXE.LASMat())
    print(matEXE.mkGrayPNG())
