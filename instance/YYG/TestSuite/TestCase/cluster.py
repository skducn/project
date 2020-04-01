# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Version    : V0.1
# Date       : 2017-5-23
# Description: 集群应用管理系统
"""
    @classmethod
    def setUpClass(self):  所有测试函数运行前执行一次

    @classmethod
    def tearDownClass(self):  所有测试函数运行完后执行一次

    def setup(self):  每个测试函数运行前执行

    def teardown(self):  每个测试函数运行后执行
    """
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from Cos.Config.configcluster import *
Level_PO = LevelPO(driver, varURL, varTitle)
net_PO = netPO()
sheet, newbk = Level_PO.iniExcel(varExcel, varExcelSheetName)


class Cluster(unittest.TestCase):

    def testMain(self):
        # 遍历main (测试函数)
        sleep(2)
        print u"\n\n----------------------------------------------------------------------"
        for i in range(1, sheet[0].nrows):
            if sheet[0].cell_value(i, 0) == "Y":
                self.Scene = sheet[0].cell_value(i, 1)
                self.SceneDesc = sheet[0].cell_value(i, 2)

                # 遍历TestCase及调用函数模块,定位测试用例位置及数量
                case1 = caseN = 0
                for j in range(1, sheet[1].nrows):
                    case1 = case1 + 1
                    if sheet[1].cell_value(j, 2) == self.Scene:
                        for k in range(case1 + 1, 100):  # 假设有100个Case
                            if k + 1 > sheet[1].nrows:  # 最后一行
                                caseN = caseN + 1
                                break
                            elif sheet[1].cell_value(k, 1) == "" and sheet[1].cell_value(k, 2) == "":
                                caseN = caseN + 1
                            elif sheet[1].cell_value(k, 1) == "skip":
                                caseN = caseN + 1
                            else:
                                caseN = caseN + 1
                                break
                        break
                # if self.Maincol2 == "skip":
                #     case1 = case1 + 1
                #     caseN = caseN - 1

                # 遍历 Testcase1~TestCaseN
                for l in range(case1, caseN + case1):
                    try:
                        if sheet[1].cell_value(l, 1) == "skip":
                            newWs = newbk.get_sheet(1)
                            newWs.write(l, 0, "skip", STYLEGRAY25)
                            newbk.save(varExcel)
                        elif sheet[1].cell_value(l, 5) == "":
                            pass
                        else:
                            varRtn = eval(sheet[1].cell_value(l, 5))
                            newWs = newbk.get_sheet(1)
                            try:
                                if "error" in varRtn:
                                    newWs.write(l, 0, varDayTime14, STYLERED)
                                    newWs.write(l, 6, varRtn, STYLERED)
                                else:
                                    newWs.write(l, 0, varDayTime14, STYLEBLUE)
                                    newWs.write(l, 6, varRtn, STYLEBLUE)
                                newbk.save(varExcel)
                            except:
                                print "return返回错误！"
                    except:
                        print "Errorrrrrr , Excel(" + str(l + 1) + ") , " + sheet[1].cell_value(case1, 2) + " , " + sheet[1].cell_value(
                            l, 3) + " , " + sheet[1].cell_value(l, 4) + " , " + sheet[1].cell_value(l, 5)
                        newWs = newbk.get_sheet(1)
                        newWs.write(l, 0, varDayTime14, STYLERED)
                        newbk.save(varExcel)

    ''' cluster业务场景1 '''

    def login(self, varUser, varPass):
        ''' C1-1,登录系统 '''

        print u"<登录 >>>>>>>>>>>>>>>>>>>>>>>>>>"
        try:
            Level_PO.open(3)
            Level_PO.inputID('_username', varUser)
            Level_PO.inputNAME('password', varPass)
            Level_PO.clickTAGNAME('button', 4)
        except:
            return u"error, 登录失败！"
        print u" 登录, Done\n"
        return u"无"

    def createServer(self, varServer, varType, varIP, varDesc):
        # C1-1, 新增服务器
        # 规则：服务器名不能重复
        # self.createServer(u'Ser????', u'', u'10.111.10.37', u'desc123')

        print u"<C1-S1, 新增服务器 >>>>>>>>>>>>>>>>>>>>>>>>>>"

        # 服务器管理
        Level_PO.clickXPATH("//a[@onclick=\"gotoUrl('pcList');\"]", 2)

        # 新增
        Level_PO.clickXPATH("//button[@onclick=\"register();\"]", 2)

        # 服务器名称
        Level_PO.inIframeDiv("[@id='registerTaskHost']", 2)

        # 自动生成4个数字, 参数中有N个????会自动替换成数字
        varWenhao = len(varServer.split("?")) - 1
        varServer = varServer.replace("?", "")
        self.comServerName = varServer + "".join(Level_PO.myfunc(varWenhao))
        print u'self.comServerName = ' + self.comServerName
        Level_PO.inputID(u"hostName", self.comServerName)

        # 服务器类型(只有window)
        # 服务器IP
        Level_PO.inputID(u'hostServerIp',varIP)
        # 服务器描述
        Level_PO.inputID(u'description', varDesc)
        # 保存
        Level_PO.clickXPATH("//button[@onclick=\"save()\"]", 2)
        Level_PO.outIframe(2)

        # 检查表 server_info.name记录是否存在
        tblRtnStatus = Level_PO.get_TblExist(cur, conn, "server_info", "server_id", "name=" + self.comServerName)
        if tblRtnStatus != 1:
            print u'errorrrrr - S1,新增服务器,表server_info记录未找到!'
            return u'errorrrrr - S1,新增服务器,表server_info记录未找到!'
        print u"S1,Done"
        return u"S1,新增服务器,表server_info记录"

    def createCluster(self, varCluster, varBelong, varPath, varDesc):
        # C1-2, 新增集群
        # 规则：服务器名不能重复
        # self.createCluster(u'Cluster????', self.comServername, u'c:\\test2', u'desc cluster666')

        self.comServername = u"Ser1759"
        print u"<C1-S2, 新增集群 >>>>>>>>>>>>>>>>>>>>>>>>>>"

        # 集群管理
        Level_PO.clickXPATH("//a[@onclick=\"gotoUrl('clusterList');\"]", 2)

        # 新增
        Level_PO.clickXPATH("//button[@onclick=\"register();\"]", 2)
        try:
            # 集群名称
            Level_PO.inIframe("layui-layer-iframe1", 3)  # 进入frame
            # 自动生成4个数字, 参数中有N个????会自动替换成数字
            varWenhao = len(varCluster.split("?")) - 1
            varCluster = varCluster.replace("?", "")
            self.comClusterName = varCluster + "".join(Level_PO.myfunc(varWenhao))
            print u'self.comClusterName = ' + self.comClusterName
            Level_PO.inputNAME(u'clusterName', self.comClusterName)
            # 所属服务器
            Level_PO.selectNAMEtext(u"serverType", varBelong)
            # 路径
            Level_PO.inputNAME(u'file_path', varPath)
            # 集群描述
            Level_PO.inputXPATH("//textarea[@name='description']", varDesc)
            # 保存
            Level_PO.clickXPATH("//button[@onclick=\"save()\"]", 2)
            Level_PO.outIframe(2)
        except:
            print u"errorrrr, C1-S2，新增集群操作有误！"
            return u"errorrrr, C1-S2，新增集群操作有误！"

        # 检查表 cluster_info.name记录是否存在
        tblRtnStatus = Level_PO.get_TblExist(cur, conn, "cluster_info", "cluster_id", "name=" + self.comClusterName)
        if tblRtnStatus != 1:
            print u'errorrrrr - S2,新增集群,表cluster_info记录未找到!'
            return u'errorrrrr - S2,新增集群,表cluster_info记录未找到!'

        print u"S2,Done"
        return u"S2,新增集群,表cluster_info记录"

    def releaseCluster(self, varClusterName):
        # self.releaseCluster(self.comClusterName)
        # self.releaseCluster(u'Cluster9954')
        # C1-4, 发布集群

        print u"<C1-S3, 发布集群 >>>>>>>>>>>>>>>>>>>>>>>>>>"

        # 集群管理
        Level_PO.clickXPATH("//a[@onclick=\"gotoUrl('clusterList');\"]", 2)

        # 1-2、获取cluster_info.cluster_id
        tblRtnValue = Level_PO.get_TblOneValue(cur, conn, "cluster_info", "name=" + varClusterName, "cluster_id,cluster_id")
        varRadio = int(tblRtnValue) - 1
        Level_PO.clickXPATH("//input[@data-index='" + str(varRadio) + "']", 2)

        # 点击发布
        Level_PO.clickXPATH("//button[@onclick=\"javascript:versionList();\"]", 2)

        # 集群配置版本信息
        Level_PO.inIframe("layui-layer-iframe1", 2)
        Level_PO.clickXPATH("//input[@data-index='0']", 2)  # 选择某一条
        Level_PO.clickXPATH("//button[@onclick=\"publish()\"]", 2)  # 点击发布
        Level_PO.clickXPATH("//button[@onclick=\"register();\"]", 2)  # 点击新增
        Level_PO.outIframe(2)

        Level_PO.inIframe("layui-layer-iframe2", 2)
        Level_PO.inputNAME(u"worker_processes", u'10')  # 开启进程数
        Level_PO.inputNAME(u"worker_connections", u'2048')  # 最大连接数
        Level_PO.inputNAME(u'keepalive_timeout', u'66')  # 连接超时时间
        Level_PO.selectNAMEtext(u'serverType0', u'contain100')  # 集群
        Level_PO.inputNAME(u'weight0', u'22')  # 权重
        Level_PO.inputNAME(u'version', u'1.6.0')  # 版本
        Level_PO.inputNAME(u'description', u'desc1.6.0')  # 描述
        Level_PO.clickXPATH("//button[@onclick=\"save()\"]", 2)
        Level_PO.outIframe(2)




if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(Cluster)  # 构造测试集
    unittest.TextTestRunner(verbosity=2).run(suite1)  # 执行测试

