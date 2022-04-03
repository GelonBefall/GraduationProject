from src.funcs.pngMaker import makePNG
import os


class makeDisPNG(makePNG):
    def disPlot(self, clrMatrix, matLen, pdbID:str):
        __pngPath="./production/png/matPNG/"
        if not os.path.exists(__pngPath):
            os.makedirs(__pngPath)
            
        __pngFile = os.path.join(__pngPath, pdbID+".png")
        self._pngPlot(clrMatrix, matLen, pngFile=__pngFile)