from src.funcs.pngMaker import makePNG
import os


class makeDisPNG(makePNG):
    def disPlot(self, clrMatrix, matLen, pdbID: str):
        __pngPath = "./production/png/matPNG/"
        if not os.path.exists(__pngPath):
            os.makedirs(__pngPath)

        else:
            for root, dirs, files in os.walk(__pngPath):
                if bool(files):
                    print('已生成过{}的灰度矩阵图，已自动跳过。'.format(pdbID))
                    return 0

        __pngFile = os.path.join(__pngPath, pdbID+".png")
        self._pngPlot(clrMatrix, matLen, pngFile=__pngFile)
