from application import application
from src.funcs.dirWalker import getPDBID, getDSSP
from src.funcs.pickleOperater import pickleOP
from src.visualPlt.checksPloter import pltChecks


if __name__ == '__main__':
    start = 0
    end = 4
    overWrite = False
    pickle = pickleOP()
    scoreRates = []
    scoreValues = []
    simNums = {"(0,0.5)": 0, "(0.5,0.8)": 0, "(0.8,1)": 0}
    scoreNums = {"(0,0.5)": 0, "(0.5,0.8)": 0, "(0.8,1)": 0}

    dsspNum = 0
    dssps = getDSSP(start, end)

    count=0
    for dssp in dssps:
        if count < 1:
            count+=1
            continue
        path = list(dssp.keys())[0]
        print(path)
        pdbIDs = dssp[path]
        # count = 0
        for pdbID in pdbIDs:
            # count += 1
            # if count == 151:
            #     break

            app = application(pdbID, overWrite, path)

            if bool(app) == True:
                dsspNum += len(app.aE.eA.dS.aR)
                app.doMatPNG()
                # app.doAHelixPNGs()
                app.aHelixFeatures()
                # app.checkStatis()
                simNum = app.simNum()

                simNums["(0,0.5)"] += simNum["(0,0.5)"]
                simNums["(0.5,0.8)"] += simNum["(0.5,0.8)"]
                simNums["(0.8,1)"] += simNum["(0.8,1)"]
                scoreRates.append(app.scoreRater())
                scoreValues.append(app.scoreValuer())
        break
    values = 0
    nums = 0
    rates = 0
    for scoreRate in scoreRates:
        pdb, rate = scoreRate.popitem()
        if rate < 0.5:
            scoreNums["(0,0.5)"] += 1
        elif 0.5 <= rate < 0.8:
            scoreNums["(0.5,0.8)"] += 1
        else:
            scoreNums["(0.8,1)"] += 1

        rates += rate
        print('{}的二级结构范围指定的相似度为{}'.format(pdb, rate))

    for scoreValue in scoreValues:
        num, value = scoreValue.popitem()
        nums += num
        values += value

    sample = len(scoreRates)
    meanscore = rates/sample

    meanValue = values/nums
    print('本次运行一共有', sample, '个样本，每个样本指定二级结构范围的平均相似度得分为', meanscore)
    print('其中，DSSP中有', dsspNum, '个α-螺旋，程序一共指定有',
          nums, '个α-螺旋，指定得出的平均相似度得分为', meanValue)
    print('指定得到的α-螺旋中，有', simNums["(0.8,1)"], '个相似度大于80%，有',
          simNums["(0.5,0.8)"], '个大于50%，有', simNums["(0,0.5)"], '个小于50%，')

    # pickleName = '0000_statCheck'
    # steps = [1, 2, 3]
    # allchecks = pickle.loadPickle(pickleName)
    # for step in steps:
    #     pltChecks(step, allchecks[step])

    pickleName = '0000_simNums'
    pickle.savePickle(simNums, pickleName, str(count+1))
    # plotPie(simNums, "指定结果的相似度情况")

    pickleName = '0000_scoreNums'
    pickle.savePickle(scoreNums, pickleName, str(count+1))
    # plotPie(scoreNums, "指定结果的得分分布")
