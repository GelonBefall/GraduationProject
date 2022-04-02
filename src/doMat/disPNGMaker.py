from src.funcs.pngMaker import makePNG


class makeDisPNG(makePNG):
    def disPlot(self, clrMatrix, MatLen, pdbID:str):
        pngPath="./production/png/matPNG/"
        self._pngPlot(clrMatrix, MatLen, pdbID, pngPath)