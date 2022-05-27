from src.funcs.accuracyRater import accuRater
from src.funcs.pickleOperater import pickleOP
from src.funcs.labelRegainer import reagainLabels
from src.funcs.dsspReader import readDSSP
# from src.visualPlt.checksPloter import pltChecks

def getRecognSimilarity(pdbID, recognRange):
    reader=readDSSP(pdbID)
    dsspRange=reader.getAHelix()
    aR=accuRater(pdbID,dsspRange,recognRange)
    recognSimilarity=aR.getSims()
    recognSimilarity['dsspNum']=len(dsspRange)

    return recognSimilarity

def getRecSims():
    recgonRanges=reagainLabels()
    sims = {"(0,0.5)": 0, "(0.5,0.8)": 0, "(0.8,1)": 0, 'dsspNum':0}
    for pdbID in recgonRanges.keys():
        recgonRange=recgonRanges[pdbID]
        sim = getRecognSimilarity(pdbID, recgonRange)
        sims["(0,0.5)"] += sim["(0,0.5)"]
        sims["(0.5,0.8)"] += sim["(0.5,0.8)"]
        sims["(0.8,1)"] += sim["(0.8,1)"]
        sims["dsspNum"] += sim['dsspNum']
    print(sims)


if __name__ == '__main__':
    
    getRecSims()