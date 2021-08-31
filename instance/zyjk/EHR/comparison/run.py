# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2021-8-31
# Description: 电子健康档案数据比对自动化，ITF与DC库中表字段数据比对。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import os,sys
sys.path.append("../../../../")
from PO.OpenpyxlPO import *
from PO.SqlserverPO import *
from PO.DataPO import *
from PO.ListPO import *
from PO.TimePO import *
List_PO = ListPO()
Time_PO = TimePO()
from time import sleep


# 初始化数据
os.system('d: && cd /myGit/testTeam/ehr/comparison && git pull &&  copy EHR_itf与dc数据比对表.xlsx D:\\51\\python\\project\\instance\\zyjk\\EHR\\comparison')
Openpyxl_PO = OpenpyxlPO("EHR_itf与dc数据比对表.xlsx")
Openpyxl_PO.clsColData(4)
Sqlserver_PO_itf = SqlServerPO("192.168.0.234", "sa", "Zy@123456", "EHRITF")
Sqlserver_PO_dc = SqlServerPO("192.168.0.234", "sa", "Zy@123456", "EHRDC")
varRandomIdCard = 15  # 随机获取N条身份证


# 随机从 ITF_TB_EHR_MAIN_INFO 库获取 N 条身份证
r_itf_ITF_TB_EHR_MAIN_INFO_icCardNo = Sqlserver_PO_itf.ExecQuery("SELECT idCardNo  FROM ITF_TB_EHR_MAIN_INFO")
suiji = random.sample(range(1, len(r_itf_ITF_TB_EHR_MAIN_INFO_icCardNo)), varRandomIdCard)
suiji.sort()

# 输出比对字段数量
print((" 测试" + str(Openpyxl_PO.l_getTotalRowCol()[0]-1) + "个字段 ").center(100, "-"))

# 遍历身份证
for i in range(len(r_itf_ITF_TB_EHR_MAIN_INFO_icCardNo)):
    for j in range(len(suiji)):
        if suiji[j] == i :
            idCardNo = (r_itf_ITF_TB_EHR_MAIN_INFO_icCardNo[i][0])

            # 获取记录
            r_itf_ITF_TB_EHR_MAIN_INFO = Sqlserver_PO_itf.ExecQuery("SELECT *  FROM ITF_TB_EHR_MAIN_INFO where idCardNo='%s'" % (idCardNo))
            # print(r_itf_ITF_TB_EHR_MAIN_INFO)
            r_dc_HrCover = Sqlserver_PO_dc.ExecQuery("SELECT * FROM HrCover where ArchiveNum='%s'" % (idCardNo))
            # convert(nvarchar(20), Name) 乱码
            # convert(nvarchar(20), ArchiveUnit) 乱码
            # print(r_dc_HrCover)
            r_dc_HrPersonBasicInfo = Sqlserver_PO_dc.ExecQuery("SELECT *  FROM HrPersonBasicInfo where ArchiveNum='%s'" % (idCardNo))
            # print(r_dc_HrPersonBasicInfo)


            # 将数据转换成字典
            d_itf_ITF_TB_EHR_MAIN_INFO = List_PO.lists2dict(Sqlserver_PO_itf.getAllFields('ITF_TB_EHR_MAIN_INFO'), list(r_itf_ITF_TB_EHR_MAIN_INFO[0]))


            l_dc_HrCover = list(r_dc_HrCover[0])
            l_dc_HrCover[3] = (l_dc_HrCover[3].encode('latin-1').decode('gbk'))
            l_dc_HrCover[4] = (l_dc_HrCover[4].encode('latin-1').decode('gbk'))
            l_dc_HrCover[17] = (l_dc_HrCover[17].encode('latin-1').decode('gbk'))
            d_dc_HrCover = List_PO.lists2dict(Sqlserver_PO_dc.getAllFields('HrCover'), l_dc_HrCover)
            # print(d_dc_HrCover)

            l_dc_HrPersonBasicInfo = list(r_dc_HrPersonBasicInfo[0])
            l_dc_HrPersonBasicInfo[1] = (l_dc_HrPersonBasicInfo[1].encode('latin-1').decode('gbk'))
            d_dc_HrPersonBasicInfo = List_PO.lists2dict(Sqlserver_PO_dc.getAllFields('HrPersonBasicInfo'), l_dc_HrPersonBasicInfo)
            # print(d_dc_HrPersonBasicInfo)

            # 执行比对
            l_all = Openpyxl_PO.l_getRowData()
            c = 0
            for i in range(len(l_all)):
                # if l_all[i][2] == "比对结果" or l_all[i][2] == "error":
                if l_all[i][2] == "比对结果" :
                    c = c + 1
                else:
                    if str(l_all[i][0]).split(".")[0] == "ITF_TB_EHR_MAIN_INFO":
                        left = (d_itf_ITF_TB_EHR_MAIN_INFO[str(l_all[i][0]).split(".")[1]])
                    if str(l_all[i][1]).split(".")[0] == "HrCover":
                        right = (d_dc_HrCover[str(l_all[i][1]).split(".")[1]])
                    if str(l_all[i][1]).split(".")[0] == "HrPersonBasicInfo":
                        right = (d_dc_HrPersonBasicInfo[str(l_all[i][1]).split(".")[1]])
                    if left == right or (left == "" and right == None) :
                        if Openpyxl_PO.getCellValue(c + 1, 4) == None:
                            Openpyxl_PO.setCellValue(c + 1, 3, "ok")
                        else:
                            Openpyxl_PO.setCellValue(c + 1, 3, "error")
                    else:
                        Openpyxl_PO.setCellValue(c + 1, 3, "error")
                        x = Openpyxl_PO.getCellValue(c + 1, 4)
                        if x == None :
                            Openpyxl_PO.setCellValue(c + 1, 4, str(idCardNo) + " , " + str(left) + " <> " + str(right))
                        else:
                            x = str(x) + "\n" + str(idCardNo) + " , " + str(left) + " <> " + str(right)
                            Openpyxl_PO.setCellValue(c + 1, 4, x)

                        # 控制台只输出错误结果：
                        print(str(j + 1) + ", " + str(idCardNo) + " , " + str(l_all[i][0]).split(".")[0] + "." + str(l_all[i][0]).split(".")[1] + "(" + str(left) + ") <> "
                              + str(l_all[i][1]).split(".")[0] + "." + str(l_all[i][1]).split(".")[1] + "(" + str(right) + ")")
                    c = c + 1
                    Openpyxl_PO.save()


# 将结果保存到git
currDate = Time_PO.getDate()
currDate = "EHR_itf与dc数据比对表_" + str(currDate) + ".xlsx"
os.system('copy EHR_itf与dc数据比对表.xlsx D:\\myGit\\testTeam\\EHR\\comparison\\result\\' + currDate + '&& cd D:\\myGit\\testTeam\ && git add . && git commit -m "add result" && git push')

