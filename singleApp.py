from application import application

if __name__ == '__main__':
    pdbID = '103l'
    overWrite = False
    app = application(pdbID, overWrite)
    if bool(app) == True:
        app.doMatPNG()
        app.doAHelixPNGs()
