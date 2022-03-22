import os, sys

from collections import deque


class dsspRead:
    def __init__(self, pdbID: str):
        self.dsspID = pdbID.lower()
        self.__dsspPath = "./materials/dssp/"
        self.__dsspFile = os.path.join(
            self.__dsspPath, "{}.dssp".format(self.dsspID))
        # self.dsspExist()

    def __str__(self):
      return str(self.getAHelix())
    
    def dsspExist(self):
        if os.path.exists(self.__dsspFile):
            print("DSSP file exist!")
            return 0
        else:
            # print("DSSP file doesn't exist!")
            sys.exit("DSSP file doesn't exist!")

    def getAHelix(self):
        '''返回α螺旋位置。例如[1, 3]为第二个到第四个α残基。'''
        with open(self.__dsspFile, mode='r') as dF:
            aHelix = deque()
            tmp = []
            for line in dF.readlines():

                line = line.split(" ")
                if "H" not in line:
                    continue
                for _ in range(len(line)):
                    if '' in line:
                        line.remove('')
                    else:
                        break

                if (line[4] == 'H') and len(tmp) < 2:
                    tmp.append(int(line[0]))
                elif (line[4] == 'H') and len(tmp) == 2:
                    tmp[1] = int(line[0])
                else:
                    if tmp != []:
                        tmp[0] -= 1
                        tmp[1] -= 1
                        aHelix.append(tmp)
                        tmp = []
        aHelix = list(aHelix)
        return aHelix

    def aHelixRange(self):
        '''返回range列表.'''
        aHRange=[]
        rangeList=self.getAHelix()
        for i in rangeList:
            aHRange.append(range(i[0], i[1]+1))
        return aHRange


if __name__ == '__main__':
    dR = dsspRead('1a4f')
    # dR = dsspRead('1faw')
    print(dR.aHelixRange())
