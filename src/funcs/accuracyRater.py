def getAccuRate(pdbID, dsspRange, assignRange):
    accu = 0
    lenAssign = len(assignRange)
    lendssp = len(dsspRange)

    if lenAssign == 0:
        accuRate = {pdbID: 0}
    else:
        for indexA in range(lenAssign):
            '''遍历指定结果'''
            assignHelix = assignRange[indexA]

            for indexB in range(lendssp):
                '''遍历dssp结果'''
                dsspHelix = dsspRange[indexB]

                if (dsspHelix[0]-5) <= assignHelix[0] <= (dsspHelix[0]+5) and (dsspHelix[1]-5) <= assignHelix[1] <= (dsspHelix[1]+5):
                    accu += 1 # 如果指定结果能在指定范围内，准确度增加
                    break
        value = accu/lenAssign
        accuRate = {pdbID: value}

    return accuRate

def getAccuRate2(pdbID, dsspRange, assignRange):
    accu = 0
    lendssp = len(dsspRange)
    lenAssign = len(assignRange)

    if lenAssign == 0:
        accuRate = {pdbID: 0}
    else:
        for indexA in range(lendssp):
            '''遍历dssp结果'''
            dsspHelix = dsspRange[indexA]
            
            for indexB in range(lenAssign):
                '''遍历指定结果'''
                assignHelix = assignRange[indexB]

                if (assignHelix[0]-5) <= dsspHelix[0] <= (assignHelix[0]+5) and (assignHelix[1]-5) <= dsspHelix[1] <= (assignHelix[1]+5):
                    accu += 1 # 如果指定结果能在指定范围内，准确度增加
                    break
        value = accu/lendssp
        accuRate = {pdbID: value}

    return accuRate