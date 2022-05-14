import os
import matplotlib.pyplot as plt
import numpy as np
# 改变绘图风格
import seaborn as sns
sns.set(color_codes=True)


def pltChecks(step: int, checks: dict):
    plt.figure()
    cell = ['1', '2', '3', '4', 'other']
    total = checks[1] + checks[2] + checks[3] + checks[4] + checks['other']
    # print(total)
    pvalue = [checks[1]/total, checks[2]/total, checks[3] /
              total, checks[4]/total, checks['other']/total]
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    width = 0.50
    index = np.arange(len(cell))
    p1 = np.arange(0, len(cell), 0.01)
    p2 = 0.05 + p1*0

    q1 = np.arange(0, len(cell), 0.01)
    q2 = 0.1 + p1*0
    plt.plot(p1, p2, color='red', label='5% significance level')  # 绘制直线
    plt.plot(q1, q2, color='yellow', label='10% significance level')  # 绘制直线

    plt.bar(index, pvalue, width, color=['y', 'g', 'b', 'c', 'm'])
    plt.xlabel('灰阶值')  # x轴
    plt.ylabel('灰阶比列')  # y轴
    plt.title('有关t值为{}时，灰阶值的分布情况'.format(step))  # 图像的名称
    plt.xticks(index, cell, fontsize=10)  # 将横坐标用cell替换,fontsize用来调整字体的大小
    plt.legend()  # 显示label
    for x, y in zip(range(0, 5), pvalue):
        plt.text(x, y+0.001, '%.4f' % y, ha='center', va='bottom', fontsize=9)

    path = os.path.join(os.getcwd(), "production/plots/",
                        't={}.png'.format(step))
    plt.savefig(path, dpi=400)  # 保存图像，dpi可以调整图像的像素大小


if __name__ == '__main__':
    from src.funcs.pickleOperater import pickleOP
    pickle = pickleOP()
    pickleName = '0000_statCheck'
    steps = [1, 2, 3]
    allchecks = pickle.loadPickle(pickleName)
    for step in steps:
        print(allchecks[step])
        pltChecks(step, allchecks[step])
