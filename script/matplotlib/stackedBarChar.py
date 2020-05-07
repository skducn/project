# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: 将数据生成表格图像
# https://matplotlib.org/gallery/index.html
#***************************************************************

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
# from matplotlib import font_manager as fm, rcParams

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False


labels = ['方程式', 'G2', 'G3', 'G4', 'G5']
men_means = [20, 35, 30, 35, 27]
women_means = [25, 32, 34, 20, 25]
men_std = [2, 3, 4, 1, 2]
women_std = [3, 5, 2, 3, 3]
width = 0.35       # the width of the bars: can also be len(x) sequence
fig, ax = plt.subplots()
ax.bar(labels, men_means, width, yerr=men_std, label='男')
ax.bar(labels, women_means, width, yerr=women_std, bottom=men_means,label='女')

ax.set_ylabel('Sco测试res')
ax.set_title('小组成绩单')
ax.legend()

# 直接打印
plt.show()

# # 文件保存路径
# savefig("test.png")