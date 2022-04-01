from src.funcs.pngMaker import makePNG


class makeAHelixPNG(makePNG):
    def plotDisPNG(self, clrMatrix, MatrixLen, pdbID):
        pngPath="./production/png/aHelixPNG/"
        self._pngPlot(clrMatrix, MatrixLen, pdbID, pngPath)