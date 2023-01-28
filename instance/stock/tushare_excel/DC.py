# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-06-15
# Description: tushare 之采集数据
# pip3.9 install tushare --upgrade
# 获取token https://tushare.pro/user/token
# *****************************************************************
import numpy as np
import pymysql
from PO.OpenpyxlPO import *
Openpyxl_PO = OpenpyxlPO("d://stock.xlsx")

class data_collect(object):

    def __init__(self, varStockCode):
        ans = self.collectDATA(varStockCode)

    def collectDATA(self, varStockCode):

        self.date_seq = []
        self.open_list = []
        self.close_list = []
        self.high_list = []
        self.low_list = []
        self.vol_list = []
        self.amount_list = []

        row = Openpyxl_PO.getRowCol(varStockCode)
        # print(row[0])
        for i in range(row[0]):
            # print(Openpyxl_PO.getCellValue(i+1, 1))
            self.date_seq.append(Openpyxl_PO.getCellValue(i+1, 1,varStockCode))
            self.open_list.append(Openpyxl_PO.getCellValue(i+1, 3,varStockCode))
            self.close_list.append(Openpyxl_PO.getCellValue(i+1, 4,varStockCode))
            self.high_list.append(Openpyxl_PO.getCellValue(i+1, 5,varStockCode))
            self.low_list.append(Openpyxl_PO.getCellValue(i+1, 6,varStockCode))
            self.vol_list.append(Openpyxl_PO.getCellValue(i+1, 7,varStockCode))
            self.amount_list.append(Openpyxl_PO.getCellValue(i+1, 8,varStockCode))

            # self.date_seq.append(done_set[i][0])
            # self.open_list.append(float(done_set[i][2]))
            # self.close_list.append(float(done_set[i][3]))
            # self.high_list.append(float(done_set[i][4]))
            # self.low_list.append(float(done_set[i][5]))
            # self.vol_list.append(float(done_set[i][6]))
            # self.amount_list.append(float(done_set[i][7]))


        # 将日线行情整合为训练集(其中self.train是输入集，self.target是输出集，self.test_case是end_dt那天的单条测试输入)
        self.data_train = []
        self.data_target = []
        self.data_target_onehot = []
        self.cnt_pos = 0
        self.test_case = []

        # print(len(self.close_list))
        for i in range(1,len(self.close_list)):
            train = [self.open_list[i-1],self.close_list[i-1],self.high_list[i-1],self.low_list[i-1],self.vol_list[i-1],self.amount_list[i-1]]
            # train = [self.open_list[i],self.close_list[i],self.high_list[i],self.low_list[i],self.vol_list[i],self.amount_list[i]]
            self.data_train.append(np.array(train))

            if float(self.close_list[i])/float(self.close_list[i-1]) > 1.0:
            # if float(self.close_list[i+1])/float(self.close_list[i]) > 1.0:
                self.data_target.append(float(1.00))
                self.data_target_onehot.append([1,0,0])
            else:
                self.data_target.append(float(0.00))
                self.data_target_onehot.append([0,1,0])
        self.cnt_pos =len([x for x in self.data_target if x == 1.00])
        self.test_case = np.array([self.open_list[-1],self.close_list[-1],self.high_list[-1],self.low_list[-1],self.vol_list[-1],self.amount_list[-1]])
        self.data_train = np.array(self.data_train)
        self.data_target = np.array(self.data_target)
        return 1