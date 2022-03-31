import os
import sys
import png

class makePNG:
    def __init__(self, colorFilename="gray.rgb"):
        
        self.__rgbPath="./materials/rgb/"
        self.__colormapInit(colorFilename)

    def colormapExist(self, colorFile):
        if os.path.exists(colorFile):
          print("The RGB file exist!")
          return 0
        else:
          print("The RGB doesn't exist!")
          return 1

    def __colormapInit(self, colorFilename="gray.rgb"):
        colorFile=os.path.join(self.__rgbPath, colorFilename)
        RGBstatus=self.colormapExist(colorFile)
        if RGBstatus==1:
            sys.exit()

        colormaps = []
        with open(colorFile) as f:
            for line in f:
                # colormapMatrix.insert(0,list(map(int,line.split())))
                colormaps.append(tuple(map(int,line.split(","))))
        self.colormaps = colormaps
        # self.colormaps = np.array(colormaps)
        # print(self.colormaps)

    def pngPlot(self, clrMatrix, MatrixLen, pdbID):
        pngPath="./production/png"
        pngFile=os.path.join(pngPath, pdbID+".png")
        pngData = []
        for i in range(MatrixLen):
            tmp = []
            for j in range(MatrixLen):
                #Each line in colormap has three values,R,G,B。
                for element in clrMatrix[i][j]:
                    tmp.append(element)
            pngData.append(tuple(tmp))
        
        f = open(pngFile,"wb")
        w = png.Writer(MatrixLen, MatrixLen, greyscale=False)
        w.write(f,pngData)
        f.close()

if __name__=='__main__':
    mkPNG=makePNG()
    print(mkPNG.colormaps)