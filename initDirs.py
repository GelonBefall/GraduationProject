import os


class makeMyDirs:
    def __init__(self):
        self.cwd = os.getcwd()

    def __mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def makeAll(self):
        self.makeMaterials()
        self.makeProduction()

    def makeProduction(self):
        producPath = os.path.join(self.cwd, "production/")
        self.__mkdir(producPath)
        self.makePNG(producPath)
        self.makePickle(producPath)
        self.makeLabel(producPath)
        self.makeSQLBackup(producPath)

    def makePNG(self, producPath):

        matPath = os.path.join(producPath, "matPNG/")
        self.__mkdir(matPath)
        self.makeMatPNG(matPath)

        aHelixPath = os.path.join(producPath, "aHelixPNG/")
        self.__mkdir(aHelixPath)
        self.makeAHelixPNG(aHelixPath)

    def makeMatPNG(self, matPath):
        for i in range(1, 94):
            subDir = "matPNG_{:0>2d}/".format(i)
            subMatPath = os.path.join(matPath, subDir)
            self.__mkdir(subMatPath)

    def makeAHelixPNG(self, aHelixPath):
        for i in range(1, 94):
            subDir = "aHelix_{:0>2d}/".format(i)
            subMatPath = os.path.join(aHelixPath, subDir)
            self.__mkdir(subMatPath)

    def makePickle(self, producPath):
        picklePath = os.path.join(producPath, 'pickle/')
        self.__mkdir(picklePath)

    def makeLabel(self, producPath):
        labelPath = os.path.join(producPath, 'label/')
        self.__mkdir(labelPath)
        for i in range(1, 94):
            subDir = "label_{:0>2d}/".format(i)
            subLabelPath = os.path.join(labelPath, subDir)
            self.__mkdir(subLabelPath)

    def makeSQLBackup(self, producPath):
        sqlPath = os.path.join(producPath, 'sqlBackUp/')
        self.__mkdir(sqlPath)
    
    def makeMaterials(self):
        materialsPath = os.path.join(self.cwd, "materials/")
        self.makeBig(materialsPath)
        self.makePDB(materialsPath)
        self.makeRGB(materialsPath)
        self.makeRGB(materialsPath)
        self.makeDSSP(materialsPath)

    def makeBig(self, path):
        bigDSSPPath = os.path.join(path, 'big_dssp/')
        self.__mkdir(bigDSSPPath)

        bigPDBPath = os.path.join(path, 'big_pdb/')
        self.__mkdir(bigPDBPath)

    def makePDB(self, materialsPath):
        pdbPath = os.path.join(materialsPath, 'pdb/')
        self.__mkdir(pdbPath)

        for i in range(1, 94):
            subDir = "pdb_{:0>2d}/".format(i)
            subMatPath = os.path.join(pdbPath, subDir)
            self.__mkdir(subMatPath)

    def makeRGB(self, materialsPath):
        rgbPath = os.path.join(materialsPath, 'rgb/')
        self.__mkdir(rgbPath)

    def makeDSSP(self, materialsPath):
        dsspPath = os.path.join(materialsPath, 'dssp/')
        self.__mkdir(dsspPath)


if __name__ == '__main__':
    mkdirs = makeMyDirs()
    # mkdirs.makeProduction()
    mkdirs.makeAll()
