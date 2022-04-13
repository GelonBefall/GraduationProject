import pickle
import os


class pickleOP:
    def savePickle(self, diaLines: dict, pickleName: str, overWrite=False):
        path = "./materials/pickle/"
        pickleFile = path+pickleName
        if not os.path.exists(path):
            os.makedirs(path)
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

    def loadPickle(self, pickleName: str) -> dict:
        path = "./materials/pickle/"+pickleName
        with open(path, "rb") as pk:
            # pickles=pickle.dumps(diaLines)
            diaLines = pickle.load(pk)
        print("从pickle文件读入数据。")
        return diaLines

    # def __saveJson(self,diaLines:dict, jsonName:str):
    #     with open("./materials/json/"+jsonName, "wb") as js:
    #         jsons=json.dumps(diaLines)
    #         json.dump(jsons, js)
