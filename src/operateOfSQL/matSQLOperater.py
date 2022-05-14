import sys
import numpy

from collections import deque
from src.operateOfSQL import sqlOP


class matSQLOP(sqlOP):

    def createTable(self, matrixLen):
        # Create new table.
        if matrixLen > 800:
            return 0
        tableCreateSQL = "CREATE TABLE pdb_{}(".format(self.pdbID)
        for i in range(matrixLen-1):
            tableCreateSQL = tableCreateSQL + 'Col{} DOUBLE,'.format(i)
        tableCreateSQL = tableCreateSQL + \
            'Col{} DOUBLE)'.format(matrixLen-1)

        try:
            self.cursor.execute(tableCreateSQL)
            self.db.commit()
            return 0
        except:
            self.db.rollback()
            print("CREATE TABLE OF {} ERROR.".format(self.database))
            sys.exit()

    def loadFrDB(self):
        selectSQL = 'SELECT * FROM pdb_{}'.format(self.pdbID)
        try:
            disLists = deque()
            self.cursor.execute(selectSQL)
            data = self.cursor.fetchall()
            for line in data:
                tmpDis = list(line)
                disLists.append(tmpDis)

            disMatrix = numpy.array(disLists)
            # print(len(disMatrix))
            return disMatrix
        except:
            print("Fail to load from database {}. please check it! ".format(
                self.database))
            sys.exit()

    def saveDisMatrix(self, disMatrix, matrixLen):
        # Preparation for inserting.
        insertPre = 'INSERT INTO pdb_{}'.format(self.pdbID)+" VALUES "
        tmp = 0

        # Insert data.
        i = 0
        while i < matrixLen:
            if tmp == 5:
                print("INSERT DATA IN {} ERROR".format(self.database))
                sys.exit()
            insertSQL = insertPre + str(tuple(disMatrix[i]))
            try:
                self.cursor.execute(insertSQL)
                self.db.commit()
                i = i+1
                tmp = 0
            except:
                self.db.rollback()
                i = i-1
                tmp = tmp+1

        print("Save disMatrix of atom's distance to DB successfully.")
        return 0

    def saveToDB(self, disMatrix, overWrite=False):
        isExist = self.tableExist()
        matrixLen = len(disMatrix)
        if isExist == True:

            if (self.entryAmount == matrixLen) and (overWrite == False):
                print("You have saved the matrix in {}. pdb_{}. Do not execute again.".format(
                    self.database, self.pdbID))

            elif self.entryAmount == 0:
                self.saveDisMatrix(disMatrix, matrixLen)

            elif self.entryAmount == -1:
                self.createTable(matrixLen)
                self.saveDisMatrix(disMatrix, matrixLen)

            else:
                self.dropTable()
                self.createTable(matrixLen)
                self.saveDisMatrix(disMatrix, matrixLen)
        else:
            self.createTable(matrixLen)
            self.saveDisMatrix(disMatrix, matrixLen)
        return 0
