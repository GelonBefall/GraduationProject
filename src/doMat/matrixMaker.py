import numpy as np

from src.funcs.pdbReader import readPDB
from collections import deque


class makeMatrix(readPDB):
    '''Before using other function, better to execute "calMatrix()" first.'''

    def calMatrix(self):
        '''To calculate the distance of CA.'''
        structure = self.p.get_structure(self.pdbID, self._pdbFile)
        disLists = deque()
        ListsTemp = deque()

        residues1 = structure.get_residues()
        for residue1 in residues1:
            residues2 = structure.get_residues()
            if residue1.has_id("CA"):
                CA1 = residue1['CA']
            else:
                continue

            for residue2 in residues2:
                if residue2.has_id("CA"):
                    CA2 = residue2["CA"]
                    distance = CA1 - CA2
                    ListsTemp.append(distance)
                    # # print(ListsTemp)
                else:
                    continue

            disLists.append(ListsTemp)
            # print(disLists)
            ListsTemp = deque()
        self.disMatrix = np.array(disLists)
        # return disMatrix


if __name__ == '__main__':
    NM = makeMatrix(pdbID='3INS')
    NM.calMatrix()
    print(NM.residuesCount())
