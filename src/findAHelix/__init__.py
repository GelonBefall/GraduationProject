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
            pickleName = self.pdbID+'_chosenArea'

            self.mH.pngDeleter()
            self.eA.dS.pickle.deletePickle(pickleName)
            if self.eA.dS.CAAmount >= 800:
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
        # grayMat = self.eA.dS.mE.grayMat
        
        self.mH.plotAHelixPNGs(self.eA.dS.mE.grayMat, aList)

    def aHelixFeatures(self):
        return self.eA.featureOfAHelixs()

    # def findAHelix(self, overWrite=False):
    #     return self.eA.dS.stepClrDiaLines(overWrite)


if __name__ == '__main__':
    fE = aHelixExecute('117e')
    # print(fE.getMstClr([(1,2,3),(1,2,3),(1,2,3),(3,2,1)]))
    # print(fE.findAHelix(True)) #
    print(fE.doAHelixPNGs())
