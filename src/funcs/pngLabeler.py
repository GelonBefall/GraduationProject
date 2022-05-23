import os

from src.funcs.pdbReader import readPDB
from src.funcs.dsspReader import readDSSP
from src.funcs.dirWalker import getPNG


def labelPNG(pdbID, labelPath):
    Dreader = readDSSP(pdbID)
    Preader=readPDB(pdbID)
    dssps=Dreader.getAHelix()
    for dssp in dssps:
        site=((dssp[1]+dssp[0]+2)/2)/Preader.CAAmount
        sizeRate=(dssp[1]-dssp[0])/Preader.CAAmount

        labelFile=os.path.join(labelPath, pdbID+".txt")
        labelFile=open(labelFile, 'a+')
        labelFile.writelines("0 "+str(site)+" "+ str(site)+" "+str(sizeRate)+" "+str(sizeRate)+'\n')
        labelFile.close()


def labelPNGs(whitchDir):
    __matPath = os.path.join(os.getcwd(), "production/matPNG/")
    subDir = "matPNG_{:0>2d}/".format(whitchDir)
    __matPath = os.path.join(__matPath, subDir)

    __labelPath=os.path.join(os.getcwd(), "production/label/")
    subDir = "label_{:0>2d}/".format(whitchDir)
    __labelPath = os.path.join(__labelPath, subDir)

    pdbIDs =getPNG(__matPath)
    for pdbID in pdbIDs:
        labelPNG(pdbID, __labelPath)


if __name__=='__main__':
    labelPNGs(2)
