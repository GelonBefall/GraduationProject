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

    def grayMatrix(self, disMatrix, matLen):
        grayLists = deque()

        for i in range(matLen):
            tmp = deque()

            for m in range(matLen):
                checked = 0
                if 23 < disMatrix[i][m]:
                    checked = 10
                elif 15 < disMatrix[i][m] <= 23:
                    checked = 9
                elif 10.4 < disMatrix[i][m] <= 15:
                    checked = 8
                elif 9.2 < disMatrix[i][m] <= 10.4:
                    checked = 7
                elif 8.2 <= disMatrix[i][m] <= 9.2:
                    checked = 6
                elif 6.7 < disMatrix[i][m] < 8.2:
                    checked = 5
                elif 5.8 <= disMatrix[i][m] <= 6.7:
                    checked = 4
                elif 4.8 <= disMatrix[i][m] < 5.8:
                    checked = 3
                elif 4.0 < disMatrix[i][m] < 4.8:
                    checked = 2
                elif 3.5 <= disMatrix[i][m] <= 4.0:
                    checked = 1
                elif disMatrix[i][m] < 3.5:
                    checked = 0
                tmp.append(self.colormaps[9-checked])
            grayLists.append(tmp)

        grayMatrix = numpy.array(grayLists)
        return grayMatrix


if __name__ == '__main__':
    mkPNG = makePNG()
    print(mkPNG.colormaps)
