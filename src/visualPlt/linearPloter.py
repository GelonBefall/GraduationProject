import matplotlib.pyplot as plt
import os


def plotLinr(simNums:dict, pngName, numb:str):
    low=simNums["(0,0.5)"]
    mid=simNums["(0.5,0.8)"]
    high=simNums["(0.8,1)"]
    total = low+mid+high
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    #数据标签
    labels = ["(0,0.5)", "(0.5,0.8)", "(0.8,1)"]
    #设置绘图属性并绘图

    x = range(len(labels))
    data = [low/total,mid/total,high/total]
    plt.plot(x, data, marker='o', mec='r', mfc='w')
    
    plt.legend()  # 让图例生效
    plt.xticks(x, labels, rotation=45)
    plt.margins(0)
    plt.subplots_adjust(bottom=0.15)
    # plt.tick_params(axis='y', labelsize=10)
    # plt.axis([0, 1]) 

    plt.xlabel(u"分数分布") #X轴标签
    plt.ylabel(u"每种分数所占百分比") #Y轴标签
    plt.title(pngName) #标题

    pngName+='.png'
    path = os.path.join(os.getcwd(), "production/plots/linear", numb,pngName)
    plt.savefig(path, dpi=500)

def plotstatLinr(dataset:list):
    pngName='验证集测试结果'
    data=[]
    xlabels = range(1,8)
    ylabels=[0,0.5,1]
    x = range(len(xlabels))
    y = [0,0.5,1]
    for stats in dataset:
        data.append(stats["(0.8,1)"]/stats["dsspNum"])

    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.plot(x, data, marker='o', mec='r', mfc='w')
    plt.legend()  # 让图例生效

    plt.title(pngName)
    
    plt.xlabel(u"数据集") #X轴标签
    plt.ylabel(u"相似度高于80%的α-螺旋所占DSSP比例") #Y轴标签
    plt.xticks(x, xlabels)
    # plt.yticks(y, ylabels)#
    plt.margins(0)
    plt.subplots_adjust(bottom=0.15)

    

    pngName+='.png'
    path = os.path.join(os.getcwd(), "production/plots/linear/", pngName)
    plt.savefig(path, dpi=500)
