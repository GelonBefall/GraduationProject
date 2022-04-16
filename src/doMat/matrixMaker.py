import numpy as np

from src.funcs.pdbReader import readPDB
from collections import deque


class makeMatrix(readPDB):
    '''Before using other function, better to execute "calMatrix()" first.'''

    def calMatrix(self):
        '''To calculate the distance of CA.'''
        structure = self.p.get_structure(self.pdbID, self._pdbFile)
        chains1 = structure.get_chains()

        self.disMatrix = deque()
        ListsTemp = deque()

        chainID1s = []
        
        for chain1 in chains1:  # 开始遍历所有支链
            if chain1.id in chainID1s:
                break
            residues1 = chain1.get_residues()  # 获取该链的所有残基
            chainID1s.append(chain1.id)

            for residue1 in residues1:  # 遍历该链的所有残基
                if residue1.has_id("CA"):
                    CAlpha1 = residue1['CA']

                    chains2 = structure.get_chains()  # 重新实例化chains2
                    chainID2s = []
                else:
                    continue

                for chain2 in chains2:  # 停留在chain1的某一残基，与chains2的残基交互
                    if chain2.id in chainID2s:
                        break
                    chainID2s.append(chain2.id)

                    residues2 = chain2.get_residues()  # 获取该chain2链的所有残基
                    for residue2 in residues2:
                        if residue2.has_id("CA"):
                            CAlpha2 = residue2["CA"]
                            distance = CAlpha1 - CAlpha2  # 计算距离
                            ListsTemp.append(distance)  # 暂存距离
                            # print(ListsTemp)
                        else:
                            continue

                self.disMatrix.append(ListsTemp)  # 一个残基与其他残基计算完距离后保存
                # print(self.disMatrix)
                ListsTemp = deque()
        self.disMatrix = np.array(self.disMatrix)


if __name__ == '__main__':
    NM = makeMatrix(pdbID='1a02')
    NM.calMatrix()
    print(NM.residuesCount())
