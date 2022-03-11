import os


class dsspReader:
    def __init__(self, pdbID):
        self.dsspbID = pdbID
        self.__dsspPath = "./materials/dssp/"
        self.__dsspFile = os.path.join(self.__dsspPath, "{}.dssp".format(self.dsspID))

    def dsspExist(self):
        if os.path.exists(self.pdbFile):
          print("PDB file exist!")
          return 0
        else:
          print("PDB file doesn't exist!")
          return 1