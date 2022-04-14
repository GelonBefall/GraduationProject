from src.operateOfPNG.pngMaker import makePNG
import os


class makeAHelixPNG(makePNG):

    def __mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def __pathExe(self, pdbID: str):
        __pngPath = "./production/png/aHelixPNG/"
        self.__mkdir(__pngPath)
        __pngPath += pdbID
        self.__mkdir(__pngPath)

        return __pngPath

    def __plotAHelixPNG(self, clrMatrix, matLen, __pngFile):
        self._pngPlot(clrMatrix, matLen, __pngFile)

    def plotAHelixPNGs(self, clrMatrix, aHelixList: list, pdbID: str):
        __pngPath = self.__pathExe(pdbID)

        for root, dirs, files in os.walk(__pngPath):
            if len(files) == len(aHelixList):
                print('已生成过{}的α螺旋灰度矩阵图，已自动跳过。'.format(pdbID))
                return 0

        for aHelix in aHelixList:
            __pngFile = os.path.join(
                __pngPath, pdbID+"_{}.png".format(str(aHelix)))
            
            start = aHelix[0]
            end = aHelix[1]+1
            clrMatPiece = clrMatrix[start:end, start:end]

            matLen = clrMatPiece.shape[0]
            try:
                self.__plotAHelixPNG(clrMatPiece, matLen, __pngFile)
            except:
                print("生成图片错误的蛋白质：", pdbID)
