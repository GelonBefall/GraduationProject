import pymysql
import os
import sys

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

        self.database = database
        self.pdbID = pdbID

        # 打开数据库连接
        self.db = pymysql.connect(host='127.0.0.1',
                                  user=user,
                                  password=password,
                                  database=self.database,
                                  charset='utf8')
        self.cursor = self.db.cursor()

        self.entryAmount = self.entryCount()

    def tableExist(self):
        try:
            describeSQL = "DESCRIBE pdb_{}".format(self.pdbID)
            self.cursor.execute(describeSQL)
            return True
        except:
            return False

    def entryCount(self):
        try:
            isEmptySQL = 'SELECT COUNT(1) FROM pdb_{}'.format(self.pdbID)
            self.cursor.execute(isEmptySQL)
            data = self.cursor.fetchone()
            print("The entrys of {} you have saved is {}".format(
                self.database, data[0]))
            return data[0]
        except:
            print("Cant found the table in {}.".format(self.database))
            return -1

    def dropTable(self):
        if self.entryAmount == -1:
            print("pdb_{}在数据库{}中不存在，无需删除。".format(self.pdbID, self.database))
            return 0
        try:
            deleteTableSQL = "DROP TABLE pdb_{}".format(self.pdbID)
            self.cursor.execute(deleteTableSQL)
            self.db.commit()
            print("DROP TABLE SUCCESSFULLY IN {}.".format(self.database))
            return 0
        except:
            self.db.rollback()
            print("DROP TABLE IN {} ERROR, please check your database.".format(
                self.database))
            sys.exit()


if __name__ == '__main__':
    op = sqlOP('2erk')  # pdbID='6vw1'
    # op.dropTable()
    print(op.entryAmount)
    # print(op.createTable())
    # print(op.saveToDB())
    # print(op.loadFrDB())
