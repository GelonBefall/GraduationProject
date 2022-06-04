import os
import sys


class pngInit:
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
                colormaps.append(tuple(map(int, line.split(","))))
        self.colormaps = colormaps
        # print(self.colormaps)

    def getChecked(self, dis):
        '''划分距离区间，数字化选择上色颜色。'''
        def getCheck(dis): return {
            20 < dis: 10,
            13 < dis <= 20: 9,
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


if __name__ == '__main__':
    png1 = pngInit()
