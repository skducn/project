# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-5-12
# Description: 质控对象库
# *****************************************************************

from instance.zyjk.EHR.controlRuleNew.config.config import *
from PO.FilePO import *
File_PO = FilePO()

class RulePO(object):

    def __init__(self):
        self.Time_PO = TimePO()
        self.Log_PO = LogPO(logFile, fmt='%(levelname)s - %(message)s - %(asctime)s')  # 输出日志


    # 1，执行sql文件
    def execSqlFile(self, varSqlFile):
        Sqlserver_PO.ExecQueryBySQL(File_PO.getLayerPath("./config") + "\\" + varSqlFile)

    # 2，执行SQL命令
    def execQuery(self, varSQL):
        x = Sqlserver_PO.ExecQuery(varSQL)
        return x






