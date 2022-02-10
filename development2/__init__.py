import sys
import numpy as np

from matrixMaker import makeMatrix
from sqlOperate import sqlOP


class matrixExecute:
    def __init__(self, pdbID='2erk', database='atomdistance'):
        self.pdbID=pdbID
        self.sql=sqlOP(pdbID=self.pdbID, database=database)
        self.mkMat=makeMatrix(pdbID=self.pdbID)

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
            disMatrix=self.mkMat.calMatrix()
            return disMatrix

        else:
            checkRes=self.checkSQL()
            if checkRes==0:
                disMatrix=self.sql.loadFrDB()
                return disMatrix
            else:
                disMatrix=self.mkMat.calMatrix()
                return disMatrix

    def LASMatrix(self):
        '''LAS means load martix and save the matrix to database.'''
        disMatrix=self.loadMat()
        self.saveMat(disMatrix)
        return disMatrix
    
    def DLASMatrix(self):
        '''DLAS means drop table first, then load martix and save the matrix to database.'''
        self.sql.dropTable()
        disMatrix=self.loadMat()
        self.saveMat(disMatrix)
        return disMatrix
        
if __name__ == '__main__':
    matEXE = matrixExecute(pdbID='6vw1')
    # print(op.createTable())
    # print(op.saveToDB())
    print(matEXE.DLASMatrix())
