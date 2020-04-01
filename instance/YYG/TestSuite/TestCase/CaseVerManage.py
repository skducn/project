# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 1.0.0
# Date       : 2017-4-9
# Description: 任务调度引擎管理客户端入口 , 版本管理
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


from Cos.Config.config import *
from Cos.PageObject.TaskManagePO import *

TaskManage_PO = TaskManagePO(driver, sheetMain.cell_value(1, 5), sheetMain.cell_value(3, 5))

class CaseVerManage(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print u"C3，版本管理"

    def test_1(self):

        # 业务场景：创建一个作业任务
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # 作业管理 - 作业框架管理
        Level_PO.selectMenu("//a[@class='dropdown-toggle']", u"版本管理", "//a[@href='#']", u"版本管理")

        # 版本管理
        Level_PO.clickXPATH("//button[@onclick=\"showTaskVersion()\"]", 4)

        # 上传作业文件
        Level_PO.clickXPATH("//button[@onclick=\"addTaskVersion()\"]", 4)
        # 作业版本
        Level_PO.inIframe("layui-layer-iframe1", 1)
        Level_PO.inputID("_version", u'1.1.1')
        # 版本描述
        Level_PO.inputID("_versionDesc", u'自动描述1。1。1')

        # 上传文件??
        Level_PO.script()
        sleep(3)
        Level_PO.sendID("_taskFilePath", u'//Users//linghuchong//Downloads//51//Project//Cos//308976358703235072.zip',
                        2)

        # 保存
        Level_PO.clickXPATH("//button[@onclick=\"save()\"]", 3)
