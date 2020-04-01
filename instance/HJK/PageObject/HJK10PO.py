# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2017-11-20
# Description: HJK1.0
#***************************************************************

from Dangjian.Config.config import *
varUrlPrefix = u"https://hjk.iotcetc.com:18080/his/"  # 访问URL

class HJK10PO(object):

    def __init__(self, Level_PO):
        self.Level_PO = Level_PO




    def flowSetup(self, varExecute, *varObjects):

        '''流程设置'''

        # Dangjian20_PO.flowSetup(u"del", u"all") ， 删除所有审核人。
        # Dangjian20_PO.flowSetup(u"del", u"支部书记") ， 删除支部书记审核人
        # Dangjian20_PO.flowSetup(u"del", u"支部书记,审核项目")  ， 删除 审核项目,支部书记2个审核人
        # Dangjian20_PO.flowSetup(u"del", u"33,项目管理员,33")  # 重复写了33，容错不受影响。

        # Dangjian20_PO.flowSetup(u"add", u"审核项目")  ， 添加审核项目审核人
        # Dangjian20_PO.flowSetup(u"add", u"支部书记,审核项目,支部学习委员") ， 添加审核项目,支部书记,支部学习委员3个审核人。
        # Dangjian20_PO.flowSetup(u"add", u"项目管理员,3333,33") , 添加的人 3333不存在，则忽略。

        Level_PO.clickLINKTEXT(u'流程设置', 2)

        if varExecute == u"del" and varObjects[0] == u"all":
            #  岗位人数
            varPost = Level_PO.get_attFromAtts(u"//a[@class='btn btn-block btn-info']", u"onclick", u"all")
            for i in range(len(varPost)):
                #  获取所有的岗位的ID，如 onclick="doAddRole('6', '审核项目')" ， ID=6
                varObjectId = str(varPost[i]).replace(u"doAddRole('", u"").split(u"'")[0]
                if Level_PO.isElementId(u"approval-item-" + varObjectId):
                    Level_PO.clickXPATH(u"//div[@id='approval-item-" + varObjectId + u"']/i[1]", 2)
            Level_PO.clickXPATH(u"//button[@class='btn btn-sm btn-primary']", 6)
            return u"已取消 -> 所有审批人"
            # self.varIsAudit = u"N"

        # 取消审批人

        elif varExecute == u"del":
            dict1 = {}
            varPost = Level_PO.get_attFromAtts(u"//a[@class='btn btn-block btn-info']", u"onclick", u"all")
            for i in range(len(varPost)):
                dictKey = str(varPost[i]).replace(u"doAddRole('", u"").split(u"'")[0]
                dictValue = str(varPost[i]).replace(u"doAddRole('", u"").split(u"', ")[1].replace(u"'", u"").replace(u')', u"")
                dict1[dictKey] = dictValue

            varIsComma = str(varObjects[0]).count(",")

            # 取消多个审批人
            if int(varIsComma) > 0:
                for j in range(int(varIsComma)+1):
                    varAudit = str(varObjects[0]).split(",")[j]
                    for dictKey in dict1:
                        if varAudit == str(dict1[dictKey]):
                            varKey = list(dict1.keys())[list(dict1.values()).index(dict1[dictKey])]  # 从字典value得到对应的key
                            if Level_PO.isElementId(u"approval-item-" + varKey):
                                Level_PO.clickXPATH(u"//div[@id='approval-item-" + varKey + u"']/i[1]", 2)
                                return u"已取消 -> " + str(dict1[dictKey]) + u" 审批人"
            else:

                # 取消单个审批人
                for i in range(len(varPost)):
                    dictKey = str(varPost[i]).replace(u"doAddRole('", u"").split(u"'")[0]
                    dictValue = str(varPost[i]).replace(u"doAddRole('", u"").split(u"', ")[1].replace(u"'", u"").replace(u')',u"")
                    dict1[dictKey] = dictValue
                    if varObjects[0] == str(dict1[dictKey]):
                        varKey = list(dict1.keys())[list(dict1.values()).index(dict1[dictKey])]
                        if Level_PO.isElementId(u"approval-item-" + varKey):
                            Level_PO.clickXPATH(u"//div[@id='approval-item-" + varKey + u"']/i[1]", 2)
                            return u"已取消 -> " + str(dict1[dictKey]) + u" 审批人"

            Level_PO.clickXPATH(u"//button[@class='btn btn-sm btn-primary']", 2)

        # 点击审批人

        elif varExecute == u"add":
            varIsComma = str(varObjects[0]).count(",")

            # 添加多个审批人
            if int(varIsComma) > 0:
                for j in range(int(varIsComma) + 1):
                    varTmp = str(varObjects[0]).split(",")[j]
                    try:
                        Level_PO.clickLINKTEXT(varTmp, 2)
                        return u"已添加 -> " + varTmp + u" 审批人"
                    except:
                        print u"warningggggggggg, " + varTmp + u" 没有找到，无法添加。"
            else:

                # 添加单个审批人
                Level_PO.clickLINKTEXT(varObjects[0], 2)
                return u"已添加 -> " + varObjects[0] + u" 审批人"
            Level_PO.clickXPATH(u"//button[@class='btn btn-sm btn-primary']", 6)

    def orgUsers(self, varArchitecture):

        '''架构切换'''

        if not varArchitecture in self.Level_PO.getXpathText(u"//a[@class='dropdown-toggle']"):
            self.Level_PO.clickXPATH(u"//a[@class='dropdown-toggle']", 2)
            dict2 = self.Level_PO.getXpathsAttrdict(u"//ul[@class='dropdown-menu']/li/a", u"href")
            for key in dict2:
                if varArchitecture in key:
                    self.Level_PO.clickXPATH(u"//a[@href='" + str(dict2[key]).split(varUrlPrefix)[1] + u"']", 2)
                    break

        '''用户及权限管理'''

        self.Level_PO.clickLINKTEXT(u'用户及权限管理', 2)

        self.Level_PO.clickLINKTEXT(u'架构及用户管理', 10)
        # print u"errorrrrrrrrrrr", sys._getframe().f_lineno, u"'架构及用户管理'不存在！！！", __file__
        # os._exit(0)
        listA = []
        # listA = Level_PO.getList_XpathsText(u"//ul[@id='treeDemo']/li/ul/li")
        listA = self.Level_PO.getXpathsText(u"//ul[@id='treeDemo']/li/ul/li")

        return listA
