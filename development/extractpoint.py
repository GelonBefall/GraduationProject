from Bio.PDB.PDBParser import PDBParser
import numpy
import os
import csv

p = PDBParser() #可选参数PERMISSIVE=1时忽略错误

class calMatrix:
  def __init__(self, pdb_id = "6vw1"):
      self.structure_id = pdb_id
      self.pdbPath = "./materials/pdb/"
      self.csvPath = "./materials/csv/"
      self.pdbFile = os.path.join(self.pdbPath, "{}.pdb".format(self.structure_id))
      self.csvFile = os.path.join(self.csvPath, "{}.csv".format(self.structure_id))

  def isExist(self,file):
    if os.path.exists(file):
      return True
    else :
      return False

  def trueMatrix(self):
    if not self.isExist(self.pdbFile):
        print(self.pdbFile)
        raise ValueError("The PDB file for your input id is not existed or uploaded.")

    if self.isExist(self.csvFile) :
      disfile = open(self.csvFile,"r")
      distanceMatrix = numpy.loadtxt(disfile, delimiter=",", skiprows=0)
      disfile.close()
      return distanceMatrix
    else :
      distanceMatrix=[]
      matrixTemp=[]
      structure = p.get_structure(self.structure_id, self.pdbFile)
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
      numpy.savetxt(self.csvPath+"{}.csv".format(self.structure_id), distanceMatrix, delimiter=',')
      return distanceMatrix

  def maskMatrix(self):
    if not self.isExist(self.pdbFile):
        raise ValueError("The PDB file for your input id is not existed or uploaded.")

    maskCSV = os.path.join(self.csvPath, "{}_mask.csv".format(self.structure_id))
    if self.isExist(maskCSV) :
      disfile = open(self.csvFile,"r")
      maskMatrix = numpy.loadtxt(disfile, delimiter=",", skiprows=0)
      disfile.close()
      return maskMatrix
    elif self.isExist(self.csvFile) :
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
      structure = p.get_structure(self.structure_id, self.pdbFile)
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
    rgbCSV = os.path.join(self.csvPath, "{}_RGB.csv".format(self.structure_id))
    if self.isExist(rgbCSV) :
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
