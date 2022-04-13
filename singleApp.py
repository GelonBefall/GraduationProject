from application import application

if __name__ == '__main__':
    pdbID = '13gs'  # input()
    overWrite = False
    app = application(pdbID, overWrite)
    accuRates = []
    values = 0

    if bool(app) == True:
        app.doMatPNG()
        app.doAHelixPNGs()
        app.aHelixFeatures()
        accuRates.append(app.getAccuRate())

        for accuRate in accuRates:
            key, value = accuRate.popitem()
            values += value
            print('{}的正确率为{}'.format(key, value))
# 12e8 1a03