from src.findAHelix.aHelixExtractr import extractAHelix
from src.findAHelix.aHelixPNGMaker import makeAHelixPNG


class aHelixExecute:
    def __init__(self, pdbID: str, overWrite=False):
        self.pdbID = pdbID.lower()
        self.eA = extractAHelix(self.pdbID, overWrite=overWrite)
        self.mH = makeAHelixPNG()

    def doAHelixPNGs(self):
        aList = self.eA.dS.dR.getAHelix()
        disMatrix = self.eA.dS.disMatrix
        matLen = self.eA.dS.CAAmount

        grayMat = self.mH.grayMatrix(disMatrix, matLen)

        self.mH.plotAHelixPNGs(grayMat, aList, self.pdbID)

        return grayMat

    def findAHelix(self, overWrite=False):
        return self.eA.dS.stepClrDiaLines(overWrite)


if __name__ == '__main__':
    fE = aHelixExecute('1faw',True) # 
    # print(fE.getMstClr([(1,2,3),(1,2,3),(1,2,3),(3,2,1)]))
    print(fE.findAHelix(True)) # 
