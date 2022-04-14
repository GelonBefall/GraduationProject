import sys

from src.operateOfSQL import sqlOP


class aHelixSQLOP(sqlOP):

    def createTable(self):
        # Create new table.
        tableCreateSQL = "CREATE TABLE pdb_{}(".format(self.pdbID)
        tableCreateSQL += ' STEP TINYINT(10), ALPHARANGES CHAR(12), STEPMINS DOUBLE, STEPMAXS DOUBLE, DIFFERVALUES FLOAT, MEAN FLOAT, VARIANCE FLOAT)'
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

            return alphaFeatures
        except:
            print("Fail to load from database {}. please check it! ".format(
                self.database))
            sys.exit()

    def saveAlphaFeatures(self, alphaFeatures, featureLen):
        # Preparation for inserting.
        insertPre = 'INSERT INTO pdb_{}'.format(self.pdbID)+" VALUES "
        tmp = 0

        # Insert data.
        i = 0
        while i < featureLen:
            if tmp == 5:
                print("INSERT DATA IN {} ERROR".format(self.database))
                sys.exit()
            alphaFeatures[i][1] = str(alphaFeatures[i][1])
            insertSQL = insertPre + str(tuple(alphaFeatures[i]))
            try:
                self.cursor.execute(insertSQL)
                self.db.commit()
                i = i+1
                tmp = 0
            except:
                self.db.rollback()
                i = i-1
                tmp = tmp+1

        print("Save features of α-Helix to DB successfully.")
        return 0

    def saveToDB(self, alphaFeatures, overWrite=False):
        isExist = self.tableExist()
        featuresLen = len(alphaFeatures)
        if isExist == True:

            if (self.entryAmount == featuresLen) and (overWrite == False):
                print("You have saved the features of α-Helix in {}. pdb_{}. Do not execute again.".format(
                    self.database, self.pdbID))
                return 0

            elif self.entryAmount == 0:
                self.saveAlphaFeatures(alphaFeatures, featuresLen)

            elif self.entryAmount == -1:
                self.createTable()
                self.saveAlphaFeatures(alphaFeatures, featuresLen)

            else:
                self.dropTable()
                self.createTable()
                self.saveAlphaFeatures(alphaFeatures, featuresLen)
        else:
            self.createTable()
            self.saveAlphaFeatures(alphaFeatures, featuresLen)
        return 0
