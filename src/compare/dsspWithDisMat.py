from src.funcs.dsspReader import dsspReader
from src.MatrixAndPNG import matrixExecuter

class dWD:
    def __init__(self, pdbID):
        self.dR=dsspReader(pdbID)
        self.mE=matrixExecuter(pdbID)
    # aHelix=
    
    def calAHelixDis(self):
        aHelix=self.dR.getAHelix()
        disMat=self.mE.LASMat()
        disInfo={}
        for i in aHelix:
            disInfo[(i[0],i[1])]=disMat[i[0]][i[1]]
        return disInfo


if __name__=='__main__':
    dWD1=dWD(pdbID='1a4f')
    print(dWD1.calAHelixDis())