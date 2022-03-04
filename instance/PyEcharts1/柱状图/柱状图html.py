# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-3-3
# Description: pyEcharts 柱状图生产html
# 安装 v1 以上版本
# $ pip3.9 install pyecharts -U
# pip3.9 install bar
# 更多的可视化报表的应用方式和参考代码，大家可以参考：https://github.com/pyecharts/pyecharts
#***************************************************************

# //导入柱状图-Bar
from pyecharts.charts import Bar
from pyecharts import options as opts
import os

# # 方法1：单独调用方法
# bar = Bar()
# # //设置行名
# bar.add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
# # //设置数据
# bar.add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
# bar.add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
# # //设置柱状图的标题
# bar.set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
# # //生成本地文件（默认为.html文件） # bar.render("test测试.html")
# bar.render()


# 方法2：V1 版本开始支持链式调用
bar = (
    Bar()
    .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
    .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
    .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
    .set_global_opts(title_opts=opts.TitleOpts(title="某商场销售情况"))
)
bar.render()

os.system("render.html")