from application import application
from src.funcs.dirWalker import getPDBID, getDSSP


if __name__ == '__main__':
    start = 0
    end = 1
    overWrite = False
    accuRates = []
    dssps = getDSSP(start, end)
    values = 0

    count = 0
    for dssp in dssps:
        path = list(dssp.keys())[0]
        print(path)
        pdbIDs = dssp[path]

        for pdbID in pdbIDs:
            count += 1
            if count == 151:
                break
            app = application(pdbID, overWrite, path)
            if bool(app) == True:
                app.doMatPNG()
                app.doAHelixPNGs()
                app.aHelixFeatures()
                accuRates.append(app.getAccuRate())
        break

    for accuRate in accuRates:
        key, value = accuRate.popitem()
        values += value
        print('{}的二级结构范围指定的相似度为{}'.format(key, value))

    num = len(accuRates)
    meanAccu = values/num
    print('一共有', num, '个样本，指定二级结构范围的平均相似度为', meanAccu)
