

# class getAccuRate:
#     def __init__(self) -> None:
#         pass

    
def getAccuRate(pdbID, dsspRange, assignRange):
    accu=0
    lenAssign=len(assignRange)
    for indexA in range(lenAssign):
        assignHelix=assignRange[indexA]
        for indexB in range(len(dsspRange)):
            dsspHelix=dsspRange[indexB]

            if (dsspHelix[0]-2)<=assignHelix[0]<=(dsspHelix[0]+2) and (dsspHelix[1]-2)<=assignHelix[1]<=(dsspHelix[1]+2):
                accu+=1
    value=accu/lenAssign
    accuRate={pdbID:value}
    return accuRate



