from Bio.PDB.PDBParser import PDBParser
from Bio import PDB
import numpy
import os
import sys
import csv
import requests

from sqlOperate import sqlOP

p = PDBParser() #可选参数PERMISSIVE=1时忽略错误

class calMatrix:
  def __init__(self, pdb_id = "2erk"):
      self.pdbID = pdb_id
      self.pdbPath = "./materials/pdb/"
      self.csvPath = "./materials/"
      self.pdbFile = os.path.join(self.pdbPath, "{}.pdb".format(self.pdbID))
      self.csvFile = os.path.join(self.csvPath, "{}.csv".format(self.pdbID))

  def pdbDownload(self):
    url = "https://files.rcsb.org/download/" + self.pdbID + ".pdb"
    r = requests.get(url)
    print(r)
    if r:
        with open(self.pdbFile,"wb") as pdbFile:
            pdbFile.write(r.content)
        if os.path.exists(self.pdbFile):
          print("Download complete!")
          return 0
    else:
        if not os.path.exists(self.pdbFile):
            print("File don't exists, please check!")
            sys.exit()
        else:
          return 0

  def new_trueMatrix(self):

  def trueMatrix(self):

    #检查文件是否存在，并三次重试
    if not os.path.exists(self.pdbFile):
        for i in range(3) :
          if self.pdbDownload() == 0:
            break
          if i == 2:
            print("The PDB file for your input id is not existed or can't be downloaded.")
            sys.exit()

    if os.path.exists(self.csvFile) :
      disfile = open(self.csvFile,"r")
      distanceMatrix = numpy.loadtxt(disfile, delimiter=",", skiprows=0)
      disfile.close()
      return distanceMatrix
    else :
      distanceMatrix=[]
      matrixTemp=[]
      structure = p.get_structure(self.pdbID, self.pdbFile)
      # atoms = structure.get_atoms()
      residues1 = structure.get_residues()
      for residue1 in residues1:
        residues2 = structure.get_residues()
        if residue1.has_id("CA"):
          CA1 = residue1["CA"]
        else:
          continue
        for residue2 in residues2:
          if residue2.has_id("CA"):
            CA2 = residue2["CA"]
            distance = CA1 - CA2
            matrixTemp.append(distance)
            # print(matrixTemp)
          else :
              continue
        distanceMatrix.append(matrixTemp)
        # print(distanceMatrix)
        matrixTemp=[]
      numpy.savetxt(self.csvPath+"{}.csv".format(self.pdbID), distanceMatrix, delimiter=',')
      return distanceMatrix

  def maskMatrix(self):
    if not os.path.exists(self.pdbFile):
        raise ValueError("The PDB file for your input id is not existed or uploaded.")

    maskCSV = os.path.join(self.csvPath, "{}_mask.csv".format(self.pdbID))
    if os.path.exists(maskCSV) :
      disfile = open(self.csvFile,"r")
      maskMatrix = numpy.loadtxt(disfile, delimiter=",", skiprows=0)
      disfile.close()
      return maskMatrix
    elif os.path.exists(self.csvFile) :
      disfile = open(self.csvFile,"r")
      maskMatrix = numpy.loadtxt(disfile, delimiter=",", skiprows=0)
      disfile.close()
      for row in range(0,len(maskMatrix)):
        for column in range(0,len(maskMatrix[row])):
          if maskMatrix[row][column] > 20:
            maskMatrix[row][column] = 20
    else :
      maskMatrix=[]
      matrixTemp=[]
      structure = p.get_structure(self.pdbID, self.pdbFile)
      # atoms = structure.get_atoms()
      residues1 = structure.get_residues()
      for residue1 in residues1:
        residues2 = structure.get_residues()
        if residue1.has_id("CA"):
          CA1 = residue1["CA"]
        else:
          continue
        for residue2 in residues2:
          if residue2.has_id("CA"):
            CA2 = residue2["CA"]
            distance = CA1 - CA2
            if distance > 20:
              distance=20
            matrixTemp.append(distance)
            # print(matrixTemp)
          else :
              continue
        maskMatrix.append(matrixTemp)
        matrixTemp=[]
    numpy.savetxt(maskCSV, maskMatrix, delimiter=',')
    return maskMatrix

  def grayRGBMatrix(self, mask = True, level = 10):
    '''if mask = True, function will use  maskMatrix; else it will use trueMatrix'''
    rgbCSV = os.path.join(self.csvPath, "{}_RGB.csv".format(self.pdbID))
    if os.path.exists(rgbCSV) :
      disfile = open(self.csvFile,"r")
      maskMatrix = numpy.loadtxt(disfile, delimiter=",", skiprows=0)
      disfile.close()
      return maskMatrix
    if mask == True:
      distanceMatrix = self.maskMatrix()
      rgbMatrix = []
      with open(rgbCSV,'w', newline='') as file:
        writer = csv.writer(file)
        for row in range(0,len(distanceMatrix)):
          matrixTemp=[]
          for column in range(0,len(distanceMatrix[row])):
            try:
              RGB = 255 - level*(20 - int(distanceMatrix[row][column]))
              if RGB < 0:
                raise ValueError("Your level value is too big.")
              matrixTemp.append((RGB, RGB, RGB))
              # print(matrixTemp)
            except Exception:
              print(Exception)
              break
          writer.writerow(matrixTemp)
          rgbMatrix.append(matrixTemp)
          
      # numpy.savetxt(rgbCSV, rgbMatrix, delimiter=',')
      return rgbMatrix
    elif mask == False:
      pass
    else :
      raise ValueError("Your level value is invalid.")


if __name__=='__main__':
  cal=calMatrix()
  distanceMatrix=cal.trueMatrix()
  print(distanceMatrix)
