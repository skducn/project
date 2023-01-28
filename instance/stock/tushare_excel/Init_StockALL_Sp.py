# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-06-15
# Description: 量化框架，机器量化分析（一）——数据采集、预处理与建模
# pip3.9 install tushare --upgrade
# 获取token https://tushare.pro/user/token
# 机器量化分析（一）——数据采集、预处理与建模 https://tushare.pro/document/1?doc_id=63

# 数据采集：通过tushare获取数据到excel  （Init_StockALL_Sp.py）
# 数据预处理：主要包括数据清洗，排序，缺失值或异常值处理，统计量分析，相关性分析，主成分分析（PCA），归一化等。将存在本地数据库的日线行情数据整合成一份训练集数据，以用于后续的机器学习建模和训练。(DC.py)
# SVM建模：机器学习中有诸多有监督学习算法，SVM是比较常见的一种，本例采用SVM算法进行建模。(SVM.py)
# *****************************************************************

import datetime
import tushare as ts
from PO.OpenpyxlPO import *
from sklearn import svm
import numpy as np
import DC

class Init_StockALL_Sp(object):

    def getStockData(self, l_stockCode, start_dt, end_dt, excelFile):
        # 设置tushare pro的token并获取连接
        ts.set_token('894e80b70503f5cda0d86f75820c5871ff391cf7344e55931169bb2a')
        pro = ts.pro_api()

        # 设定获取日线行情的初始日期和终止日期，其中终止日期设定为昨天。
        # start_dt = '20230110'
        # time_temp = datetime.datetime.now() - datetime.timedelta(days=1)
        # end_dt = time_temp.strftime('%Y%m%d')
        # end_dt = '20230120'


        # 新建excel
        Openpyxl_PO = OpenpyxlPO("")
        if len(l_stockCode) > 1 :
            Openpyxl_PO.newExcel(excelFile, l_stockCode)
        else:
            Openpyxl_PO.newExcel(excelFile, l_stockCode[0])


        Openpyxl_PO = OpenpyxlPO(excelFile)
        # Openpyxl_PO.setRowValue({1: ['state_dt','stock_code','open','close','high','low','vol','amount','pre_close','amt_change','pct_change']})
        # (交易日，股票代码，开盘价，收盘价，最高价，最低价，成交量，成交额，前日收盘价，涨跌额，涨跌幅)

        # 设定需要获取数据的股票池
        stock_pool = l_stockCode
        # stock_pool = ['603439.SH','300666.SZ','300618.SZ','002049.SZ','300672.SZ']

        total = len(stock_pool)
        # 循环获取单个股票的日线行情
        for i in range(len(stock_pool)):
            try:
                df = pro.daily(ts_code=stock_pool[i], start_date=start_dt, end_date=end_dt)
                print('Seq: ' + str(i+1) + ' of ' + str(total) + '   Code: ' + str(stock_pool[i]))
                c_len = df.shape[0]
            except Exception as aa:
                print(aa)
                print('No DATA Code: ' + str(i))
                continue

            for j in range(c_len):
                # resu0 = list(df.ix[c_len-1-j])
                resu0 = list(df.iloc[c_len-1-j])
                resu = []
                for k in range(len(resu0)):
                    if str(resu0[k]) == 'nan':
                        resu.append(-1)
                    else:
                        resu.append(resu0[k])
                state_dt = (datetime.datetime.strptime(resu[1], "%Y%m%d")).strftime('%Y-%m-%d')
                try:
                    # 写入excel
                    Openpyxl_PO.setRowValue({j+1: [state_dt,str(resu[0]),float(resu[2]),float(resu[5]),float(resu[3]),float(resu[4]),float(resu[9]),float(resu[10]),float(resu[6]),float(resu[7]),float(resu[8])]},stock_pool[i])
                except Exception as err:
                    continue

        print('All Finished!')


    def svm(self, varStockCode):

        dc = DC.data_collect(varStockCode)

        train = dc.data_train
        target = dc.data_target
        test_case = [dc.test_case]

        model = svm.SVC()  # 建模
        model.fit(train, target)  # 训练
        ans2 = model.predict(test_case)  # 预测

        print("[" + varStockCode + "] => " + str(ans2[0]))  # 预测下一个交易日涨跌，1表示涨，0表示不涨。


if __name__ == '__main__':

    Init_StockALL_Sp1 = Init_StockALL_Sp()

    # 数据采集
    # Init_StockALL_Sp1.getStockData(['603439.SH', '002864.SZ', '301278.SZ', '300832.SZ', '300957.SZ'], '20221008', '20230119', 'd://stock.xlsx')
    Init_StockALL_Sp1.getStockData(['603439.SH'], '20220926', '20230119', 'd://stock.xlsx')

    Init_StockALL_Sp1.svm('603439.SH')
    # Init_StockALL_Sp1.svm('002864.SZ')
    # Init_StockALL_Sp1.svm('301278.SZ')
    # Init_StockALL_Sp1.svm('300832.SZ')
    # Init_StockALL_Sp1.svm('300957.SZ')






