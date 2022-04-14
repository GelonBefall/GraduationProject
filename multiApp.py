from application import application
from src.funcs.dirWalker import getPDBID, getDSSP

if __name__ == '__main__':
    start=0
    end=1
    overWrite = False
    accuRates = []
    dssps = getDSSP(start, end)
    values = 0

    count=0
    for dssp in dssps:
        count+=1
        if count==500:
            break

        path=list(dssp.keys())[0]
        print(path)
        pdbIDs=dssp[path]

        for pdbID in pdbIDs:
            app = application(pdbID, overWrite,path)
            if bool(app) == True:
                app.doMatPNG()
                app.doAHelixPNGs()
                # app.aHelixFeatures()
                accuRates.append(app.getAccuRate())

    for accuRate in accuRates:
        key, value = accuRate.popitem()
        values += value
        print('{}的二级结构指定正确率为{}'.format(key, value))
        
    meanAccu = values/len(accuRates)
    print('指定二级结构平均正确率为', meanAccu)
