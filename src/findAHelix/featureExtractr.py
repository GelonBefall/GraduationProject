from src.findAHelix.diagonalSteper import diaStep
from src.funcs.listModer import listMode

from collections import Counter


class featureExtract:
    def __init__(self, pdbID='1a4f'):

        self.dS = diaStep(pdbID)
        pass

    def getMstClr(list_data):
        x1 = sorted(Counter(list_data))
        print(x1)
        return x1[0]

    def __feature(self, diaLines):
        lM = listMode()
        # self.dS = diaStep(pdbID)
        feature = {}

        for step in diaLines:
            counts = {}
            for ranged in diaLines[step]:
                mode = lM.modeClr(diaLines[step][ranged])

                if mode not in counts:
                    counts[mode] = 1
                else:
                    counts[mode] += 1
            # print(counts)
            mstFreq = max(counts, key=counts.get)
            # alpahFeature[step]=rangedFeature
            feature[step] = mstFreq

        return feature

    def featureOfAHelix(self):
        '''提取α螺旋每条对角线的特征距离范围。'''
        diaLines = self.dS.stepAHelixDiaLines()
        # alpahFeature = self.__feature(diaLines)
        lM = listMode()
        alphaFeature = {}

        for step in diaLines:
            disRange = []
            for aRange in diaLines[step]:
                if not bool(disRange):
                    disRange = lM.modeDisRange(diaLines[step][aRange])
                else:
                    tmp = lM.modeDisRange(diaLines[step][aRange])
                    if disRange[0] > tmp[0]:
                        disRange[0] = tmp[0]
                    if disRange[1] < tmp[1]:
                        disRange[1] = tmp[1]
            alphaFeature[step] = disRange

        return alphaFeature

    def __featureOfTotal(self):
        pass


if __name__ == '__main__':
    fE = featureExtract()
    # print(fE.getMstClr([(1,2,3),(1,2,3),(1,2,3),(3,2,1)]))
    print(fE.featureOfAHelix())
