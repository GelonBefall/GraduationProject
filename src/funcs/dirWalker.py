import os
from pathlib import Path


def getPDBID():
    __pdbPath = "./materials/pdb/"
    pdbIDs = []
    for root, dirs, files in os.walk(__pdbPath):
        for file in files:
            pdbID = os.path.splitext(file)[0]
            pdbIDs.append(pdbID)
    # print(pdbIDs)
    return pdbIDs


def getDSSP(start=0, end=None):
    '''Return a list include dicts which contain pdbIDs in certain path.'''

    __dsspPath = "./materials/dssp/"
    wholeDsspIDs = []

    for root, dirs, files in os.walk(__dsspPath):

        dirs = dirs[start:end]
        for __subPath in dirs:
            __subPath = os.path.join(root, __subPath)+'/'
            dsspTmps = []

            # for subroot, subdirs, subfiles in os.walk(__subPath):
            subPath = Path(__subPath)
            subfiles = subPath.glob('*.dssp')
            for dssp in subfiles:
                dsspID = dssp.stem
                dsspTmps.append(dsspID)  # 收集该目录下的所有dssp

            singleDsspIDs = {__subPath: dsspTmps}  # 字典记录目录名和下面的所有dsspid

            wholeDsspIDs.append(singleDsspIDs)

    return wholeDsspIDs


if __name__ == '__main__':
    getDSSP()
