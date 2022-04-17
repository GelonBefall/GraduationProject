from src.doMat.matrixMaker import makeMatrix
from src.operateOfSQL.matSQLOperater import matSQLOP
from src.doMat.disPNGMaker import makeDisPNG


class matrixExecute:
    def __init__(self, pdbID: str, database='atomdistance'):
        self.pdbID = pdbID.lower()
        self.database = database

        self.mkMat = makeMatrix(pdbID=self.pdbID)
        self.mkPNG = makeDisPNG()

    def dropPDB(self):
        self.mkPNG.pngDeleter(self.pdbID)

        sql = matSQLOP(pdbID=self.pdbID, database=self.database)
        sql.dropTable()
        sql.db.close()

        self.mkMat.pdbDeleter()

    def checkSQL(self, sql: matSQLOP):
        CACount = self.mkMat.CAAmount
        entryCount = sql.entryAmount

        if CACount == entryCount:
            return True
        else:
            return False

    def loadMat(self, overWrite):
        sql = matSQLOP(pdbID=self.pdbID, database=self.database)
        isTableExist = sql.tableExist()
        checkRes = self.checkSQL(sql)

        if isTableExist == False or checkRes == False:

            if self.mkMat.CAAmount == 0:
                return False
            else:
                self.mkMat.calMatrix()
                sql.saveToDB(self.mkMat.disMatrix, overWrite)
                sql.db.close()
                return self.mkMat.disMatrix

        else:
            disMatrix = sql.loadFrDB()
            sql.db.close()
            return disMatrix

    def LASMat(self, overWrite=False):
        '''LAS means load and save the matrix to database.
           If overWrite==False, Production will drop the table of database first.'''
        # sql = matSQLOP(pdbID=self.pdbID, database=self.database)
        disMatrix = self.loadMat(overWrite)
        if type(disMatrix) == bool:
            return False
        # sql.saveToDB(disMatrix, overWrite=overWrite)
        # sql.db.close()

        return disMatrix

    def doDisPNG(self):
        try:
            grayMat = self.mkPNG.loadGrayMat(self.pdbID)
        except:
            disMatrix = self.LASMat(False)

            grayMat = self.mkPNG.newGrayMatrix(
                disMatrix=disMatrix, matLen=self.mkMat.CAAmount)

            stutus = self.mkPNG.disPlot(
                grayMat, self.mkMat.CAAmount, self.pdbID)  # 返回作图之后的状态
            if stutus == 0:
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
