import os
import sys
import png
import numpy

from collections import deque


class makePNG:
    def __init__(self, colorFilename="gray.rgb"):

        self.__rgbPath = "./materials/rgb/"
        self.__colormapInit(colorFilename)

    def colormapExist(self, colorFile):
        if os.path.exists(colorFile):
            # print("The RGB file exist!")
            return 0
        else:
            print("The RGB doesn't exist!")
            return 1

    def __colormapInit(self, colorFilename="gray.rgb"):
        colorFile = os.path.join(self.__rgbPath, colorFilename)
        RGBstatus = self.colormapExist(colorFile)
        if RGBstatus == 1:
            sys.exit()

        colormaps = []
        with open(colorFile) as f:
            for line in f:
                # colormapMatrix.insert(0,list(map(int,line.split())))
                colormaps.append(tuple(map(int, line.split(","))))
        self.colormaps = colormaps  # np.array(colormaps)
        # print(self.colormaps)

    def _pngPlot(self, clrMatrix, matLen, pngFile):
        # pngPath="./production/png"
        # pngFile = os.path.join(pngPath, pdbID+".png")
        pngData = []
        for i in range(matLen):
            tmp = []
            for j in range(matLen):
                # Each line in colormap has three values,R,G,B。
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

    def getChecked(self, dis):
        def getCheck(dis): return {
            23 < dis: 10,
            13 < dis <= 23: 9,
            10.0 < dis <= 13: 8,
            9.0 < dis <= 10.0: 7,
            8.0 <= dis <= 9.0: 6,
            7.0 < dis < 8.0: 5,
            6.0 <= dis <= 7.0: 4,
            5.0 <= dis < 6.0: 3,
            4.0 < dis < 5.0: 2,
            3.0 <= dis <= 4.0: 1,
            dis < 3.0: 0
        }
        checked = getCheck(dis)[True]
        return checked

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
    print(mkPNG.colormaps)
