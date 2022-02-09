from attr import field
import pymysql
import os
import sys
import numpy as np

from pydoc import describe
from soupsieve import select

from development.matrixMaker import calMatrix


class sqlOp:
    '''The username and password of MySQL are needed from Envionment Variables.
       user's key is "SQLUSER", password's is "SQLPSWD". 
       Attention: You need to restart you PC to make new Envionment Variables available'''

    def __init__(self, pdbID='2erk', database='atomdistance'):
        # You need to set which database you will use.
        user = os.environ.get('SQLUSER')
        password = os.environ.get('SQLPSWD')

        self.pdbID = pdbID
        newMatrix = calMatrix(pdb_id=pdbID)
        self.distanceMatrix = np.array(newMatrix.trueMatrix())
        self.matrixLen = len(self.distanceMatrix)

        # 打开数据库连接
        self.db = pymysql.connect(host='127.0.0.1',
                                  user=user,
                                  password=password,
                                  database=database,
                                  charset='utf8')
        self.cursor = self.db.cursor()

    def tableExist(self):
        try:
            describeSQL = "DESCRIBE {}".format(self.pdbID)
            self.cursor.execute(describeSQL)
            return 0
        except:
            return 1

    def createTable(self, reload_mode=True):
        '''reload_mode means to cover the old table.'''
        isExist = self.tableExist()
        if isExist == 0:

            # Drop table.
            if reload_mode == True:
                try:
                    deleteTableSQL = "DROP TABLE {}".format(self.pdbID)
                    self.cursor.execute(deleteTableSQL)
                    self.db.commit()
                except:
                    self.db.rollback()
                    print("DROP TABLE ERROR, please check your database.")
                    sys.exit()
            else:
                return 0

        # Create new table.
        tableCreateSQL = "CREATE TABLE {}(".format(self.pdbID)
        for i in range(self.matrixLen-1):
            tableCreateSQL = tableCreateSQL + 'Coloumn{} DOUBLE,'.format(i)
        tableCreateSQL = tableCreateSQL + \
            'Coloumn{} DOUBLE)'.format(self.matrixLen-1)
        if i>1000: # Choose engine MyISAM.
            tableCreateSQL=tableCreateSQL+'engine=MyISAM'

        try:
            self.cursor.execute(tableCreateSQL)
            self.db.commit()
            return 0
        except:
            self.db.rollback()
            print("CREATE TABLE ERROR.")
            sys.exit()

    def saveDistance(self):
        insertPre = 'INSERT INTO {}'.format(self.pdbID)+" VALUES " # Preparation for inserting.
        i = 0
        tmp=0
        print(self.matrixLen)
        while i < self.matrixLen:
            if tmp == 5:
                print("INSERT ERROR")
                sys.exit()
            insertSQL = insertPre + str(tuple(self.distanceMatrix[i]))
            try:
                self.cursor.execute(insertSQL)
                self.db.commit()
                i = i+1
                tmp = 0
            except:
                self.db.rollback()
                i = i-1
                tmp = tmp+1

    def saveToDB(self):
        isExist=self.tableExist()
        if isExist==0:
            isEmptySQL='SELECT COUNT(1) FROM {}'.format(self.pdbID)
            self.cursor.execute(isEmptySQL)
            data=self.cursor.fetchone()
            print(data[0])
            if data[0]==self.matrixLen:
                print("You have saved the distance matrix. Do not execute again.")
                sys.exit()
            elif data[0]==0:
                self.saveDistance()
            else:
                self.createTable()
                self.saveDistance()
        else:
            self.createTable()
            self.saveDistance()
    
    def loadFrDB(self):
        pass

    def backup():
        pass
        # insertPre=' ('
        # for i in range(self.matrixLen-1):
        #     insertPre=insertPre+"Coloumn{},".format(i)
        # insertPre = insertPre + "Coloumn{} ) ".format(self.matrixLen-1) + " VALUES "


if __name__ == '__main__':
    op = sqlOp(pdbID='6vw1')
    # print(op.createTable())
    print(op.saveToDB())
