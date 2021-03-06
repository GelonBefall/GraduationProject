import os
import shutil
from pathlib import Path

from src.operateOfPNG.pngMaker import makePNG


class makeAHelixPNG(makePNG):
    def __init__(self, pdbID: str, colorFilename="gray.rgb"):
        super().__init__(colorFilename)
        self.pdbID = pdbID
        self.__path = self.__pathExe()

    def __mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def __pathExe(self):
        __pngPath = os.path.join(os.getcwd(), "production/aHelixPNG/")
        subdir = Path(__pngPath)

        result = list(subdir.rglob(self.pdbID))
        if len(result) != 0:
            __pngPath = str(result[0])  # 如果找到了已存在的文件夹，返回路径。
            return __pngPath

        else:
            for root, dirs, files in os.walk(__pngPath):  # 选择存储图片的位置
                for dir in dirs:  # aHelix_x
                    dirPath = os.path.join(__pngPath, dir)

                    # 如果未找到，寻找一个存放位置。
                    for subroot, subdirs, subfiles in os.walk(dirPath):
                        if len(subdirs) >= 2000:
                            break  # 太多了，去下一个文件夹

                        else:
                            __pngPath = os.path.join(dirPath, self.pdbID)
                            return __pngPath

    def pngDeleter(self):
        if os.path.exists(self.__path):
            shutil.rmtree(self.__path)
        print("已成功删除{}的α螺旋灰度图片集！".format(self.pdbID))

    def __pngCopyer(self, source, destination):
        shutil.copyfile(source, destination)

    def __plotAHelixPNG(self, clrMatrix, matLen, __pngFile):
        __pngPath1=os.path.join(self.__path, __pngFile)
        self._pngPlot(clrMatrix, matLen, __pngPath1)

        def getLen(dis): return {
            30.0 < dis : 40,
            20.0 < dis <= 30.0: 30,
            10.0 < dis <= 20.0: 20,
            5.0 < dis <= 10.0: 10,
            dis <= 5.0: 5
        }
        len = getLen(matLen)[True]

        desPath=os.path.join(os.getcwd(), "production/sizePNG/", str(len))
        __pngPath2=os.path.join(desPath, __pngFile)
        self.__pngCopyer(__pngPath1,__pngPath2)

    def plotAHelixPNGs(self, clrMatrix, aHelixList: list):

        self.__mkdir(self.__path)
        for root, dirs, files in os.walk(self.__path):
            if len(files) == len(aHelixList):
                print('已生成过{}的α螺旋灰度矩阵图，已自动跳过。'.format(self.pdbID))
                return 0
            else:
                print('未生成过{}的α螺旋灰度矩阵图，将自动生成。'.format(self.pdbID))

        for aHelix in aHelixList:
            __pngFile = self.pdbID+"_{}.png".format(str(aHelix))

            start = aHelix[0]
            end = aHelix[1]+1
            clrMatPiece = clrMatrix[start:end, start:end]

            matLen = clrMatPiece.shape[0]
            try:
                self.__plotAHelixPNG(clrMatPiece, matLen, __pngFile)
            except:
                print("生成图片错误的蛋白质：", self.pdbID)


if __name__ == '__main__':
    mah = makeAHelixPNG('1a4f')
