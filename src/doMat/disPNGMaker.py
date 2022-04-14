import os

from src.operateOfPNG.pngMaker import makePNG
from src.operateOfPNG.pngReader import readPNG


class makeDisPNG(makePNG):

    def __pathExe(self, pdbID: str):
        __pngPath = "./production/png/matPNG/"
        if not os.path.exists(__pngPath):
            os.makedirs(__pngPath)

        __pngFile = pdbID+".png"
        __pngFile = os.path.join(__pngPath, __pngFile)

        if os.path.exists(__pngFile):
            return 0
        else:
            return __pngFile

    def disPlot(self, clrMatrix, matLen, pdbID: str):
        __pngFile = self.__pathExe(pdbID)

        if __pngFile == 0:
            return 0

        else:
            self._pngPlot(clrMatrix, matLen, pngFile=__pngFile)

    def loadGrayMat(self, pdbID: str):
        __pngFile = self.__pathExe(pdbID)
        if __pngFile != 0:
            print('未生成过{}的灰度矩阵图，将自动生成。'.format(pdbID))
            raise
            # return
        else:
            reader = readPNG()
            grayMat = reader.loadGrayMat(__pngFile)
            return grayMat
