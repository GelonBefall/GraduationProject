from src.funcs.pngMaker import makePNG


class makeDisPNG(makePNG):
    def disPlot(self, clrMatrix, MatrixLen, pdbID):
        pngPath="./production/png/matPNG/"
        self._pngPlot(clrMatrix, MatrixLen, pdbID, pngPath)