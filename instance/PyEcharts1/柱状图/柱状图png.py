# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-3-3
# Description: pyEcharts 柱状图生产png
# pip3.9 install pyecharts -U   //安装 v1 以上版本
# pip3.9 install bar
# pip3.9 install snapshot-selenium
# 更多的可视化报表的应用方式和参考代码：https://github.com/pyecharts/pyecharts
#***************************************************************

from snapshot_selenium import snapshot as driver
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.render import make_snapshot

def bar_chart() -> Bar:
    c = (
        Bar()
        .add_xaxis(["衬衫", "毛衣", "领带", "裤子", "风衣", "高跟鞋", "袜子"])
        .add_yaxis("商家A", [114, 55, 27, 101, 125, 27, 105])
        .add_yaxis("商家B", [57, 134, 137, 129, 145, 60, 49])
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-测试渲染图片"))
    )
    return c

# 需要安装 snapshot-selenium 或者 snapshot-phantomjs
make_snapshot(driver, bar_chart().render(), "bar.png")