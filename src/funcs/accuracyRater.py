class accuRater:
    def __init__(self, pdbID, dsspRange, assignRange):
        self.pdbID = pdbID
        self.dsspRange = dsspRange
        self.assignRange = assignRange

        self.lenAssign = len(assignRange)
        self.lendssp = len(dsspRange)

        self.accu = self.getAccu()

    def getAccu(self):  # ,dsspRange, assignRange
        accu = self.lenAssign

        if self.lenAssign == 0:
            return accu

        for indexA in range(self.lenAssign):
            '''遍历指定结果'''
            assignHelix = self.assignRange[indexA]

            for indexB in range(self.lendssp):
                '''遍历dssp结果'''
                flag = 0
                dsspHelix = self.dsspRange[indexB]

                if (dsspHelix[0]-3) <= assignHelix[0] <= (dsspHelix[0]+3) and (dsspHelix[1]-3) <= assignHelix[1] <= (dsspHelix[1]+3):
                    # accu += 1 # 如果指定结果能在指定范围内，得分增加1
                    flag = 1
                    break
                elif (dsspHelix[0]-1) <= assignHelix[0] < (dsspHelix[1]+1) and (dsspHelix[0]-1) < assignHelix[1] <= (dsspHelix[1]+1):
                    # 如果指定结果能在指定范围内，得分增加百分比
                    score = (assignHelix[1]-assignHelix[0]) / (dsspHelix[1]-dsspHelix[0])
                    accu -= (1-score)
                    flag = 1
                    break
            if flag == 0:
                accu -= 1
        return accu

    def getAccuRate(self):  # , pdbID, dsspRange, assignRange
        # lenAssign = len(assignRange)
        if self.accu == 0:
            return {self.pdbID: 0}
        # accu = getAccu(dsspRange, assignRange)
        # lenAssign = len(assignRange)
        rate = self.accu/self.lenAssign
        accuRate = {self.pdbID: rate}

        return accuRate

    def getAccuValue(self):  # dsspRange, assignRange
        # accu = getAccu(dsspRange, assignRange)
        # lendssp = len(dsspRange)
        # lenAssign = len(assignRange)
        accuValue = {self.lenAssign: self.accu}
        return accuValue
