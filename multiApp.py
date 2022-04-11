from application import application
from src.funcs.dirWalker import getPDBID, getDSSPID

if __name__ == '__main__':

    overWrite = False
    for pdbID in getDSSPID():
        app = application(pdbID, overWrite)
        if bool(app) == True:
            app.doMatPNG()
            app.doAHelixPNGs()
