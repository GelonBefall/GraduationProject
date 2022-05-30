import matplotlib.pyplot as plt
import os


def plotLinr(simNums: dict, pngName, numb: str):
    low = simNums["(0,0.5)"]
    mid = simNums["(0.5,0.8)"]
    high = simNums["(0.8,1)"]
    total = low+mid+high
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    # 数据标签
    labels = ["(0,0.5)", "(0.5,0.8)", "(0.8,1)"]
    # 设置绘图属性并绘图

    x = range(len(labels))
    data = [low/total, mid/total, high/total]
    plt.plot(x, data, marker='o', mec='r', mfc='w')

    plt.legend()  # 让图例生效
    plt.xticks(x, labels, rotation=45)
    plt.margins(0)
    plt.subplots_adjust(bottom=0.15)
    # plt.tick_params(axis='y', labelsize=10)
    # plt.axis([0, 1])

    plt.xlabel(u"分数分布")  # X轴标签
    plt.ylabel(u"每种分数所占百分比")  # Y轴标签
    plt.title(pngName)  # 标题

    pngName += '.png'
    path = os.path.join(os.getcwd(), "production/plots/linear", numb, pngName)
    plt.savefig(path, dpi=500)


def plotstatLinr(dataset: list):
    pngName = '验证集测试结果'
    Precisions = []
    Recalls = []
    xlabels = range(1, 7)
    # ylabels=[0,0.5,1]
    x = range(len(xlabels))
    # y = [0,0.5,1]
    for stats in dataset:
        Recalls.append(stats["(0.8,1)"]/stats["dsspNum"])
        Precisions.append(
            stats["(0.8,1)"]/(stats["(0.8,1)"]+stats["(0.5,0.8)"]+stats["(0,0.5)"]))
    print(str(Precisions)+'\n'+str(Recalls))
    
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.plot(x, Precisions, marker='o', mec='r', mfc='w', label=u'Precisions')
    plt.plot(x, Recalls, marker='s', mec='c', mfc='w', label=u'Recalls')
    plt.legend()  # 让图例生效

    plt.title(pngName)

    plt.xlabel(u"验证集编号")  # X轴标签
    plt.ylabel(u"二级指标大小")  # Y轴标签
    plt.xticks(x, xlabels)
    plt.ylim(0.7, 1)  # 限定纵轴的范围
    # plt.yticks(y, ylabels)#
    plt.margins(0)
    plt.subplots_adjust(bottom=0.15)

    pngName += '.png'
    path = os.path.join(os.getcwd(), "production/plots/linear/", pngName)
    plt.savefig(path, dpi=500)

def plotPRCLinr(dataset: list):
    pngName = 'PR Curve'
    Precisions = []
    Recalls = []
    xlabels = range(1, 7)
    # ylabels=[0,0.5,1]
    x = range(len(xlabels))
    # y = [0,0.5,1]
    for stats in dataset:
        Recalls.append(stats["(0.8,1)"]/stats["dsspNum"])
        Precisions.append(
            stats["(0.8,1)"]/(stats["(0.8,1)"]+stats["(0.5,0.8)"]+stats["(0,0.5)"]))
    print(str(Precisions)+'\n'+str(Recalls))
    
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.plot(Recalls, Precisions, marker='o', mec='r', mfc='w')
    # plt.plot(x, Recalls, marker='s', mec='c', mfc='w', label=u'Recalls')
    plt.legend()  # 让图例生效

    plt.title(pngName)

    plt.xlabel(u"Recalls")  # X轴标签
    plt.ylabel(u"Precisions")  # Y轴标签
    # plt.xticks(x, xlabels)
    plt.xlim(0, 1)  # 限定横轴的范围
    plt.ylim(0, 1)  # 限定纵轴的范围
    # plt.yticks(y, ylabels)#
    plt.margins(0)
    plt.subplots_adjust(bottom=0.15)

    pngName += '.png'
    path = os.path.join(os.getcwd(), "production/plots/linear/", pngName)
    plt.savefig(path, dpi=500)
