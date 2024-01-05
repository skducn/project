# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2024-1-5
# Description: https://zhuanlan.zhihu.com/p/150941077?utm_id=0
# *****************************************************************


import wfdb
import numpy as np

# 读取心电数据和对应标签,并对数据进行小波去噪
def getDataSet(number, X_data):
    # 读取心电数据记录
    print("正在读取 " + number + " 号心电数据...")
    record = wfdb.rdrecord('ecg_data/' + number, channel_names=['MLII'])  #源文件都放在ecg_data这个文件夹中了
    data = record.p_signal.flatten()
    #data=np.array(data)

    # 获取心电数据记录中R波的位置和对应的标签
    annotation = wfdb.rdann('ecg_data/' + number, 'atr')
    Rlocation = annotation.sample  #对应位置
    Rclass = annotation.symbol  #对应标签

    X_data.append(data)

    return

# 加载数据集并进行预处理
def loadData():
    numberSet = ['100','103']
    dataSet = []
    for n in numberSet:
        getDataSet(n, dataSet)
    return dataSet

def main():
    dataSet = loadData()
    dataSet = np.array(dataSet)
    print(dataSet.shape)
    print("data ok!!!")

if __name__ == '__main__':
    main()