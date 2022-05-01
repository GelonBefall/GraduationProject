from application import application

if __name__ == '__main__':
    pdbID = '12e8'  # input()1a4f
    overWrite = False
    app = application(pdbID, overWrite)
    accuRates = []
    accuValues=[]
    if bool(app) == True:
        app.doMatPNG()
        app.doAHelixPNGs()
        app.aHelixFeatures()

        rate=app.accuRater()
        accuRates.append(rate)
        accuValues.append(app.accuValuer())

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
#  1a03 12e8 117e 1a02 169l 1a0d 1a0n 1a2b
