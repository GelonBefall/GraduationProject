from src.findAHelix.aHelixExtractr import extractAHelix
from src.findAHelix.aHelixPNGMaker import makeAHelixPNG

class aHelixExecute:
    def __init__(self, pdbID:str):
        self.eA=extractAHelix(pdbID)
        self.mH=makeAHelixPNG(pdbID)
    
    def doAHelixPNG(self):
        self.mH.plotAHelixPNG()