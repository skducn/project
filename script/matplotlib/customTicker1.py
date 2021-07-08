# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2021-7-7
# Description:
# https://matplotlib.org/stable/gallery/ticks_and_spines/custom_ticker1.html#sphx-glr-gallery-ticks-and-spines-custom-ticker1-py
#***************************************************************


import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False

labels = ['致命', '严重', '一般', '轻微']
men_means = [20, 34, 30, 35]


x = np.arange(len(labels))  # the label locations
width = 0.8  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, men_means, width, label='缺陷')
ax.set_ylabel('数量')
ax.set_title('bug严重程度')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
ax.bar_label(rects1, padding=3)

# fig.tight_layout()

# plt.show()



# # 文件保存路径
plt.savefig("d:\\1\\test.png")