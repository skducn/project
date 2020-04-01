# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : 1.0.0
# Date       : 2017-4-9
# Description: 任务调度引擎管理客户端入口 , 作业管理
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


from Cos.Config.config import *
from Cos.PageObject.TaskManagePO import *

TaskManage_PO = TaskManagePO(driver, sheetMain.cell_value(1, 5), sheetMain.cell_value(3, 5))

class CaseTaskManage(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print u"C2，作业管理"




    def test_3(self):

        # 业务场景：创建一个作业任务
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # 作业管理 - 作业框架管理
        Level_PO.selectMenu("//a[@class='dropdown-toggle']", u"作业管理", "//a[@href='#']", u"作业框架管理")

        # # 选择第二个
        # TaskManage_PO.clickONline(2)
        # # 上线
        # Level_PO.clickXPATH("//a[@class='layui-layer-btn0']", 2)
        # 取消
        # Level_PO.clickXPATH("//a[@class='layui-layer-btn1']", 2)

        # # 编辑
        # Level_PO.clickXPATH("//button[@onclick=\"update();\"]",2)
        # # 修改
        # Level_PO.inIframe("layui-layer-iframe1", 1)
        # Level_PO.clickXPATH("//button[@onclick=\"submitForm()\"]",2)
        # Level_PO.outIframe(1)

        # [任务属性列表]

        # 点击注册
        Level_PO.clickXPATH("//button[@onclick=\"register();\"]", 1)


        Level_PO.inIframe("layui-layer-iframe1", 1)

        # [模式1, 简单触发器 + 串行]
        # 对应宿主机
        Level_PO.select_byName1('taskHostId', sheetParam.cell_value(4, 1).split(":")[1])
        # 所属组名称
        Level_PO.select_byName1('taskGroup', sheetParam.cell_value(4, 2).split(":")[1])
        # 任务名称 varRandom4
        Level_PO.inputNAME('taskName', u'auTask' + Level_PO.varRandom4)
        # 触发器类型
        Level_PO.select_byName1('cronFlag', sheetParam.cell_value(4, 4).split(":")[1])
        # 执行间隔
        Level_PO.inputID('_intervalTime', sheetParam.cell_value(4, 6).split(":")[1])
        # 最多执行次数
        Level_PO.inputNAME('maxTimes', sheetParam.cell_value(4, 7).split(":")[1])
        # 运行方式（串）
        Level_PO.select_byName1('runMode', sheetParam.cell_value(4, 8).split(":")[8])
        # 起始执行时间,切换框架   //今天
        Level_PO.clickXPATH("//input[@id='_timeStr']", 1)
        Level_PO.outIframe(1)
        Level_PO.inIframeXPATH("//body[@class='gray-bg top-navigation']/div[4]/iframe", 1)
        Level_PO.clickXPATH("//input[@id='dpTodayInput']", 1)
        Level_PO.outIframe(1)
        Level_PO.inIframe("layui-layer-iframe1", 1)
        # # 保存
        Level_PO.clickXPATH("//button[@onclick=\"submitForm()\"]", 1)
        # # 退出
        # Level_PO.clickXPATH("//button[@onclick=\"cancelForm()\"]", 2)



        # [模式2, 简单触发器 + 并行]

        # 对应宿主机
        Level_PO.select_byName1('taskHostId', u'宿主1')
        # 所属组名称
        Level_PO.select_byName1('taskGroup', u'group1')
        # 任务名称
        Level_PO.inputNAME('taskName', u'testjob5')
        # 触发器类型
        Level_PO.select_byName1('cronFlag', u'简单触发器')
        # 执行间隔
        Level_PO.inputID('_intervalTime', u'1000')
        # 最多执行次数
        Level_PO.inputNAME('maxTimes', u'3')
        # 运行方式（并）
        Level_PO.select_byName1('runMode', u'并行')
        # 并行任务最大运行数量
        Level_PO.inputID('_parallelMaxNum', 20)
        # 起始执行时间,切换框架
        Level_PO.clickXPATH("//input[@id='_timeStr']", 1)
        Level_PO.outIframe(1)
        Level_PO.inIframeXPATH("//body[@class='gray-bg top-navigation']/div[4]/iframe", 1)
        Level_PO.clickXPATH("//input[@id='dpTodayInput']", 1)
        Level_PO.outIframe(1)
        Level_PO.inIframe("layui-layer-iframe1", 1)
        # # 保存
        Level_PO.clickXPATH("//button[@onclick=\"submitForm()\"]", 1)

        # [模式3, cron表达式 + 串行]
        # [模式4, cron表达式 + 并行]





        # # 编辑
        # Level_PO.clickXPATH("//button[@onclick=\"update();\"]",2)
        #
        # # 发布
        # Level_PO.clickXPATH("//button[@onclick=\"showVersionPublish()\"]",2)
        #
        # # 切换宿主
        # Level_PO.clickXPATH("//button[@onclick=\"changeHost();\"]",2)
        #
        # 刷新
        # Level_PO.clickXPATH("//button[@onclick=\"refresh()\"]",2)


        # # 选择所属组
        # Level_PO.select_byName('groupName', u'group1')
        # # 任务名称
        # Level_PO.inputID('_taskName', u'job')
        # # 点击搜索
        # Level_PO.clickXPATH("//button[@type='submit']", 3)

