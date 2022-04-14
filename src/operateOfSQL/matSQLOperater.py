import sys
import numpy

from collections import deque
from src.operateOfSQL import sqlOP

class matSQLOP(sqlOP):
    
    def createTable(self, matrixLen):
        # Create new table.
        tableCreateSQL = "CREATE TABLE pdb_{}(".format(self.pdbID)
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
    
    def saveDisMatrix(self, disMatrix, matrixLen):
        # Preparation for inserting.
        insertPre = 'INSERT INTO pdb_{}'.format(self.pdbID)+" VALUES "
        tmp = 0

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

        print("SAVE TO DB SUCCESSFULLY.")

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
            print("Fail to load from database. please check it! ")
            sys.exit()
