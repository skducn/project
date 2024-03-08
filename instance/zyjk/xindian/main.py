# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2024-1-5
# Description: 获取 MIT-BIH 心律数据，一组两个导联的心电波形
# 基于机器学习的心律失常分类(二)——读取MIT-BIH数据库中的心电数据[MATLAB] https://zhuanlan.zhihu.com/p/150941077?utm_id=0
# 读取 MIT-BIH 心律数据（pyton）：https://cloud.tencent.com/developer/article/1408068
# *****************************************************************

import wfdb as wf
import os

path = "/Users/linghuchong/Downloads/xindian/mit-bih-arrhythmia-database-1.0.0/"
for i in range(100, 235):
    if os.access(path + str(i) + ".dat", os.F_OK) == True:
        # 获取心率数据记录
        record = wf.rdrecord(path + str(i))
        fig = wf.plot_wfdb(record=record, title='Record ' + str(i) + ' from MIT-BIH Arrhythmia Database', return_fig=True)
        fig.savefig(path + "/result/" + str(i) + ".png")
        # 获取心率注释
        annotation = wf.rdann(path + str(i), 'atr', sampto=15000)
        fig = wf.plot_wfdb(record=record, annotation=annotation,
                       title='Record ' + str(i) + 'atr from MIT-BIH Arrhythmia Database',
                       time_units='seconds', return_fig=True)
        fig.savefig(path + "/result/" + str(i) + "atr.png")



path = "/Users/linghuchong/Downloads/xindian/mit-bih-st-change-database-1.0.0/"
for i in range(300, 328):
    if os.access(path + str(i) + ".dat", os.F_OK) == True:
        # 获取心率数据记录
        record = wf.rdrecord(path + str(i))
        fig = wf.plot_wfdb(record=record, title='Record ' + str(i) + ' from MIT-BIH-ST Change Database', return_fig=True)
        fig.savefig(path + "/result/" + str(i) + ".png")
        # 获取心率注释
        annotation = wf.rdann(path + str(i), 'atr', sampto=15000)
        fig = wf.plot_wfdb(record=record, annotation=annotation,
                       title='Record ' + str(i) + 'atr from MIT-BIH-ST Change Database',
                       time_units='seconds', return_fig=True)
        fig.savefig(path + "/result/" + str(i) + "atr.png")

