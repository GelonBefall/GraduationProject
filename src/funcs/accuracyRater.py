class accuRater:
    def __init__(self, pdbID, dsspRange, assignRange):
        self.pdbID = pdbID
        self.dsspRange = dsspRange
        self.assignRange = assignRange

        self.lenAssign = len(assignRange)
        self.lendssp = len(dsspRange)

    
    def getSims(self):
        allSim = {"(0,0.5)": 0, "(0.5,0.8)": 0, "(0.8,1)": 0}
        if self.lenAssign == 0:
            return allSim

        for indexA in range(self.lenAssign):
            '''遍历指定结果'''
            assignHelix = self.assignRange[indexA]
            
            for indexB in range(self.lendssp):
                '''遍历dssp结果'''
                dsspHelix = self.dsspRange[indexB]
                newRange = [0, 0]

                if (dsspHelix[0] >assignHelix[1]) or (dsspHelix[1] < assignHelix[0]):
                    simRate=0
                    flag=0
                    continue

                if assignHelix[0] > dsspHelix[0]:
                    newRange[0] = assignHelix[0]
                else:
                    newRange[0] = dsspHelix[0]
                if assignHelix[1] > dsspHelix[1]:
                    newRange[1] = dsspHelix[1]
                else:
                    newRange[1] = assignHelix[1]

                simRate = (newRange[1]-newRange[0])/(dsspHelix[1]-dsspHelix[0])
                if simRate >= 0.8:
                    allSim["(0.8,1)"] += 1
                    flag=1
                    break
                else:
                    if (dsspHelix[0]-3) <= assignHelix[0] <= (dsspHelix[0]+3) and (dsspHelix[1]-3) <= assignHelix[1] <= (dsspHelix[1]+3):
                        allSim["(0.8,1)"] += 1
                        flag=1
                        break
                    elif 0.5<= simRate < 0.8:
                        allSim["(0.5,0.8)"] += 1
                        flag=1
                        break
                    else:
                        allSim["(0,0.5)"] += 1
                        flag=1
                        break
            if flag==0:
                allSim["(0,0.5)"] += 1
                continue

        return allSim


        # self.score = self.getScore()

    # def getScore(self):  # ,dsspRange, assignRange
    #     score = self.lenAssign

    #     if self.lenAssign == 0:
    #         return score

    #     for indexA in range(self.lenAssign):
    #         '''遍历指定结果'''
    #         assignHelix = self.assignRange[indexA]
    #         for indexB in range(self.lendssp):
    #             '''遍历dssp结果'''
    #             flag = 0
    #             dsspHelix = self.dsspRange[indexB]

    #             if (dsspHelix[0]-3) <= assignHelix[0] <= (dsspHelix[0]+3) and (dsspHelix[1]-3) <= assignHelix[1] <= (dsspHelix[1]+3):
    #                 # accu += 1 # 如果指定结果能在指定范围内，得分增加1
    #                 flag = 1
    #                 break
    #             elif (dsspHelix[0]-1) <= assignHelix[0] < (dsspHelix[1]+1) and (dsspHelix[0]-1) < assignHelix[1] <= (dsspHelix[1]+1):
    #                 # 如果指定结果能在指定范围内，得分增加百分比
    #                 rateScore = (
    #                     assignHelix[1]-assignHelix[0]) / (dsspHelix[1]-dsspHelix[0])
    #                 score -= (1-rateScore)
    #                 flag = 1
    #                 break
    #         if flag == 0:
    #             score -= 1
    #     return score

    # def getScoreRate(self):  # , pdbID, dsspRange, assignRange
    #     if self.score == 0:
    #         return {self.pdbID: 0}

    #     rate = self.score/self.lenAssign
    #     scoreRate = {self.pdbID: rate}

    #     return scoreRate

    # def getScoreValue(self):  # dsspRange, assignRange
    #     scoreValue = {self.lenAssign: self.score}
    #     return scoreValue

    # def getSimNum(self):
    #     simNum = {"(0,0.5)": 0, "(0.5,0.8)": 0, "(0.8,1)": 0}
    #     if self.lenAssign == 0:
    #         return simRate

    #     for indexA in range(self.lenAssign):
    #         '''遍历指定结果'''
    #         assignHelix = self.assignRange[indexA]
            
    #         for indexB in range(self.lendssp):
    #             '''遍历dssp结果'''
    #             dsspHelix = self.dsspRange[indexB]
    #             newRange = [0, 0]
    #             flag=0

    #             if assignHelix[0] > dsspHelix[0]:
    #                 newRange[0] = assignHelix[0]
    #             else:
    #                 newRange[0] = dsspHelix[0]
    #             if assignHelix[1] > dsspHelix[1]:
    #                 newRange[1] = dsspHelix[1]
    #             else:
    #                 newRange[1] = assignHelix[1]

    #             simRate = (newRange[1]-newRange[0])/(dsspHelix[1]-dsspHelix[0])
    #             if simRate < 0.5:
    #                 continue
    #             elif 0.5 <= simRate < 0.8:
    #                 simNum["(0.5,0.8)"] += 1
    #                 flag=1
    #                 break
    #             else:
    #                 simNum["(0.8,1)"] += 1
    #                 flag=1
    #                 break
    #         if flag==0:
    #             simNum["(0,0.5)"] += 1
    #     return simNum

    