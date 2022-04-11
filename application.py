from src.findAHelix import aHelixExecute
from src.funcs.accuracyRater import getAccuRate


class application:
    def __init__(self, pdbID: str, overWrite=False):
        self.pdbID=pdbID.lower()
        self.aE = aHelixExecute(self.pdbID, overWrite)
        

    def __bool__(self):
        if type(self.aE.eA.dS.disMatrix) == bool:
            return False
        else:
            return True

    def doMatPNG(self):
        return self.aE.eA.dS.mE.doDisPNG()

    def doAHelixPNGs(self):
        return self.aE.doAHelixPNGs()

    def aHelixFeatures(self):
        return self.aE.aHelixFeatures()
    
    def getAccuRate(self):
        dsspRange=self.aE.eA.dS.dR.getAHelix()
        assignRange=self.aE.eA.dS.stepClrDiaLines()
        return getAccuRate(self.pdbID, dsspRange, assignRange)