from src.findAHelix import aHelixExecute
from src.funcs.accuracyRater import getAccuRate, getAccuRate2


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

    def getAccuRate(self):
        dsspRange = self.aE.eA.dS.dR.getAHelix()
        assignRange = self.aE.eA.dS.stepClrDiaLines()
        return getAccuRate2(self.pdbID, dsspRange, assignRange)
