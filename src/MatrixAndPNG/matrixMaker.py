import numpy as np
import os
import sys
import requests

from collections import deque
from Bio.PDB.PDBParser import PDBParser
# from Bio import PDB

class makeMatrix:
    '''Before using other function, better to execute "calMatrix()" first.'''
    def __init__(self, pdbID = "2erk"):
        self.pdbID = pdbID
        self.__pdbPath = "./materials/pdb/"
        self.__pdbFile = os.path.join(self.__pdbPath, "{}.pdb".format(self.pdbID))

        initStatus=self.initPDBFile()
        if initStatus==0:
          self.p = PDBParser() #可选参数PERMISSIVE=1时忽略错误
          self.CAAmount=self.CACount()
        else:
          print("The .pdb file is not existed or can't be downloaded, init class fail.")
          sys.exit()

    def initPDBFile(self):
        pdbExist=self.pdbExist()
        if pdbExist==0:
          return 0
        else:
          dlStatus=self.__pdbDownload()
          if dlStatus==0:
            return 0
          else:
            return 1

    def pdbExist(self):
        if os.path.exists(self.__pdbFile):
          print("PDB file exist!")
          return 0
        else:
          print("PDB file doesn't exist!")
          return 1

    def __pdbDownload(self):
        url = "https://files.rcsb.org/download/" + self.pdbID + ".pdb"
        r = requests.get(url)
        print(r)
        for i in range(3) :
          if r:
            print("Downloading {}...".format(self.pdbID))
            with open(self.__pdbFile,"wb") as pdbFile:
              pdbFile.write(r.content)
            isPDBExist=self.pdbExist()
            if isPDBExist==0:
              print("PDB file download successfully!")
              return 0
          else:
            isPDBExist=self.pdbExist()
            if isPDBExist==0:
              return 0
          if i==2:
            print("PDB file doesn't download successfully, please check!")
            return 1

    def CACount(self):
        '''Get CA atoms' count.'''
        structure = self.p.get_structure(self.pdbID, self.__pdbFile)
        # atoms = structure.get_atoms()
        residues = structure.get_residues()
        count = 0
        for residue in residues:
          if residue.has_id("CA"):
            count = count + 1
        print("The CAAmount of {} is {}.".format(self.pdbID,count))
        return count

    def calMatrix(self):
        '''To calculate the distance of CA.'''
        structure = self.p.get_structure(self.pdbID, self.__pdbFile)
        disLists = deque()
        ListsTemp= deque()

        residues1 = structure.get_residues()
        for residue1 in residues1:
          residues2 = structure.get_residues()
          if residue1.has_id("CA"):
            CA1 = residue1['CA']
          else:
              continue

          for residue2 in residues2:
            if residue2.has_id("CA"):
              CA2 = residue2["CA"]
              distance = CA1 - CA2
              ListsTemp.append(distance)
              # print(ListsTemp)
            else:
                continue

          disLists.append(ListsTemp)
          # print(disLists)
          ListsTemp=deque()
        self.disMatrix =np.array(disLists)
        # return disMatrix

    def grayMatrix(self, disMatrix, clrmaps):
        clrLists=deque()

        for i in range(self.CAAmount):
          tmp=deque()

          for m in range(self.CAAmount):
            checked=0
            if disMatrix[i][m]>=19:
              checked=19
            else:
              checked=round(disMatrix[i][m])
            tmp.append(clrmaps[19-checked])
          clrLists.append(tmp)

        clrMatrix=np.array(clrLists)
        return clrMatrix


if __name__=='__main__':
    NM=makeMatrix()
    disMatrix=NM.calMatrix()
    print(disMatrix)