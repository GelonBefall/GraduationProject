import os
import requests
import shutil

from pathlib import Path
from Bio.PDB.PDBParser import PDBParser


class readPDB:
    def __init__(self, pdbID: str, pdbPath=None):
        self.pdbID = pdbID.lower()
        self.__pdbPath = os.path.join(os.getcwd(), "materials/pdb/")
        self.__initPDBFile(pdbPath)

        self.p = PDBParser(PERMISSIVE=1)  # 可选参数PERMISSIVE=1时忽略错误
        self.CAAmount = self.CACount()
        print("The CAAmount of {} is {}.".format(self.pdbID, self.CAAmount))

    def __initPDBFile(self, pdbPath):

        if pdbPath:  # 如果路径存在
            # self.__pdbPath = pdbPath
            self._pdbFile = os.path.join(pdbPath, "{}.pdb".format(self.pdbID))
            if self.pdbExist() == 0:  # 如果pdb文件存在
                return 0
            else:
                self._pdbFile == None
        else:
            self._pdbFile = self.__pdbFinder()

        if self._pdbFile == None:
            path = self.__pdbDownload()
            self.__initPDBFile(path)

    def __pdbFinder(self):
        # __pdbPath = os.path.join(os.getcwd(), "materials/pdb/")
        pdbPath = Path(self.__pdbPath)
        pdbFile = self.pdbID+'.pdb'

        result = list(pdbPath.rglob(pdbFile))
        if len(result) == 0:
            return None

        else:
            pdbFile = os.path.join(self.__pdbPath, result[0])  # ._cparts[2]
            return pdbFile

    def pdbDeleter(self):
        os.remove(self._pdbFile)
        print("已成功删除{}的pdb文件！".format(self.pdbID))

    def pdbMover(self):
        __newFile = os.path.join(
            os.getcwd(), "materials/big_pdb/", "{}.pdb".format(self.pdbID))
        shutil.move(self._pdbFile, __newFile)

    def pdbExist(self):
        if os.path.exists(self._pdbFile):
            # print("PDB file exist!")
            return 0
        else:
            print("PDB file doesn't exist!")
            return 1

    def __pdbDownload(self):

        for root, dirs, files in os.walk(self.__pdbPath):  # 开始遍历pdb文件夹
            for __subPath in dirs:  # 遍历子文件夹
                __subPath = os.path.join(root, __subPath)+'/'

                # 查看子文件夹下面的文件数量
                for subRoot, ssDirs, subFiles in os.walk(__subPath):
                    if len(list(subFiles)) >= 2000:
                        break

                    else:
                        url = "https://files.rcsb.org/download/" + self.pdbID + ".pdb"
                        r = requests.get(url)
                        # print(r)
                        for i in range(3):
                            if r:
                                print("Downloading {}.pdb...".format(self.pdbID))

                                self._pdbFile = os.path.join(
                                    __subPath, self.pdbID + ".pdb")
                                with open(self._pdbFile, "wb") as pdbFile:
                                    pdbFile.write(r.content)

                                isPDBExist = self.pdbExist()
                                if isPDBExist == 0:
                                    print("PDB file download successfully!")
                                    return __subPath
                            if i == 2:
                                print(
                                    "PDB file can't download or doesn't exist, please check!")
                                return 1

    def residuesCount(self):
        '''Get CA atoms' count.'''
        structure = self.p.get_structure(self.pdbID, self._pdbFile)
        chains = structure.get_chains()
        counts = {}
        chainIDs = []

        for chain in chains:
            if chain.id in chainIDs:
                break
            chainIDs.append(chain.id)
            residues = chain.get_residues()
            count = 0
            # print(chain.id)
            for residue in residues:
                if residue.has_id("CA"):
                    count = count + 1
            if count == 0:
                continue
            counts[chain.id] = count
            # print("The CAAmount of {} is {}.".format(chain, count))
        return counts

    def CACount(self):
        '''Get CA atoms' count.'''
        count = 0
        counts = self.residuesCount()
        for id in counts:
            count += counts[id]
        return count


if __name__ == '__main__':
    rp = readPDB(pdbID='1aov')
    print(rp.residuesCount())
    print(rp.CAAmount)
    # print(rp.pdbDeleter())
    # print(rp.pdbMover())
