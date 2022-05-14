import matplotlib.pyplot as plt
import os

def plotPie(simNums:dict):
    low=simNums["(0,0.5)"]
    mid=simNums["(0.5,0.8)"]
    high=simNums["(0.8,1)"]
    total = low+mid+high
    plt.figure()
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    data = [low/total*100,mid/total*100,high/total*100]
    #数据标签
    labels = ["(0,0.5)", "(0.5,0.8)", "(0.8,1)"]
    #各区域颜色
    # colors = ['green','blue','orange']
    
    expodes = (0,0,0.1)
    plt.title('程序指定的相似度占比')
    #设置绘图属性并绘图
    plt.pie(data,explode=expodes,labels=labels,shadow=True,autopct='%10.2f%%')#,colors=colors
    ## 用于显示为一个长宽相等的饼图
    plt.axis('equal')
    plt.legend()
    
    path = os.path.join(os.getcwd(), "production/plots/",'simNumPie.png')
    plt.savefig(path, dpi=400)
    