from src.findAHelix import aHelixExecute


class application:
    def __init__(self, pdbID: str, overWrite=False):
        self.aE = aHelixExecute(pdbID, overWrite)

    def __bool__(self):
        if type(self.aE.eA.dS.disMatrix) == bool:
            return False
        else:
            return True

    def doMatPNG(self):
        return self.aE.eA.dS.mE.doDisPNG()

    def doAHelixPNGs(self):
        return self.aE.doAHelixPNGs()
