from src.operateOfPNG.pngMaker import makePNG
import os
import shutil
from pathlib import Path


class makeAHelixPNG(makePNG):
    def __init__(self, colorFilename="gray.rgb"):
        super().__init__(colorFilename)
        self.__path=self.__pathExe()
    
    def __mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def __pathExe(self, pdbID: str):
        __pngPath = "./production/aHelixPNG/"

        for root, dirs, files in os.walk(__pngPath): # 选择存储图片的位置
            for dir in dirs: # aHelix_x
                subdir = Path(dir)
                result=list(subdir.glob(pdbID))

                __pngPath=os.path.join(dir, pdbID)
                if result!=[]:
                    return __pngPath # 如果找到了已存在的文件夹，返回路径。

                else:
                    for subroot, subdirs, subfiles in os.walk(dir):
                        if len(list(subdirs))>=2000:
                            continue

                    else:
                        self.__mkdir(__pngPath)
                        return __pngPath

    def pngDeleter(self, pdbID: str):
        # __pngPath = self.__pathExe(pdbID)
        shutil.rmtree(self.__path)
        # for root, dirs, files in os.walk(self.__path):
        #     if list(files):
        #         for file in files:
        #             file=os.path.join(self.__path, file)
        #             os.remove(file)

        # os.rmdir(self.__path)
        print("已成功删除{}的α螺旋灰度图片集！".format(pdbID))

    def __plotAHelixPNG(self, clrMatrix, matLen, __pngFile):
        self._pngPlot(clrMatrix, matLen, __pngFile)

    def plotAHelixPNGs(self, clrMatrix, aHelixList: list, pdbID: str):
        # __pngPath = self.__pathExe(pdbID)

        for root, dirs, files in os.walk(self.__path):
            if len(files) == len(aHelixList):
                print('已生成过{}的α螺旋灰度矩阵图，已自动跳过。'.format(pdbID))
                return 0
            else:
                print('未生成过{}的α螺旋灰度矩阵图，将自动生成。'.format(pdbID))

        for aHelix in aHelixList:
            __pngFile = os.path.join(
                self.__path, pdbID+"_{}.png".format(str(aHelix)))

            start = aHelix[0]
            end = aHelix[1]+1
            clrMatPiece = clrMatrix[start:end, start:end]

            matLen = clrMatPiece.shape[0]
            try:
                self.__plotAHelixPNG(clrMatPiece, matLen, __pngFile)
            except:
                print("生成图片错误的蛋白质：", pdbID)
