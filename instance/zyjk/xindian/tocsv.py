# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2024-1-5
# Description: https://zhuanlan.zhihu.com/p/150941077?utm_id=0
# *****************************************************************
# todo 获取MIT_BIH 心律失常数据库中的ECG注释文件atr

import wfdb, os, csv
import pandas as pd

file_path = "/Users/linghuchong/Downloads/xindian/mit-bih-arrhythmia-database-1.0.0/"

files = os.listdir(file_path)
for file in files:
    name = os.path.splitext(file)[0]
    annotation = wfdb.rdann(file_path + name, "atr")
    sample = annotation.sample
    symbol = annotation.symbol
    dataframe = pd.DataFrame({'sample': sample, 'symbol': symbol})
    dataframe.to_csv(file_path + "atr.csv", sep=',')