from src.findAHelix.diagonalSteper import diaStep
from src.funcs.listAnalyst import anaList
from src.operateOfSQL.sqlOperater import sqlOP

from collections import Counter


class extractAHelix:
    def __init__(self, pdbID: str, overWrite=False):

        self.dS = diaStep(pdbID, overWrite=overWrite)
        self.pdbID = pdbID

    def getMstClr(list_data):
        x1 = sorted(Counter(list_data))
        print(x1)
        return x1[0]

    def featureOfAHelixs(self, overWrite=False):
        '''分组计算某蛋白质每种间隔中，所有α螺旋的距离范围。'''
        diaLines = self.dS.stepDiaLines()
        lM = anaList()
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

                mR = lM.rangeDis(diaLines[step][aRange])

                alphaFeature[aRange] = mR  # 范围内的最大最小值

                disInfo = [step, aRange]
                disInfo.append(mR[0])  # 相差几个
                disInfo.append(mR[1])  # α螺旋开始点
                disInfo.append(mR[1]-mR[0])  # α螺旋结束点

                disInfos.append(disInfo)

            alphaFeatures[step] = alphaFeature

        sql.saveToDB(disMatrix=disInfos, overWrite=overWrite)
        sql.db.close()

        return alphaFeatures


if __name__ == '__main__':
    fE = extractAHelix(pdbID='2WFV')
    # print(fE.getMstClr([(1,2,3),(1,2,3),(1,2,3),(3,2,1)]))
    print(fE.featureOfAHelixs(overWrite=True))  #
