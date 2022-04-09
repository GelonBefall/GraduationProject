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
