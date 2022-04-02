from src.funcs.pngMaker import makePNG


class makeAHelixPNG(makePNG):
    def plotAHelixPNG(self, clrMatrix, matLen, pdbID:str):
        pngPath="./production/png/aHelixPNG/"
        self._pngPlot(clrMatrix, matLen, pdbID, pngPath)