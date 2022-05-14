from src.findAHelix.diagonalSteper import diaStep
from src.funcs.listAnalyst import anaList
from src.operateOfSQL.aHelixSQLOperater import aHelixSQLOP


class extractAHelix:
    def __init__(self, pdbID: str, overWrite=False, dsspPath=None):
        self.pdbID = pdbID.lower()

        self.dS = diaStep(self.pdbID, overWrite=overWrite, dsspPath=dsspPath)

    def __bool__(self):
        if bool(self.dS) == False:
            return False
        else:
            return True

    def dropDSSP(self):
        sql = aHelixSQLOP(pdbID=self.pdbID, database='alphaFeatures')
        sql.dropTable()
        sql.db.close()
        
        self.dS.dR.dsspDeleter()
    
    def featureOfAHelixs(self, overWrite=False):
        '''分组计算某蛋白质每种间隔中，所有α螺旋的距离范围。'''
        diaLines = self.dS.stepDiaLines()
        lM = anaList()
        sql = aHelixSQLOP(pdbID=self.pdbID, database='alphaFeatures')

        if overWrite == False and sql.tableExist() == True and sql.entryAmount != 0:
            alphaFeatures = sql.loadFrDB()
            sql.db.close()
            return alphaFeatures

        else:
            alphaFeatures = {}
            disInfos = []
            for step in diaLines:
                # 以间隔长短遍历
                alphaFeature = {}
                # print("两残基编号相差{}时：".format(step))

                for aRange in diaLines[step]:
                    # 以α螺旋范围遍历
                    uList = diaLines[step][aRange]

                    if len(uList) <= 6:
                        continue
                    # print("  {}中的距离特征为：".format(aRange))
                    mR = lM.rangeDis(uList)
                    # print("\t相隔{}的距离范围为：".format(step), mR)
                    mD = lM.meanDis(uList)
                    # print("\t相隔{}的平均距离为：".format(step), mD)
                    vD = lM.varDis(uList)
                    # print("\t相隔{}的距离方差为：".format(step), vD)
                    if mR == 0 or mD == 0 or vD == 0:
                        continue

                    alphaFeature[aRange] = mR  # 范围内的最大最小值

                    disInfo = [step, aRange]  # 相差位数， 范围
                    disInfo.append(mR[0])  # α螺旋最小距离
                    disInfo.append(mR[1])  # α螺旋最大距离
                    disInfo.append(mR[1]-mR[0])  # 距离差值
                    disInfo.append(mD)  # 平均数
                    disInfo.append(vD)  # 方差

                    disInfos.append(disInfo)

                alphaFeatures[step] = alphaFeature

            sql.saveToDB(disInfos, True)
            sql.db.close()
        return alphaFeatures


if __name__ == '__main__':
    # from src.funcs.dirWalker import getPDBID
    # pdbIDs=getPDBID()
    # for pdbID in pdbIDs:
    pdbID = '1a0a'
    fE = extractAHelix(pdbID, True)
    # print(fE.getMstClr([(1,2,3),(1,2,3),(1,2,3),(3,2,1)]))
    print(fE.featureOfAHelixs(overWrite=True))  #
