import numpy, os

class listMode:
    def __init__(self) -> None:
        self.colormaps = []
        colorFile=os.path.join("./materials/rgb/", "gray.rgb")
        with open(colorFile) as f:
            for line in f:
                self.colormaps.append(tuple(map(int,line.split(","))))

    def modeDis(self, uList):
        if type(uList) != numpy.ndarray:
            uList = numpy.array(uList)

        uList=uList.astype(int)    
        counts = numpy.bincount(uList)
        mode = numpy.argmax(counts)
        return mode

    def modeClr(self, uList):
        
        mode=self.modeDis(uList)
        
        site=9-mode//3
        return self.colormaps[site]

    def modeDisRange(self, uList:numpy.ndarray):
        aHRange=[]
        aHRange.append(uList.min())
        aHRange.append(uList.max())
        return aHRange

if __name__ == '__main__':
    a = numpy.array([1, 1, 2, 3, 4, 5, 6, 6, 7.1, 7.2, 7.3])
    lM=listMode()
    print(lM.modeClr(a))
