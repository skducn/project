# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: 将数据生成表格图像
#***************************************************************

import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import savefig
import matplotlib.pyplot as plt

def data2pic(varTitle, varY, varXnums, varX, dimURL):

    fig, ax = plt.subplots()
    # 标题
    ax.set_title(varTitle)
    # Y轴 数量
    ax.set_ylabel(varY)
    # X轴 商品
    N = varXnums
    width = 0.2  # the width of the bars
    ind = np.arange(N)  # the x locations for the groups
    ax.set_xticks(ind + width + width)

    tmp = varX.split(",")
    ax.set_xticklabels((tmp[0], tmp[1], tmp[2], tmp[3]))

    rects1 = ax.bar(ind, (20, 35, 30, 25), width, color='r', yerr=(1, 1, 1, 1))
    rects2 = ax.bar(ind + width, (25, 32, 34, 20), width, color='y', yerr=(0, 0, 0, 0))
    rects3 = ax.bar(ind + width + width, (25, 32, 34, 20), width, color='b', yerr=(0, 0, 0, 0))
    rects4 = ax.bar(ind + width + width + width, (25, 32, 34, 21), width, color='g', yerr=(0, 0, 0, 0))
    ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]), (u'serious', 'high', 'normal', 'low'))

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height), ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    autolabel(rects4)

    # 文件保存路径
    savefig(dimURL)

    # 直接屏幕输出
    # plt.show()

data2pic(u"bug", u'num', 4, u'android,iOs,PHP,Server','test123.png')