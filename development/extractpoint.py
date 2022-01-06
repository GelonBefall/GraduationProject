from Bio.PDB.PDBParser import PDBParser
p = PDBParser() #可选参数PERMISSIVE=1时忽略错误

def calMatrix(structure_id = "6vw1"):
  distanceMatrix=[]
  matrixTemp=[]
  filename = "./materials/"+structure_id+".pdb"
  structure = p.get_structure(structure_id, filename)
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
    distanceMatrix.append(matrixTemp)
    # print(distanceMatrix)
    matrixTemp=[]
  print(len(distanceMatrix))
  return distanceMatrix
  # print(distanceMatrix)


if __name__=='__main__':
  distanceMatrix=calMatrix()
  print(distanceMatrix[0])
