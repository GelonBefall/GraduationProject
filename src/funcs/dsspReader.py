import os
import shutil

from pathlib import Path
from DSSPparser.parser import parseDSSP


class readDSSP:
    def __init__(self, pdbID: str, dsspPath=None):
        self.dsspID = pdbID.lower()

        if dsspPath:
            self.__dsspPath = dsspPath
            self.__dsspFile = os.path.join(
                self.__dsspPath, "{}.dssp".format(self.dsspID))
        else:
            self.__dsspFile = self.__dsspFinder()

    def __str__(self):
        return str(self.getAHelix())

    def __dsspFinder(self):
        __dsspPath = os.path.join(os.getcwd(), "materials/dssp/")
        dsspPath = Path(__dsspPath)
        dsspFile = self.dsspID+'.dssp'

        result = list(dsspPath.rglob(dsspFile))

        dsspFile = os.path.join(__dsspPath, result[0])  # ._cparts[2]
        return dsspFile

    def dsspDeleter(self):
        os.remove(self.__dsspFile)
        print("已成功删除{}的dssp文件！".format(self.dsspID))

    def dsspMover(self):
        __newFile = os.path.join(
            os.getcwd(), "materials/big_dssp/", "{}.dssp".format(self.dsspID))
        shutil.move(self.__dsspFile, __newFile)

    def dsspGrouper(self, resNums: list):
        tmp = []
        aHelix = []
        for resNum in resNums:
            if len(tmp) == 1:
                if resNum != (tmp[0]+1):
                    tmp[0] = resNum
                else:
                    tmp.append(resNum)
            elif len(tmp) == 2:
                if resNum != (tmp[1]+1):
                    aHelix.append(tmp)
                    tmp = [resNum]
                else:
                    tmp[1] = resNum
            else:
                tmp.append(resNum)
        if len(tmp) == 2:
            aHelix.append(tmp)
        return aHelix

    def getAHelix(self):
        '''返回α螺旋位置，下标从0开始。例如[1, 3]为第二个到第四个α残基。'''
        Dparser = parseDSSP(self.__dsspFile)
        Dparser.parse()
        pStruct = Dparser.dictTodataframe()[['resnum', 'struct']]
        # pStruct=pddict
        # print(pStruct)
        resNums = pStruct[pStruct['struct'] == '  H'].index
        # print(resNums)
        aHelix = self.dsspGrouper(resNums)
        return aHelix

    def aHelixRange(self):
        '''返回range列表.'''
        aHRange = []
        rangeList = self.getAHelix()
        for i in rangeList:
            aHRange.append(range(i[0], i[1]+1))
        return aHRange


if __name__ == '__main__':
    dsspNum = 0
    matpath = 'F:\\GraduationProject\\production\\matPNG\\matPNG_01\\images\\train'
    for dir, subdir, files in os.walk(matpath):
        for png in files:
            pdbID = png[:-4]
            dR = readDSSP(pdbID)
            dsspNum += len(dR.getAHelix())
    print(dsspNum)
    # dR = readDSSP('1jcn')
    # print(dR.getAHelix())
    # print(dR.aHelixRange())
    # print(dR.dsspFinder())
    # print(dR.dsspMover())
