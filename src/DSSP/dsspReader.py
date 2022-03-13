import os

from collections import deque


class dsspReader:
    def __init__(self, pdbID: str):
        self.dsspID = pdbID.lower()
        self.__dsspPath = "./materials/dssp/"
        self.__dsspFile = os.path.join(
            self.__dsspPath, "{}.dssp".format(self.dsspID))

    def __str__(self):
      return str(self.getAHelix())
    
    def dsspExist(self):
        if os.path.exists(self.__dsspFile):
            print("DSSP file exist!")
            return 0
        else:
            print("DSSP file doesn't exist!")
            return 1

    def getAHelix(self):
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


if __name__ == '__main__':
    # dR = dsspReader('1a4f')
    dR = dsspReader('1faw')
    print(dR)
