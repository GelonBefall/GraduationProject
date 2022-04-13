import os
import sys
import numpy
import PIL.Image as Image

from src.operateOfPNG import pngInit


class readPNG(pngInit):
    def loadGrayMat(self, pngFile):
        if not os.path.exists(pngFile):
            sys.exit('PNG文件不存在，无法读取！')
        else:
            src= Image.open(pngFile)
            grayMat = numpy.array(src)
        return grayMat


if __name__=='__main__':
    pngfile='.\\production\\png\\matPNG\\1a4f.png'
    reader=readPNG()
    gM=reader.loadGrayMat(pngfile)
    print(gM)
