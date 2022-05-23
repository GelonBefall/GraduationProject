from src.funcs.pickleOperater import pickleOP
from src.visualPlt.piePloter import plotPie
from src.visualPlt.linearPloter import plotLinr

def plotCode(x:str):
    pickle =pickleOP()
    pickleName = '0000_simNums'
    simNums = pickle.loadPickle(pickleName,x)
    # plotLinr(simNums, "指定结果的相似度情况",x)
    plotPie(simNums, "指定结果的相似度情况",x)

    pickleName = '0000_scoreNums'
    scoreNums = pickle.loadPickle(pickleName,x)
    # plotLinr(scoreNums, "指定结果的得分分布",x)
    plotPie(scoreNums, "指定结果的得分分布",x)

if __name__=='__main__':
    plotCode("1")