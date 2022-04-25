from application import application
from src.funcs.dirWalker import getPDBID, getDSSP


if __name__ == '__main__':
    start = 0
    end = 1
    overWrite = False
    accuRates = []
    accuValues = []
    dssps = getDSSP(start, end)

    for dssp in dssps:
        path = list(dssp.keys())[0]
        print(path)
        pdbIDs = dssp[path]

        for pdbID in pdbIDs:
            count = 0
            count += 1
            if count == 151:
                break
            app = application(pdbID, overWrite, path)
            if bool(app) == True:
                app.doMatPNG()
                app.doAHelixPNGs()
                app.aHelixFeatures()
                accuRates.append(app.accuRater())
                accuValues.append(app.accuValuer())
        break
    values = 0
    nums = 0
    rates = 0
    for accuRate in accuRates:
        pdb, rate = accuRate.popitem()
        rates += rate
        print('{}的二级结构范围指定的相似度为{}'.format(pdb, rate))

    for accuValue in accuValues:
        num, value = accuValue.popitem()
        nums += num
        values += value

    sample = len(accuRates)
    meanAccu = rates/sample
    meanValue = values/nums
    print('本次运行一共有', sample, '个样本，指定二级结构范围的平均相似度为', meanAccu)
    print('本次运行一共指定有', nums, '个α螺旋，指定得出的平均相似度为', meanValue)
