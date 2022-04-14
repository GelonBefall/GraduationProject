import pymysql
import os
import sys
import numpy as np

from collections import deque

from turtle import distance
from attr import field
from pydoc import describe
from soupsieve import select


class sqlOP:
    '''The username and password of MySQL are needed from Envionment Variables.
       user's key is "SQLUSER", password's is "SQLPSWD". 
       Attention: You need to restart you PC to make new Envionment Variables available.'''

    def __init__(self, pdbID, database):
        # You need to set which database you will use.
        user = os.environ.get('SQLUSER')
        password = os.environ.get('SQLPSWD')

        self.option = database
        self.pdbID = pdbID

        # 打开数据库连接
        self.db = pymysql.connect(host='127.0.0.1',
                                  user=user,
                                  password=password,
                                  database=database,
                                  charset='utf8')
        self.cursor = self.db.cursor()

        self.entryAmount = self.entryCount()

    def tableExist(self):
        try:
            describeSQL = "DESCRIBE pdb_{}".format(self.pdbID)
            self.cursor.execute(describeSQL)
            return 0
        except:
            return 1

    def entryCount(self):
        try:
            isEmptySQL = 'SELECT COUNT(1) FROM pdb_{}'.format(self.pdbID)
            self.cursor.execute(isEmptySQL)
            data = self.cursor.fetchone()
            print("The entrys you have saved is {}".format(data[0]))
            return data[0]
        except:
            print("Cant found the table.")
            return -1

    def dropTable(self):
        try:
            deleteTableSQL = "DROP TABLE pdb_{}".format(self.pdbID)
            self.cursor.execute(deleteTableSQL)
            self.db.commit()
            print("DROP TABLE SUCCESSFULLY.")
            return 0
        except:
            self.db.rollback()
            print("DROP TABLE ERROR, please check your database.")
            sys.exit()

    def createTable(self, matrixLen):
        # Create new table.
        tableCreateSQL = "CREATE TABLE pdb_{}(".format(self.pdbID)
        if self.option == 'atomdistance':
            for i in range(matrixLen-1):
                tableCreateSQL = tableCreateSQL + 'Col{} DOUBLE,'.format(i)
            tableCreateSQL = tableCreateSQL + \
                'Col{} DOUBLE)'.format(matrixLen-1)
            if i > 1000:  # Choose MySQL-engine MyISAM.
                tableCreateSQL = tableCreateSQL+'engine=MyISAM'

            try:
                self.cursor.execute(tableCreateSQL)
                self.db.commit()
                return 0
            except:
                self.db.rollback()
                print("CREATE TABLE ERROR.")
                sys.exit()

        elif self.option == 'alphaFeatures':
            tableCreateSQL += ' STEP TINYINT(10), ALPHARANGES CHAR(12), STEPMINS DOUBLE, STEPMAXS DOUBLE, DIFFERVALUES FLOAT, MEAN FLOAT, VARIANCE FLOAT)'
            try:
                self.cursor.execute(tableCreateSQL)
                self.db.commit()
                return 0
            except:
                self.db.rollback()
                print("CREATE TABLE ERROR.")
                sys.exit()

    def saveDisMatrix(self, disMatrix, matrixLen):
        # Preparation for inserting.
        insertPre = 'INSERT INTO pdb_{}'.format(self.pdbID)+" VALUES "

        tmp = 0
        if self.option == 'atomdistance':
            # Insert data.
            i = 0
            while i < matrixLen:
                if tmp == 5:
                    print("INSERT ERROR")
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

        elif self.option == 'alphaFeatures':
            # Insert data.
            i = 0
            while i < matrixLen:
                if tmp == 5:
                    print("INSERT ERROR")
                    sys.exit()
                disMatrix[i][1] = str(disMatrix[i][1])
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

        print("SAVE TO DB SUCCESSFULLY.")

    def saveToDB(self, disMatrix, overWrite=False):
        isExist = self.tableExist()
        matrixLen = len(disMatrix)
        if isExist == 0:

            if (self.entryAmount == matrixLen) and (overWrite == False):
                print("You have saved the matrix in {}. {}. Do not execute again.".format(
                    self.option,self.pdbID))
                return 0

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

    def loadFrDB(self):
        selectSQL = 'SELECT * FROM pdb_{}'.format(self.pdbID)
        if self.option == 'atomdistance':
            try:
                disLists = deque()
                self.cursor.execute(selectSQL)
                data = self.cursor.fetchall()
                for line in data:
                    tmpDis = list(line)
                    disLists.append(tmpDis)

                disMatrix = np.array(disLists)
                # print(len(disMatrix))
                return disMatrix
            except:
                print("Fail to load from database. please check it! ")
                sys.exit()
        elif self.option == 'alphaFeatures':
            try:
                alphaFeatures = {}
                self.cursor.execute(selectSQL)
                data = self.cursor.fetchall()
                for i in range(len(data)):
                    line = data[i]
                    line = list(line)
                    step = line[0]
                    aRange = eval(line[1])

                    if step in alphaFeatures:
                        alphaFeatures[step][aRange] = [line[2], line[3]]
                    else:
                        alphaFeatures[step] = {}
                        alphaFeatures[step][aRange] = [line[2], line[3]]

                # print(len(disMatrix))
                return alphaFeatures
            except:
                print("Fail to load from database. please check it! ")
                sys.exit()


if __name__ == '__main__':
    op = sqlOP('2erk')  # pdbID='6vw1'
    # op.dropTable()
    print(op.entryAmount)
    # print(op.createTable())
    # print(op.saveToDB())
    # print(op.loadFrDB())
