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
            return {True: __pngFile}
        else:
            return {False: __pngFile}

    def disPlot(self, clrMatrix, matLen, pdbID: str):
        __pngFile = self.__pathExe(pdbID)

        if True in __pngFile.keys():
            return 0

        else:
            __pngFile = __pngFile[False]
            self._pngPlot(clrMatrix, matLen, pngFile=__pngFile)

    def loadGrayMat(self, pdbID: str):
        __pngFile = self.__pathExe(pdbID)
        if False in __pngFile.keys():
            print('未生成过{}的灰度矩阵图，将自动生成。'.format(pdbID))
            raise
            # return
        else:
            print('已生成过{}的灰度矩阵图，将自动读取。'.format(pdbID))
            __pngFile = __pngFile[True]
            reader = readPNG()
            grayMat = reader.loadGrayMat(__pngFile)
            if type(grayMat) == bool:
                raise
            return grayMat
