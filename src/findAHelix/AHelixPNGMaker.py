from src.funcs.pngMaker import makePNG
import os


class makeAHelixPNG(makePNG):

    def __plotAHelixPNG(self, clrMatrix, matLen, __pngFile):
        self._pngPlot(clrMatrix, matLen, __pngFile)

    def plotAHelixPNGs(self, clrMatrix, aHelixList:list, pdbID:str):
        __pngPath="./production/png/aHelixPNG/{}/".format(pdbID)
        if not os.path.exists(__pngPath):
            os.makedirs(__pngPath)

        for aHelix in aHelixList:
            __pngFile = os.path.join(__pngPath, pdbID+"_{}.png".format(str(aHelix)))
            start=aHelix[0]
            end=aHelix[1]+1
            clrMatPiece=clrMatrix[start:end, start:end]
            matLen=clrMatPiece.shape[0]
            
            self.__plotAHelixPNG(clrMatPiece, matLen, __pngFile)

    