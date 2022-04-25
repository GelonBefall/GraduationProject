import os

from src.findAHelix import aHelixExecute
from src.funcs.accuracyRater import accuRater


class application:
    def __init__(self, pdbID: str, overWrite=False, dsspPath=None):
        self.pdbID = pdbID.lower()
        self.aE = aHelixExecute(self.pdbID, overWrite, dsspPath=dsspPath)

    def __bool__(self):
        if bool(self.aE) == False:
            return False
        else:
            return True

    def doMatPNG(self):
        return self.aE.eA.dS.mE.doDisPNG()

    def doAHelixPNGs(self):
        return self.aE.doAHelixPNGs()

    def aHelixFeatures(self):
        return (self.aE.aHelixFeatures())
        # print

    def writeLowAccu(self, dsspRange, assignRange):
        __filePath=os.path.join(os.getcwd(), 'production/lowAccu.txt')
        with open(__filePath, 'a+', encoding='utf-8') as f:
            writed=[self.pdbID+'\n', 'dssp范围：'+str(dsspRange)+'\n', '程序指定范围：'+str(assignRange)+'\n\n']
            f.writelines(writed)

    def accuRater(self):
        dsspRange = self.aE.eA.dS.aR
        assignRange = self.aE.eA.dS.stepClrDiaLines1() # 算法 1
        
        if len(assignRange)==0:
            assignRange = self.aE.eA.dS.stepClrDiaLines2() # 算法 2

        self.accR=accuRater(self.pdbID, dsspRange, assignRange)
        accuRate = self.accR.getAccuRate()
        
        if accuRate[self.pdbID] == 0:
            self.writeLowAccu(dsspRange, assignRange)
        return  accuRate

    def accuValuer(self):
        # dsspRange = self.aE.eA.dS.dR.getAHelix()
        # assignRange = self.aE.eA.dS.stepClrDiaLines1()
        return self.accR.getAccuValue()
