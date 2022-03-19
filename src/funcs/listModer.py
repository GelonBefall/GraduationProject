import numpy, os

class listMode:
    def __init__(self) -> None:
        pass
    def modeDis(self, uList):
        if type(uList) != numpy.ndarray:
            uList = numpy.array(uList)
            
        counts = numpy.bincount(uList)
        mode = numpy.argmax(counts)
        return mode

    def modeClr(self, uList):
        colorFile=os.path.join("./materials/rgb/", "gray.rgb")
        mode=self.modeDis(uList)
        colormaps = []
        with open(colorFile) as f:
            for line in f:
                colormaps.append(tuple(map(int,line.split(","))))
        site=mode//3
        return colormaps[site]
        



if __name__ == '__main__':
    a = numpy.array([1, 1, 2, 3, 4, 5, 6, 6, 7, 7, 7])
    lM=listMode()
    print(lM.modeClr(a))
