from src.doMatPNG.matrixMaker import makeMatrix
from src.operateOfSQL.sqlOperater import sqlOP
from src.doMatPNG.pngMaker import makePNG


class matrixExecute:
    def __init__(self, pdbID='1a4f', database='atomdistance'):
        self.pdbID = pdbID.lower()
        self.database = database

        self.mkMat = makeMatrix(pdbID=self.pdbID)
        self.mkPNG = makePNG(colorFilename="gray.rgb")

    def checkSQL(self):
        CACount = self.mkMat.CAAmount
        sql = sqlOP(pdbID=self.pdbID, database=self.database)
        entryCount = sql.entryAmount
        sql.db.close()
        if CACount == entryCount:
            return 0
        else:
            return 1

    def saveMat(self, disMatrix):
        sql = sqlOP(pdbID=self.pdbID, database=self.database)
        sql.saveToDB(disMatrix)
        sql.db.close()

    def loadMat(self):
        sql = sqlOP(pdbID=self.pdbID, database=self.database)
        isTableExist = sql.tableExist()
        if isTableExist == 1:
            self.mkMat.calMatrix()
            # disMatrix=self.mkMat.disMatrix
            sql.db.close()
            return self.mkMat.disMatrix

        else:
            checkRes = self.checkSQL()
            if checkRes == 0:
                disMatrix = sql.loadFrDB()
                sql.db.close()
                return disMatrix
            else:
                self.mkMat.calMatrix()
                # disMatrix=self.mkMat.disMatrix
                return self.mkMat.disMatrix

    def LASMat(self, dropMode=False):
        '''LAS means load and save the matrix to database.
           If dropMode==False, Production will drop the table of database first.'''

        if dropMode == True:
            sql = sqlOP(pdbID=self.pdbID, database=self.database)
            sql.dropTable()
            sql.db.close()
        disMatrix = self.loadMat()
        self.saveMat(disMatrix)
        return disMatrix

    def mkGrayPNG(self):
        disMatrix = self.loadMat()
        clrmaps = self.mkPNG.colormaps
        clrMat = self.mkMat.grayMatrix(disMatrix, clrmaps)
        self.mkPNG.pngPlot(clrMat, self.mkMat.CAAmount, self.pdbID)
        return clrMat


if __name__ == '__main__':
    matEXE = matrixExecute()  # default pdbID='6vw1'
    # print(op.createTable())
    # print(op.saveToDB())
    # print(matEXE.LASMat())
    print(matEXE.mkGrayPNG())
