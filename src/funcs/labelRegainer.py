import os
from src.operateOfPNG.pngReader import readPNG


def reagainLabel(pdbID, labelFile):
    # matPath='F:\\GraduationProject\\production\\matPNG\\matPNG_03'
    matPath = 'F:\\GraduationProject\\production\\trainPNG\\2\\images\\val'
    matFile = os.path.join(matPath, pdbID+'.png')
    reader = readPNG()
    grayMat = reader.loadGrayMat(matFile)

    recgonRanges = []
    if type(grayMat) != bool:
        lF = open(labelFile, 'r')#,encoding='utf8'
        for line in lF:
            line = line[:-1].split(' ')
            # cls=line[0]
            center = (float(line[1])+float(line[2]))/2
            proportion = (float(line[3])+float(line[4]))/2
            centerSite = grayMat.shape[0]*center
            lenth = grayMat.shape[0]*proportion
            recgon = (int((centerSite-lenth/2))-1, int((centerSite+lenth/2))-1)
            if (recgon[1]-recgon[0]) < 3:
                continue
            else:
                recgonRanges.append(recgon)

    if len(recgonRanges) == 0:
        return 0
    else:
        return recgonRanges


def reagainLabels():
    recgonRanges = {}
    labelPath = 'F:\\GraduationProject\\yolov5\\runs\\detect\\a-Helix3\\labels\\'
    # labelPath = 'F:\\GraduationProject\\production\\trainPNG\\1\\labels\\val'
    for dirPath, subdirs, subfiles in os.walk(labelPath):
        # for subdir in subdirs:
        #     subdir=Path(subdir)
        #     subfiles = subdir.glob('*.txt')
        for dssp in subfiles:
            pdbID = dssp[:4]
            recgonRange = reagainLabel(pdbID, os.path.join(labelPath, dssp))
            if recgonRange == 0:
                continue
            else:
                recgonRanges[pdbID] = recgonRange
                # print(recgonRange)
    return recgonRanges


if __name__ == '__main__':
    # print(reagainLabels())
    labelPath='F:\\GraduationProject\\yolov5\\runs\\detect\\a-Helix2\\labels\\'
    # labelPath = 'F:\\GraduationProject\\production\\trainPNG\\1\\labels\\val'
    pdbID = '1jcn'
    dssp = pdbID+'.txt'
    print(reagainLabel(pdbID, os.path.join(labelPath, dssp)))
