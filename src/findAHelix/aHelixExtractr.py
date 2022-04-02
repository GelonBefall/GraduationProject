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
        # residuesCount=self.dS.residuesCount
        # alpahFeature = self.__feature(diaLines)
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

                # disRange.append(aRange)
                # print(aRange)
                mR = lM.modeDisRange(diaLines[step][aRange])
                # disRange = []
                # disRange.append(mR[0])
                # disRange.append(mR[1])

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

    # def featureMatrix(self):



    # def __feature(self, diaLines):
    #     lM = listMode()
    #     # self.dS = diaStep(pdbID)
    #     feature = {}

    #     for step in diaLines:
    #         counts = {}
    #         for ranged in diaLines[step]:
    #             mode = lM.modeClr(diaLines[step][ranged])

    #             if mode not in counts:
    #                 counts[mode] = 1
    #             else:
    #                 counts[mode] += 1
    #         # print(counts)
    #         mstFreq = max(counts, key=counts.get)
    #         # alpahFeature[step]=rangedFeature
    #         feature[step] = mstFreq

    #     return feature

    # 

    # def __featureOfAllAHelix(self):
    #     '''计算某蛋白质中，α螺旋的总距离范围。'''
    #     diaLines = self.dS.stepAHelixDiaLines()
    #     # alpahFeature = self.__feature(diaLines)
    #     lM = listMode()
    #     alphaFeature = {}

    #     for step in diaLines:
    #         disRange = []
    #         for aRange in diaLines[step]:
    #             if not bool(disRange):
    #                 disRange = lM.modeDisRange(diaLines[step][aRange])
    #             else:
    #                 tmp = lM.modeDisRange(diaLines[step][aRange])

    #                 if disRange[0] > tmp[0]:
    #                     disRange[0] = tmp[0]
    #                 if disRange[1] < tmp[1]:
    #                     disRange[1] = tmp[1]

    #         alphaFeature[step] = disRange

    #     return alphaFeature


if __name__ == '__main__':
    fE = extractAHelix(pdbID='2erk')
    # print(fE.getMstClr([(1,2,3),(1,2,3),(1,2,3),(3,2,1)]))
    print(fE.featureOfAHelixs(overWrite=True))  #
