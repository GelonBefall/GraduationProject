from src.doMat.matrixMaker import makeMatrix
from src.operateOfSQL.sqlOperater import sqlOP
from src.doMat.disPNGMaker import makeDisPNG


class matrixExecute:
    def __init__(self, pdbID: str, database='atomdistance'):
        self.pdbID = pdbID.lower()
        self.database = database

        self.mkMat = makeMatrix(pdbID=self.pdbID)
        self.mkPNG = makeDisPNG()

    def checkSQL(self, sql):
        CACount = self.mkMat.CAAmount
        # sql = sqlOP(pdbID=self.pdbID, database=self.database)
        entryCount = sql.entryAmount
        # sql.db.close()
        if CACount == entryCount:
            return 0
        else:
            return 1

    def loadMat(self, overWrite):
        sql = sqlOP(pdbID=self.pdbID, database=self.database)
        isTableExist = sql.tableExist()
        if isTableExist == 1:
            self.mkMat.calMatrix()
            if self.mkMat.CAAmount <= 10:
                return False
            sql.saveToDB(self.mkMat.disMatrix, overWrite)
            sql.db.close()
            return self.mkMat.disMatrix

        else:
            checkRes = self.checkSQL(sql)
            if checkRes == 0:
                disMatrix = sql.loadFrDB()
                sql.db.close()
                return disMatrix
            else:
                self.mkMat.calMatrix()
                # disMatrix=self.mkMat.disMatrix
                return self.mkMat.disMatrix

    def LASMat(self, overWrite=False):
        '''LAS means load and save the matrix to database.
           If overWrite==False, Production will drop the table of database first.'''
        # sql = sqlOP(pdbID=self.pdbID, database=self.database)
        disMatrix = self.loadMat(overWrite)
        if type(disMatrix) == bool:
            return False
        # sql.saveToDB(disMatrix, overWrite=overWrite)
        # sql.db.close()

        return disMatrix

    def doDisPNG(self):
        # sql = sqlOP(pdbID=self.pdbID, database=self.database)
        disMatrix = self.loadMat(False)
        # sql.db.close()
        # clrmaps = self.mkPNG.colormaps
        grayMat = self.mkPNG.grayMatrix(
            disMatrix=disMatrix, matLen=self.mkMat.CAAmount)
        stutus=self.mkPNG.disPlot(grayMat, self.mkMat.CAAmount, self.pdbID)
        if stutus==0:
            print('已生成过{}的灰度矩阵图，已自动跳过。'.format(self.pdbID))

        return grayMat

    def loadGrayMat(self):
        # grayMat=self.mkPNG.loadGrayMat(self.pdbID)
        try:
            return self.mkPNG.loadGrayMat(self.pdbID)
        except:
            return self.doDisPNG()
             


if __name__ == '__main__':
    matEXE = matrixExecute(pdbID='1a4f')  # pdbID='1a4f'
    # print(op.createTable())
    # print(op.saveToDB())
    # print(matEXE.LASMat())
    # print(matEXE.doDisPNG())
    print(matEXE.loadGrayMat())
