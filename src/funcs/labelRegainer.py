import os
from pathlib import Path
from src.operateOfPNG.pngReader import readPNG

def reagainLabel(pdbID, matPath, labelFile):
    matPath='F:\\GraduationProject\\production\\matPNG\\matPNG_03'
    matFile=os.path.join(matPath, pdbID+'.png')
    reader=readPNG()
    grayMat=reader.loadGrayMat(matFile)
    if type(grayMat) != bool:
        lF=open(labelFile,'r')
        for line in lF:
            line.split(' ')

def reagainLabels(x):
    # dsspTmps=[]
    # dirPath=Path()
    for dirPath,subdirs,subfiles in os.walk('F:\\GraduationProject\\yolov5\\runs\\detect\\a-Helix\\label\\'):
        for subdir in subdirs:
            subdir=Path(subdir)
            subfiles = subdir.glob('*.txt')
            for dssp in subfiles:
                pdbID = dssp.stem
                