from src.findAHelix.aHelixExtractr import extractAHelix
from src.findAHelix.aHelixPNGMaker import makeAHelixPNG


class aHelixExecute:
    def __init__(self, pdbID: str, overWrite=False, dsspPath=None):
        self.pdbID = pdbID.lower()
        self.eA = extractAHelix(
            self.pdbID, overWrite=overWrite, dsspPath=dsspPath)
        self.mH = makeAHelixPNG(self.pdbID)

    def __bool__(self):
        if bool(self.eA) == False:
            self.mH.pngDeleter()
            self.eA.dS.mE.mkPNG.pngDeleter()
            
            if self.eA.dS.CAAmount > 500:
                self.eA.dS.mE.mkMat.pdbMover()
                self.eA.dS.dR.dsspMover()
            else:
                self.eA.dS.mE.dropPDB()
                self.eA.dropDSSP()
            return False
        else:
            return True

    def doAHelixPNGs(self):
        aList = self.eA.dS.dR.getAHelix()
        grayMat = self.eA.dS.mE.loadGrayMat()
        
        self.mH.plotAHelixPNGs(grayMat, aList)

    def aHelixFeatures(self):
        return self.eA.featureOfAHelixs()


if __name__ == '__main__':
    fE = aHelixExecute('117e')
    # print(fE.getMstClr([(1,2,3),(1,2,3),(1,2,3),(3,2,1)]))
    # print(fE.findAHelix(True)) #
    print(fE.doAHelixPNGs())
