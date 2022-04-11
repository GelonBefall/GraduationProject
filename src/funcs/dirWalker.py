import os


def getPDBID():
    __pdbPath = "./materials/pdb/"
    pdbIDs = []
    for root, dirs, files in os.walk(__pdbPath):
        for file in files:
            pdbID = os.path.splitext(file)[0]
            pdbIDs.append(pdbID)
    # print(pdbIDs)
    return pdbIDs

def getDSSPID():
    __dsspPath = "./materials/dssp/"
    dsspIDs = []
    for root, dirs, files in os.walk(__dsspPath):
        for file in files:
            dsspID = os.path.splitext(file)[0]
            dsspIDs.append(dsspID)
    # print(pdbIDs)
    return dsspIDs
