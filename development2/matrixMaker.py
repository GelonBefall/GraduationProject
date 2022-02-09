from unittest import result
from Bio.PDB.PDBParser import PDBParser
from Bio import PDB
import numpy as np
import os
import sys
import requests
from collections import deque

from sqlOperate import sqlOP


class makeMatrix:
  def __init__(self, pdb_id = "2erk", database='atomdistance'):
      self.pdbID = pdb_id
      self.database = database
      self.pdbPath = "./materials/pdb/"
      self.pdbFile = os.path.join(self.pdbPath, "{}.pdb".format(self.pdbID))
      self.p = PDBParser() #可选参数PERMISSIVE=1时忽略错误
      sql=sqlOP(pdbID=pdb_id,database=database)
      
  def pdbExist(self):
    if os.path.exists(self.pdbFile):
      print("PDB file exist!")
      return 0
    else:
      print("PDB file doesn't exist!")
      return 1

  def pdbDownload(self):
    url = "https://files.rcsb.org/download/" + self.pdbID + ".pdb"
    r = requests.get(url)
    print(r)
    if r:
      with open(self.pdbFile,"wb") as pdbFile:
        pdbFile.write(r.content)
    else:
      isPDBExist=self.pdbExist()
      if isPDBExist==0:
        return 0
      else:
        print("PDB file doesn't download successfully, please check!")
        return 1

  def CACount(self):
    '''Get CA atoms' count.'''
    structure = self.p.get_structure(self.pdbID, self.pdbFile)
    # atoms = structure.get_atoms()
    residues1 = structure.get_residues()
    count = 0
    for residue1 in residues1:
      if residue1.has_id("CA"):
        count = count + 1
    return count

  def calMatrix(self):
    '''To calculate the distance of CA.'''
    structure = self.p.get_structure(self.pdbID, self.pdbFile)
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
    disMatrix =np.array(disLists)
    return disMatrix

  def trueMatrix(self):
    sql=sqlOP(pdbID=self.pdbID, database=self.database)
    isTableExsit = sql.tableExist()
    # Check the table is existing or not.
    if isTableExsit == 1:
      PDBstatus = self.pdbExist()
      # Check the PDB file is existing or not, and retry three times.
      if PDBstatus==1:
          for i in range(3) :
            DLstatus=self.pdbDownload()
            if DLstatus == 0:
              break
            if i == 2:
              print("The PDB file is not existed or can't be downloaded.")
              sys.exit()
      else:
        pass
    else:
      CACount=self.CACount()
      entryCount = sql.entryCount()

      # To verdict if count fit or not.
      if CACount==entryCount:
        pass


if __name__=='__main__':
  NM=makeMatrix()
  disMatrix=NM.calMatrix()
  print(disMatrix)