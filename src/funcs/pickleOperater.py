import pickle
import os


class pickleOP:
    def __init__(self):
        self.__path = os.path.join(os.getcwd(), "production/pickle/")

    def savePickle(self, diaLines: dict, pickleName: str, otherpath='', overWrite=False):

        pickleFile = self.__path+otherpath+'/'+pickleName

        if overWrite == True:
            with open(pickleFile, "wb") as pk: 
                # pickles=pickle.dumps(diaLines)
                pickle.dump(diaLines, pk)

        else:
            if os.path.exists(pickleFile):
                print("pickle文件已存在，若要覆盖，请使用覆盖模式。")

            else:
                with open(pickleFile, "wb") as pk:
                    # pickles=pickle.dumps(diaLines)
                    pickle.dump(diaLines, pk)

    def loadPickle(self, pickleName: str, otherpath='') -> dict:
        pickleFile = self.__path+otherpath+'/'+pickleName

        with open(pickleFile, "rb") as pk:
            # pickles=pickle.dumps(diaLines)
            diaLines = pickle.load(pk)

        print("从pickle文件读入数据。")
        return diaLines

    def deletePickle(self, pickleName: str):
        pickleFile = self.__path+pickleName
        if os.path.exists(pickleFile):
            os.remove(pickleFile)
            print("已成功删除{}！".format(pickleName))

    # def __saveJson(self,diaLines:dict, jsonName:str):
    #     with open("./materials/json/"+jsonName, "wb") as js:
    #         jsons=json.dumps(diaLines)
    #         json.dump(jsons, js)
