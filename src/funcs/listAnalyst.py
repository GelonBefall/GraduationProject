from cv2 import mean
import numpy


class anaList:
    def __init__(self):
        pass

    def arrExe(self, uList: numpy.ndarray):
        # if len(uList) >= 4:
        uList = uList[1:-1]  # 去掉头尾误差

        index = []
        index.append(uList.min())
        index.append(uList.max())
        index = numpy.array(index)

        uList = numpy.setdiff1d(uList, index)  # 删除最大最小元素，会同时删除重复元素且自动排序。
        return uList

    def rangeDis(self, uList: numpy.ndarray):
        '''求范围'''
        uList = self.arrExe(uList)  # 去除大小误差

        aHRange = []
        aHRange.append(uList[0])
        aHRange.append(uList[-1])
        return aHRange

    def meanDis(self, uList: numpy.ndarray):
        '''求平均数'''
        uList = self.arrExe(uList)
        mean = uList.mean()
        return mean

    def varDis(self, uList: numpy.ndarray):
        '''求方差'''
        uList = self.arrExe(uList)
        var = uList.var()
        return var


if __name__ == '__main__':
    a = numpy.array([1, 1, 2, 7.2, 4, 3, 5, 6, 6, 7.1,  7.3])
    aL = anaList()
    print(aL.arrExe(a))
