from application import application
from src.funcs.dirWalker import getPDBID, getDSSPID

if __name__ == '__main__':

    overWrite = False
    accuRates=[]
    for pdbID in getDSSPID():
        app = application(pdbID, overWrite)
        if bool(app) == True:
            app.doMatPNG()
            app.doAHelixPNGs()
            app.aHelixFeatures()
            accuRates.append(app.getAccuRate())
    for _ in accuRates:
        print(_)
            
