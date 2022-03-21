from src.findAHelix.diagonalSteper import diaStep
from src.funcs.listModer import listMode

from collections import Counter


class featureExtract:
    def __init__(self, pdbID='1faw'):

        self.dS = diaStep(pdbID)

    def getMstClr(list_data):
        x1 = sorted(Counter(list_data))
        print(x1)
        return x1[0]

    def __feature(self, diaLines):
        lM = listMode()
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
        '''提取α螺旋每条对角线的特征距离。'''
        diaLines = self.dS.stepAHelixDiaLines()
        alpahFeature = self.__feature(diaLines)

        return alpahFeature

    def featureOfTotal(self):
        pass


if __name__ == '__main__':
    fE = featureExtract()
    # print(fE.getMstClr([(1,2,3),(1,2,3),(1,2,3),(3,2,1)]))
    print(fE.featureOfAHelix())
