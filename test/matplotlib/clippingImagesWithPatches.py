# coding: utf-8
#***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: 将数据生成表格图像
# https://matplotlib.org/gallery/index.html
#***************************************************************


import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cbook as cbook
from matplotlib.pyplot import savefig



with cbook.get_sample_data('d:\\1\\test.jpg') as image_file:
    image = plt.imread(image_file)

fig, ax = plt.subplots()
im = ax.imshow(image)
patch = patches.Circle((640, 324), radius=300, transform=ax.transData)  # 640,324 分别是图片分辨率一半，如 1280*649 ， 300是圆圈的大小
im.set_clip_path(patch)

ax.axis('off')
# plt.show()


# # 文件保存路径
savefig("d:\\1\\test.png")