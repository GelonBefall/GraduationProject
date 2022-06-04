import sys

from application import application
from src.funcs.dirWalker import getDSSP
from src.funcs.pickleOperater import pickleOP
# from src.visualPlt.checksPloter import pltChecks


if __name__ == '__main__':
    start = 0
    end = 99
    overWrite = False
    pickle = pickleOP()

    dsspNum = 0
    dssps = getDSSP(start, end)

    count=0
    for dssp in dssps:
        # if count < 6: #6
        #     count+=1
        #     continue
        # else:
        #     sys.exit()
        path = list(dssp.keys())[0]
        print(path)
        pdbIDs = dssp[path]
        sims = {"(0,0.5)": 0, "(0.5,0.8)": 0, "(0.8,1)": 0, 'dsspNum':0}

        for pdbID in pdbIDs:
            app = application(pdbID, overWrite, path)

            if bool(app) == True:
                # dsspNum += len(app.aE.eA.dS.aR)
                # app.doMatPNG()
                app.doAHelixPNGs()
                # sim = app.getMyAssignSimilarity()
                # sims["(0,0.5)"] += sim["(0,0.5)"]
                # sims["(0.5,0.8)"] += sim["(0.5,0.8)"]
                # sims["(0.8,1)"] += sim["(0.8,1)"]
                # sims["dsspNum"] += len(app.aE.eA.dS.aR)
                # app.checkStatis()
            else:
                continue

        # pickleName = '00'+str(count+1)+'_sims'
        # pickle.savePickle(sims, pickleName, 'assign', overWrite=True) #str(count+1)
        break
    print('done')
    # app.doAHelixPNGs()
                # app.aHelixFeatures()
                # app.checkStatis()
                
                
                # scoreRates.append(app.scoreRater())
                # scoreValues.append(app.scoreValuer())
    # values = 0
    # nums = 0
    # rates = 0
    # for scoreRate in scoreRates:
    #     pdb, rate = scoreRate.popitem()
    #     if rate < 0.5:
    #         scoreNums["(0,0.5)"] += 1
    #     elif 0.5 <= rate < 0.8:
    #         scoreNums["(0.5,0.8)"] += 1
    #     else:
    #         scoreNums["(0.8,1)"] += 1

    #     rates += rate
    #     print('{}的二级结构范围指定的相似度为{}'.format(pdb, rate))

    # for scoreValue in scoreValues:
    #     num, value = scoreValue.popitem()
    #     nums += num
    #     values += value

    # sample = len(scoreRates)
    # meanscore = rates/sample

    # meanValue = values/nums
    # print('本次运行一共有', sample, '个样本，每个样本指定二级结构范围的平均相似度得分为', meanscore)
    # print('其中，DSSP中有', dsspNum, '个α-螺旋，程序一共指定有',
    #       nums, '个α-螺旋，指定得出的平均相似度得分为', meanValue)
    # print('指定得到的α-螺旋中，有', simNums["(0.8,1)"], '个相似度大于80%，有',
    #       simNums["(0.5,0.8)"], '个大于50%，有', simNums["(0,0.5)"], '个小于50%，')

    # pickleName = '0000_statCheck'
    # steps = [1, 2, 3]
    # allchecks = pickle.loadPickle(pickleName)
    # for step in steps:
    #     pltChecks(step, allchecks[step])

    # pickleName = '0000_simNums'
    # pickle.savePickle(simNums, pickleName, str(count+1))
    # # plotPie(simNums, "指定结果的相似度情况")

    # pickleName = '0000_scoreNums'
    # pickle.savePickle(scoreNums, pickleName, str(count+1))
    # # plotPie(scoreNums, "指定结果的得分分布")
