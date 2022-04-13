import png
import numpy

from collections import deque

from src.operateOfPNG import pngInit


class makePNG(pngInit):

    def _pngPlot(self, clrMatrix, matLen, pngFile):
        # pngPath="./production/png"
        # pngFile = os.path.join(pngPath, pdbID+".png")
        pngData = []
        for i in range(matLen):
            tmp = []
            for j in range(matLen):
                # Each line in colormap has three values including R,G,B。
                for element in clrMatrix[i][j]:
                    tmp.append(element)
            pngData.append(tuple(tmp))

        f = open(pngFile, "wb")
        w = png.Writer(matLen, matLen, greyscale=False)
        w.write(f, pngData)
        f.close()

    def getMyChecks(self, RGB):
        RGB = tuple(RGB)
        check = []
        index = self.colormaps.index(RGB)
        check.append(9-index)
        if (2 in check) or (3 in check):
            check = [2, 3]
        elif 4 in check:
            check = [4, 5]
        return check

    def grayMatrix(self, disMatrix, matLen):
        grayLists = deque()

        for i in range(matLen):
            tmp = deque()

            for m in range(matLen):
                checked = self.getChecked(disMatrix[i][m])
                tmp.append(self.colormaps[9-checked])
            grayLists.append(tmp)

        grayMatrix = numpy.array(grayLists)
        return grayMatrix


if __name__ == '__main__':
    mkPNG = makePNG()
    pngfile='.\\production\\png\\matPNG\\1a4f.png'
    print(mkPNG._pngPlot())
