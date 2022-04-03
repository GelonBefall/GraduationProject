import os
import sys
import requests

from Bio.PDB.PDBParser import PDBParser


class readPDB:
    def __init__(self, pdbID:str):
        self.pdbID = pdbID.lower()
        self._pdbPath = "./materials/pdb/"
        self._pdbFile = os.path.join(
            self._pdbPath, "{}.pdb".format(self.pdbID))

        initStatus = self.__initPDBFile()
        if initStatus == 0:
            self.p = PDBParser(PERMISSIVE=1)  # 可选参数PERMISSIVE=1时忽略错误
            self.CAAmount = self.CACount()
            print("The CAAmount of {} is {}.".format(self.pdbID, self.CAAmount))
        else:
            print("The .pdb file is not existed or can't be downloaded, init class fail.")
            sys.exit()

    def __initPDBFile(self):
        pdbExist = self.pdbExist()
        if pdbExist == 0:
            return 0
        else:
            dlStatus = self.__pdbDownload()
            if dlStatus == 0:
                return 0
            else:
                return 1

    def pdbExist(self):
        if os.path.exists(self._pdbFile):
            # print("PDB file exist!")
            return 0
        else:
            print("PDB file doesn't exist!")
            return 1

    def __pdbDownload(self):
        url = "https://files.rcsb.org/download/" + self.pdbID + ".pdb"
        r = requests.get(url)
        print(r)
        for i in range(3):
            if r:
                print("Downloading {}.pdb...".format(self.pdbID))
                with open(self._pdbFile, "wb") as pdbFile:
                    pdbFile.write(r.content)
                isPDBExist = self.pdbExist()
                if isPDBExist == 0:
                    print("PDB file download successfully!")
                    return 0
            else:
                isPDBExist = self.pdbExist()
                if isPDBExist == 0:
                    return 0
            if i == 2:
                print("PDB file doesn't download successfully, please check!")
                return 1

    def residuesCount(self):
        '''Get CA atoms' count.'''
        structure = self.p.get_structure(self.pdbID, self._pdbFile)
        chains = structure.get_chains()
        counts = {}
        for chain in chains:
            residues = chain.get_residues()
            count = 0
            # print(chain.id)
            for residue in residues:
                if residue.has_id("CA"):
                    count = count + 1
            if count==0:
                continue
            counts[chain.id]=count
            print("The CAAmount of {} is {}.".format(chain, count))
        return counts

    def CACount(self):
        '''Get CA atoms' count.'''
        count = 0
        counts=self.residuesCount()
        for id in counts:
            count += counts[id]
        return count

if __name__=='__main__':
    rp=readPDB(pdbID='2erk')
    print(rp.residuesCount())