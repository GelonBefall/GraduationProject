from src.operateOfPNG.pngMaker import makePNG
import os
import shutil
from pathlib import Path


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
        subdir = Path(dir)
        result = list(subdir.rglob(self.pdbID))
        if len(result) != 0:
            __pngPath =str(result[0]) # 如果找到了已存在的文件夹，返回路径。
            return  __pngPath 

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
                            self.__mkdir(__pngPath)
                            return __pngPath

    def pngDeleter(self):
        # __pngPath = self.__pathExe(pdbID)
        shutil.rmtree(self.__path)
        # for root, dirs, files in os.walk(self.__path):
        #     if list(files):
        #         for file in files:
        #             file=os.path.join(self.__path, file)
        #             os.remove(file)

        # os.rmdir(self.__path)
        print("已成功删除{}的α螺旋灰度图片集！".format(self.pdbID))

    def __plotAHelixPNG(self, clrMatrix, matLen, __pngFile):
        self._pngPlot(clrMatrix, matLen, __pngFile)

    def plotAHelixPNGs(self, clrMatrix, aHelixList: list):
        # __pngPath = self.__pathExe(pdbID)

        for root, dirs, files in os.walk(self.__path):
            if len(files) == len(aHelixList):
                print('已生成过{}的α螺旋灰度矩阵图，已自动跳过。'.format(self.pdbID))
                return 0
            else:
                print('未生成过{}的α螺旋灰度矩阵图，将自动生成。'.format(self.pdbID))

        for aHelix in aHelixList:
            __pngFile = os.path.join(
                self.__path, self.pdbID+"_{}.png".format(str(aHelix)))

            start = aHelix[0]
            end = aHelix[1]+1
            clrMatPiece = clrMatrix[start:end, start:end]

            matLen = clrMatPiece.shape[0]
            try:
                self.__plotAHelixPNG(clrMatPiece, matLen, __pngFile)
            except:
                print("生成图片错误的蛋白质：", self.pdbID)
