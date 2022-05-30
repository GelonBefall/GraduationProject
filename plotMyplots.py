from src.funcs.pickleOperater import pickleOP
# from src.visualPlt.piePloter import plotPie
from src.visualPlt.linearPloter import plotstatLinr,plotPRCLinr

# dict1 = {'a': 1, 'b': 2}
# dict2 = {'a': 2, 'c': 3}
# print(dict(Counter(dict1) + Counter(dict2)))


def getStat(x:str, genre):
    pickle =pickleOP()
    pickleName = '00'+x+'_sims'
    simNums = pickle.loadPickle(pickleName, genre)#,x
    print(simNums)
    return simNums
    # plotLinr(simNums, "指定结果的相似度情况",x)
    # plotPie(simNums, "指定结果的相似度情况",x)

    # pickleName = '00'+x+'_scoreNums'
    # scoreNums = pickle.loadPickle(pickleName)#,x
    # # plotLinr(scoreNums, "指定结果的得分分布",x)
    # # plotPie(scoreNums, "指定结果的得分分布",x)
    
def plotAssignlinrs(genre):
    stats=[]
    for i in range(1,7):
        stats.append(getStat(str(i),genre))
    plotstatLinr(stats)
    # plotPRCLinr(stats)
        

if __name__=='__main__':
    # getStat("1","recogn")
    plotAssignlinrs('assign')
    # plotAssignlinrs("recogn")
    