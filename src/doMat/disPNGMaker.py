import os

from pathlib import Path

from src.operateOfPNG.pngMaker import makePNG
from src.operateOfPNG.pngReader import readPNG


class makeDisPNG(makePNG):
    def __init__(self, pdbID: str, colorFilename="gray.rgb"):
        super().__init__(colorFilename)
        self.pdbID = pdbID
        self.__pngFile = self.__pathExe()

    def __pathExe(self):
        # "./production/matPNG/"
        __pngPath = os.path.join(os.getcwd(), "production/matPNG/")
        pngName = self.pdbID+".png"

        dirPath = Path(__pngPath)
        result = list(dirPath.rglob(pngName))
        if len(result) != 0:
            __pngFile = str(result[0])
            return {True: __pngFile}  # 如果找到了已存在的文件，返回路径。

        else:
            for root, dirs, files in os.walk(__pngPath):  # 如果不存在，选择存储图片的位置
                for dir in dirs:  # matPNG_x
                    __dirPath = os.path.join(__pngPath, dir)
                    # 如果未找到，寻找一个存放位置。
                    for subroot, subdirs, subfiles in os.walk(__dirPath):
                        if len(subfiles) >= 2000:
                            break  # 文件太多了，去下一个文件夹

                        else:
                            __pngFile = os.path.join(__dirPath, pngName)
                            return {False: __pngFile}

    def pngDeleter(self):

        if False in self.__pngFile.keys():
            return 0
        else:
            __pngFile = self.__pngFile[True]
            os.remove(__pngFile)
            print("已成功删除{}的灰度矩阵图！".format(self.pdbID))

    def disPlot(self, clrMatrix, matLen):

        if True in self.__pngFile.keys():
            return 0

        else:
            __pngFile = self.__pngFile[False]
            self._pngPlot(clrMatrix, matLen, pngFile=__pngFile)

    def loadGrayMat(self):

        if False in self.__pngFile.keys():
            print('未生成过{}的灰度矩阵图，将自动生成。'.format(self.pdbID))
            raise
            # return
        else:
            print('已生成过{}的灰度矩阵图，将自动读取。'.format(self.pdbID))
            __pngFile = self.__pngFile[True]
            reader = readPNG()
            grayMat = reader.loadGrayMat(__pngFile)
            if type(grayMat) == bool:
                raise
            return grayMat


if __name__ == "__main__":
    mdp = makeDisPNG('1145')
