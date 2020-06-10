# coding=utf-8
# *****************************************************************
# Author     : John
# Date       : 2020-5-12
# Description: 质控对象库
# *****************************************************************

import instance.zyjk.EHR.controlRuleNew.config.readConfig as readConfig
localReadConfig = readConfig.ReadConfig()
from PO.LogPO import *
from PO.NetPO import *
from PO.DataPO import *
from PO.ColorPO import *
from PO.ExcelPO.ExcelPO import *
from PO.TimePO import *
from PO.SqlserverPO import *
from PO.FilePO import *
from time import sleep
from multiprocessing import Process

class RulePO(object):

    def __init__(self):
        global ruleType,isRun,caseFrom,caseTo,curl,rulesApi,archiveNum,jar,excel,excelSheet1
        self.ruleType = localReadConfig.get_filter("ruleType")
        self.isRun = localReadConfig.get_filter("isRun")
        self.caseFrom = localReadConfig.get_filter("caseFrom")
        self.caseTo = localReadConfig.get_filter("caseTo")
        self.caseList = localReadConfig.get_filter("caseList")
        self.curl = localReadConfig.get_http("curl")
        self.rulesApi = localReadConfig.get_http("rulesApi")
        self.archiveNum = localReadConfig.get_http("archiveNum")
        self.jar = localReadConfig.get_jar("jar")
        self.excelFile = localReadConfig.get_excel("excelFile")
        self.excelFileSheetName = localReadConfig.get_excel("excelFileSheetName")

        host = localReadConfig.get_database("host")
        username = localReadConfig.get_database("username")
        password = localReadConfig.get_database("password")
        database = localReadConfig.get_database("database")
        self.Sqlserver_PO = SqlServerPO(host, username, password, database)
        # logFile = localReadConfig.get_log("logFile")
        self.Time_PO = TimePO()
        self.File_PO = FilePO()
        self.Excel_PO = ExcelPO()
        # self.Log_PO = LogPO(logFile, fmt='%(levelname)s - %(message)s - %(asctime)s')  # 输出日志

    # 执行SQL命令
    def execQuery(self, varSQL):
        return self.Sqlserver_PO.ExecQuery(varSQL)


    def switchPath(self, varSwitchPath, varFile):
        # 切换文件路径
        return self.File_PO.getLayerPath(varSwitchPath) + "\\" + varFile



if __name__ == '__main__':
    currentPath = os.path.split(os.path.realpath(__file__))[0]
    getConfig = os.path.join(currentPath, "config.ini")
    print(currentPath)
    # print(File_PO.getLayerPath("../config") + "\\" + jar)
    Rule_PO = RulePO()

    print(Rule_PO.curl + " " + Rule_PO.rulesApi + Rule_PO.archiveNum)


