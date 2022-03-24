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

    def __init__(self, pdbID='2erk', database='atomdistance'):
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
            describeSQL = "DESCRIBE {}".format(self.pdbID)
            self.cursor.execute(describeSQL)
            return 0
        except:
            return 1

    def entryCount(self):
        try:
            isEmptySQL = 'SELECT COUNT(1) FROM {}'.format(self.pdbID)
            self.cursor.execute(isEmptySQL)
            data = self.cursor.fetchone()
            print("The entrys you have saved is {}".format(data[0]))
            return data[0]
        except:
            print("Cant found the table.")
            return -1

    def dropTable(self):
        try:
            deleteTableSQL = "DROP TABLE {}".format(self.pdbID)
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
        tableCreateSQL = "CREATE TABLE {}(".format(self.pdbID)
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
            tableCreateSQL += ' RANGE VARSIZE(12), ' + \
                ' MIN DOUBLE, ' + ' MAX DOUBLE )'
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
        insertPre = 'INSERT INTO {}'.format(self.pdbID)+" VALUES "
        i = 0
        tmp = 0
        if self.option == 'atomdistance':
            # Insert data.
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
            while i < matrixLen:
                if tmp == 5:
                    print("INSERT ERROR")
                    sys.exit()
                insertSQL = insertPre + \
                    str(tuple(disMatrix[i][0])) + ', ' + \
                    disMatrix[i][1]+','+disMatrix[i][2]
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

    def saveToDB(self, disMatrix):
        isExist = self.tableExist()
        matrixLen = len(disMatrix)
        if isExist == 0:

            if self.entryAmount == matrixLen:
                print("You have saved the distance matrix. Do not execute again.")
                return 0

            elif self.entryAmount == 0:
                self.saveDisMatrix(disMatrix, matrixLen)

            else:
                self.dropTable()
                self.createTable(matrixLen)
                self.saveDisMatrix(disMatrix, matrixLen)
        else:
            self.createTable(matrixLen)
            self.saveDisMatrix(disMatrix, matrixLen)

    def loadFrDB(self):
        if self.option == 'atomdistance':
            try:
                disLists = deque()
                selectSQL = 'SELECT * FROM {}'.format(self.pdbID)
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
                disLists = []
                selectSQL = 'SELECT * FROM {}'.format(self.pdbID)
                self.cursor.execute(selectSQL)
                data = self.cursor.fetchall()
                for line in data:
                    tmpDis = list(line)
                    tmpDis[0] = tuple(tmpDis[0])
                    disLists.append(tmpDis)

                # print(len(disMatrix))
                return disLists
            except:
                print("Fail to load from database. please check it! ")
                sys.exit()


if __name__ == '__main__':
    op = sqlOP()  # pdbID='6vw1'
    # op.dropTable()
    print(op.entryAmount)
    # print(op.createTable())
    # print(op.saveToDB())
    # print(op.loadFrDB())
