from src.findAHelix.diagonalSteper import diaStep
from src.funcs.listModer import listMode
from src.operateOfSQL.sqlOperater import sqlOP

from collections import Counter


class extractAHelix:
    def __init__(self, pdbID:str, overWrite=False):

        self.dS = diaStep(pdbID, overWrite=overWrite)
        self.pdbID = pdbID

    def getMstClr(list_data):
        x1 = sorted(Counter(list_data))
        print(x1)
        return x1[0]

    def featureOfAHelixs(self, overWrite=False):
        '''分组计算某蛋白质每种间隔中，所有α螺旋的距离范围。'''
        diaLines = self.dS.stepAHelixDiaLines()
        lM = listMode()
        sql = sqlOP(pdbID=self.pdbID, database='alphaFeatures')

        if overWrite == False:
            if sql.tableExist() == 0:
                alphaFeatures = sql.loadFrDB()
                sql.db.close()
                return alphaFeatures

        alphaFeatures = {}
        disInfos = []
        for step in diaLines:
            alphaFeature = {}

            for aRange in diaLines[step]:

                mR = lM.modeDisRange(diaLines[step][aRange])

                alphaFeature[aRange] = mR  # disRange

                disInfo = [step, aRange]
                disInfo.append(mR[0])
                disInfo.append(mR[1])
                disInfo.append(mR[1]-mR[0])
                disInfos.append(disInfo)

            alphaFeatures[step] = alphaFeature

        sql.saveToDB(disMatrix=disInfos, overWrite=overWrite)
        sql.db.close()

        return alphaFeatures


if __name__ == '__main__':
    fE = extractAHelix(pdbID='2erk')
    # print(fE.getMstClr([(1,2,3),(1,2,3),(1,2,3),(3,2,1)]))
    print(fE.featureOfAHelixs(overWrite=True))  #
