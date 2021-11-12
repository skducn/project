# -*- coding: utf-8 -*-
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2021-8-31
# Description: 电子健康档案化，ITF与DC库中表字段数据比对。（公司）
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import os, sys
sys.path.append("../../../../")
from PO.OpenpyxlPO import *
from PO.SqlserverPO import *
from PO.DataPO import *
from PO.ListPO import *
List_PO = ListPO()
from PO.ColorPO import *
Color_PO = ColorPO()
from PO.TimePO import *
Time_PO = TimePO()
from time import sleep


# os.system('d: && cd /myGit/testTeam/ehr/自动化/comparison && git pull &&  copy EHR.xlsx D:\\51\\python\\project\\instance\\zyjk\\EHR\\comparison')

# 初始化数据
Openpyxl_PO = OpenpyxlPO("EHR.xlsx")
Openpyxl_PO.clsColData(4)
Sqlserver_PO_itf = SqlServerPO("192.168.0.234", "sa", "Zy@123456", "EHRITF", "")
Sqlserver_PO_dc = SqlServerPO("192.168.0.234", "sa", "Zy@123456", "EHRDC", "")


# 测试次数（随机身份证）
QTY = 1

# 输出比对字段数量
print((" 测试" + str(Openpyxl_PO.l_getTotalRowCol()[0]-1) + "个字段 ").center(100, "-"))

# 遍历身份证
for i in range(QTY):

    print("-" * 100)

    # ITF库
    # 封面与基本信息表
    l_idCardNo = Sqlserver_PO_itf.execQuery("SELECT idCardNo  FROM ITF_TB_EHR_MAIN_INFO")
    idCardNo = random.choice(l_idCardNo)
    print("ITF_TB_EHR_MAIN_INFO  => " + str(idCardNo[0]))
    r_ITF_TB_EHR_MAIN_INFO = Sqlserver_PO_itf.execQuery("SELECT *  FROM ITF_TB_EHR_MAIN_INFO where idCardNo='%s'" % (idCardNo[0]))
    d_ITF_TB_EHR_MAIN_INFO = List_PO.lists2dict(Sqlserver_PO_itf.l_getAllField('ITF_TB_EHR_MAIN_INFO'), list(r_ITF_TB_EHR_MAIN_INFO[0]))  # 将数据转换成字典
    Color_PO.consoleColor("31", "33", "d_ITF_TB_EHR_MAIN_INFO => " + str(d_ITF_TB_EHR_MAIN_INFO), "")
    # print("d_ITF_TB_EHR_MAIN_INFO => " + str(d_ITF_TB_EHR_MAIN_INFO))

    # 体检信息表
    l_EXAMINATION_idCardNo = Sqlserver_PO_itf.execQuery("SELECT idcardNo  FROM ITF_TB_EXAMINATION_INFO")
    EXAMINATION_idCardNo = random.choice(l_EXAMINATION_idCardNo)
    print("ITF_TB_EXAMINATION_INFO => " + str(EXAMINATION_idCardNo[0]))
    r_ITF_TB_EXAMINATION_INFO = Sqlserver_PO_itf.execQuery("SELECT *  FROM ITF_TB_EXAMINATION_INFO where idCardNo='%s'" % (EXAMINATION_idCardNo[0]))
    l_ITF_TB_EXAMINATION_INFO = list(r_ITF_TB_EXAMINATION_INFO[0])
    l_ITF_TB_EXAMINATION_INFO[3] = (l_ITF_TB_EXAMINATION_INFO[3].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_EXAMINATION_INFO[6] = (l_ITF_TB_EXAMINATION_INFO[6].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_EXAMINATION_INFO[8] = (l_ITF_TB_EXAMINATION_INFO[8].encode('latin-1').decode('gbk'))  # 中文编码转换
    d_ITF_TB_EXAMINATION_INFO = List_PO.lists2dict(Sqlserver_PO_itf.l_getAllField('ITF_TB_EXAMINATION_INFO'), l_ITF_TB_EXAMINATION_INFO)
    Color_PO.consoleColor("31", "33", "d_ITF_TB_EXAMINATION_INFO => " + str(d_ITF_TB_EXAMINATION_INFO), "")
    # print("d_ITF_TB_EXAMINATION_INFO => " + str(d_ITF_TB_EXAMINATION_INFO))

    # 高血压随访表
    l_HTN_idCardNo = Sqlserver_PO_itf.execQuery("select visitIdcardNo from itf_tb_chronic_main t1 INNER JOIN itf_tb_htn_visit t2 on t1.visitNum=t2.visitNum WHERE t1.visitTypeCode='31'")
    HTN_idCardNo = random.choice(l_HTN_idCardNo)
    print("itf_tb_htn_visit => " + str(HTN_idCardNo[0]))
    r_ITF_TB_HTN_VISIT = Sqlserver_PO_itf.execQuery("select * from itf_tb_chronic_main t1 INNER JOIN itf_tb_htn_visit t2 on t1.visitNum=t2.visitNum WHERE t1.idcardNo='%s'" % (HTN_idCardNo[0]))
    l_ITF_TB_HTN_VISIT = list(r_ITF_TB_HTN_VISIT[0])
    l_ITF_TB_HTN_VISIT[3] = (l_ITF_TB_HTN_VISIT[3].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_HTN_VISIT[6] = (l_ITF_TB_HTN_VISIT[6].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_HTN_VISIT[9] = (l_ITF_TB_HTN_VISIT[9].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_HTN_VISIT[12] = (l_ITF_TB_HTN_VISIT[12].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_HTN_VISIT[14] = (l_ITF_TB_HTN_VISIT[14].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_HTN_VISIT[21] = (l_ITF_TB_HTN_VISIT[21].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_HTN_VISIT[23] = (l_ITF_TB_HTN_VISIT[23].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_HTN_VISIT[29] = (l_ITF_TB_HTN_VISIT[29].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_HTN_VISIT[33] = (l_ITF_TB_HTN_VISIT[33].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_HTN_VISIT[36] = (l_ITF_TB_HTN_VISIT[36].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_HTN_VISIT[38] = (l_ITF_TB_HTN_VISIT[38].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_HTN_VISIT[40] = (l_ITF_TB_HTN_VISIT[40].encode('latin-1').decode('gbk'))  # 中文编码转换
    d_ITF_TB_HTN_VISIT = List_PO.lists2dict(Sqlserver_PO_itf.l_getAllField('ITF_TB_HTN_VISIT'), l_ITF_TB_HTN_VISIT)
    Color_PO.consoleColor("31", "33", "d_ITF_TB_HTN_VISIT => " + str(d_ITF_TB_HTN_VISIT), "")
    # print("d_ITF_TB_HTN_VISIT => " + str(d_ITF_TB_HTN_VISIT))

    # 糖尿病随访表
    l_DM_idCardNo = Sqlserver_PO_itf.execQuery("select visitIdcardNo from itf_tb_chronic_main t1 INNER JOIN itf_tb_dm_visit t2 on t1.visitNum=t2.visitNum WHERE t1.visitTypeCode='33'")
    DM_idCardNo = random.choice(l_DM_idCardNo)
    print("itf_tb_dm_visit => " + str(DM_idCardNo[0]))
    r_ITF_TB_DM_VISIT = Sqlserver_PO_itf.execQuery("select * from itf_tb_chronic_main t1 INNER JOIN itf_tb_dm_visit t2 on t1.visitNum=t2.visitNum WHERE t1.idcardNo='%s'" % (DM_idCardNo[0]))
    l_ITF_TB_DM_VISIT = list(r_ITF_TB_DM_VISIT[0])
    l_ITF_TB_DM_VISIT[3] = (l_ITF_TB_DM_VISIT[3].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_DM_VISIT[6] = (l_ITF_TB_DM_VISIT[6].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_DM_VISIT[9] = (l_ITF_TB_DM_VISIT[9].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_DM_VISIT[12] = (l_ITF_TB_DM_VISIT[12].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_DM_VISIT[14] = (l_ITF_TB_DM_VISIT[14].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_DM_VISIT[21] = (l_ITF_TB_DM_VISIT[21].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_DM_VISIT[23] = (l_ITF_TB_DM_VISIT[23].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_DM_VISIT[29] = (l_ITF_TB_DM_VISIT[29].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_DM_VISIT[33] = (l_ITF_TB_DM_VISIT[33].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_DM_VISIT[36] = (l_ITF_TB_DM_VISIT[36].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_DM_VISIT[38] = (l_ITF_TB_DM_VISIT[38].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_ITF_TB_DM_VISIT[40] = (l_ITF_TB_DM_VISIT[40].encode('latin-1').decode('gbk'))  # 中文编码转换
    d_ITF_TB_DM_VISIT= List_PO.lists2dict(Sqlserver_PO_itf.l_getAllField('ITF_TB_DM_VISIT'), l_ITF_TB_DM_VISIT)
    Color_PO.consoleColor("31", "33", "d_ITF_TB_DM_VISIT => " + str(d_ITF_TB_DM_VISIT), "")
    # print("d_ITF_TB_DM_VISIT => " + str(d_ITF_TB_DM_VISIT))


    # dc库
    # 封面表
    r_HrCover = Sqlserver_PO_dc.execQuery("SELECT * FROM HrCover where ArchiveNum='%s'" % (idCardNo))
    l_HrCover = list(r_HrCover[0])
    l_HrCover[3] = (l_HrCover[3].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_HrCover[4] = (l_HrCover[4].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_HrCover[17] = (l_HrCover[17].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_HrCover[4] = str(l_HrCover[4]).strip()
    d_HrCover = List_PO.lists2dict(Sqlserver_PO_dc.l_getAllField('HrCover'), l_HrCover)
    Color_PO.consoleColor("31", "33", "d_HrCover => " + str(d_HrCover), "")
    # print("d_HrCover => " + str(d_HrCover))

    # 基本信息表
    r_HrPersonBasicInfo = Sqlserver_PO_dc.execQuery("SELECT *  FROM HrPersonBasicInfo where ArchiveNum='%s'" % (idCardNo))
    l_HrPersonBasicInfo = list(r_HrPersonBasicInfo[0])
    l_HrPersonBasicInfo[1] = (l_HrPersonBasicInfo[1].encode('latin-1').decode('gbk'))  # 中文编码转换
    d_HrPersonBasicInfo = List_PO.lists2dict(Sqlserver_PO_dc.l_getAllField('HrPersonBasicInfo'), l_HrPersonBasicInfo)
    Color_PO.consoleColor("31", "33", "d_HrPersonBasicInfo => " + str(d_HrPersonBasicInfo), "")
    # print("d_HrPersonBasicInfo => " + str(d_HrPersonBasicInfo))

    # 体检信息表
    r_tb_dc_examination_info = Sqlserver_PO_dc.execQuery("select * from tb_dc_examination_info t1 left join tb_empi_index_root t2 on t1.empiGuid = t2.guid where t2.idcardNo = '%s'" % (EXAMINATION_idCardNo[0]))
    l_tb_dc_examination_info = list(r_tb_dc_examination_info[0])
    d_tb_dc_examination_info = List_PO.lists2dict(Sqlserver_PO_dc.l_getAllField('tb_dc_examination_info'), l_tb_dc_examination_info)
    Color_PO.consoleColor("31", "33", "d_tb_dc_examination_info => " + str(d_tb_dc_examination_info), "")
    # print("d_tb_dc_examination_info => " + str(d_tb_dc_examination_info))

    # 高血压随访表
    r_tb_dc_htn_visit = Sqlserver_PO_dc.execQuery("SELECT  * FROM tb_dc_htn_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % (HTN_idCardNo[0]))
    l_tb_dc_htn_visit = list(r_tb_dc_htn_visit[0])
    l_tb_dc_htn_visit[2] = (l_tb_dc_htn_visit[2].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_tb_dc_htn_visit[7] = (l_tb_dc_htn_visit[7].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_tb_dc_htn_visit[10] = (l_tb_dc_htn_visit[10].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_tb_dc_htn_visit[12] = (l_tb_dc_htn_visit[12].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_tb_dc_htn_visit[14] = (l_tb_dc_htn_visit[14].encode('latin-1').decode('gbk'))  # 中文编码转换
    d_tb_dc_htn_visit = List_PO.lists2dict(Sqlserver_PO_dc.l_getAllField('tb_dc_htn_visit'), l_tb_dc_htn_visit)
    Color_PO.consoleColor("31", "33", "d_tb_dc_htn_visit => " + str(d_tb_dc_htn_visit), "")
    # print("d_tb_dc_htn_visit => " + str(d_tb_dc_htn_visit))

    # 糖尿病随访表
    r_tb_dc_dm_visit = Sqlserver_PO_dc.execQuery("SELECT  * FROM tb_dc_dm_visit AS dm INNER JOIN tb_dc_chronic_main AS cMain ON dm.OrgCode = cMain.orgCode AND dm.cardId = cMain.visitNum INNER JOIN tb_dc_chronic_info AS cInfo ON cInfo.orgCode = cMain.orgCode AND cInfo.manageNum = cMain.manageNum INNER JOIN tb_empi_index_root AS empi ON cInfo.empiGuid = empi.guid WHERE empi.idCardNo='%s'" % (DM_idCardNo[0]))
    l_tb_dc_dm_visit = list(r_tb_dc_dm_visit[0])
    l_tb_dc_dm_visit[2] = (l_tb_dc_dm_visit[2].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_tb_dc_dm_visit[7] = (l_tb_dc_dm_visit[7].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_tb_dc_dm_visit[10] = (l_tb_dc_dm_visit[10].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_tb_dc_dm_visit[12] = (l_tb_dc_dm_visit[12].encode('latin-1').decode('gbk'))  # 中文编码转换
    l_tb_dc_dm_visit[14] = (l_tb_dc_dm_visit[14].encode('latin-1').decode('gbk'))  # 中文编码转换
    d_tb_dc_dm_visit = List_PO.lists2dict(Sqlserver_PO_dc.l_getAllField('tb_dc_dm_visit'), l_tb_dc_dm_visit)
    Color_PO.consoleColor("31", "33", "d_tb_dc_dm_visit => " + str(d_tb_dc_dm_visit), "")
    # print("d_tb_dc_dm_visit => " + str(d_tb_dc_dm_visit))


    # 执行比对
    l_all = Openpyxl_PO.l_getRowData()
    c = 0
    left = ""
    right = ""
    for k in range(len(l_all)):
        if l_all[k][2] == "核对结果":
            c = c + 1
        else:
            # itf库
            if str(l_all[k][0]).split(".")[0] == "ITF_TB_EHR_MAIN_INFO":
                left = (d_ITF_TB_EHR_MAIN_INFO[str(l_all[k][0]).split(".")[1]])
            if str(l_all[k][0]).split(".")[0] == "ITF_TB_EXAMINATION_INFO":
                left = (d_ITF_TB_EXAMINATION_INFO[str(l_all[k][1]).split(".")[1]])
            if str(l_all[k][0]).split(".")[0] == "ITF_TB_HTN_VISIT":
                left = (d_ITF_TB_HTN_VISIT[str(l_all[k][1]).split(".")[1]])
            if str(l_all[k][0]).split(".")[0] == "ITF_TB_DM_VISIT":
                left = (d_ITF_TB_DM_VISIT[str(l_all[k][1]).split(".")[1]])
            # dc库
            if str(l_all[k][1]).split(".")[0] == "HrCover":
                right = (d_HrCover[str(l_all[k][1]).split(".")[1]])
            if str(l_all[k][1]).split(".")[0] == "HrPersonBasicInfo":
                right = (d_HrPersonBasicInfo[str(l_all[k][1]).split(".")[1]])
            if str(l_all[k][1]).split(".")[0] == "tb_dc_examination_info":
                right = (d_tb_dc_examination_info[str(l_all[k][1]).split(".")[1]])
            if str(l_all[k][1]).split(".")[0] == "tb_dc_htn_visit":
                right = (d_tb_dc_htn_visit[str(l_all[k][1]).split(".")[1]])
            if str(l_all[k][1]).split(".")[0] == "tb_dc_dm_visit":
                right = (d_tb_dc_dm_visit[str(l_all[k][1]).split(".")[1]])

            if left == right:
                if Openpyxl_PO.getCellValue(c + 1, 4) == None:
                    Openpyxl_PO.setCellValue(c + 1, 3, "ok", ['ffffff', '000000'])
                else:
                    Openpyxl_PO.setCellValue(c + 1, 3, "error", ['ffeb9c', '000000'])
            else:
                Openpyxl_PO.setCellValue(c + 1, 3, "error", ['ffeb9c', '000000'])
                x = Openpyxl_PO.getCellValue(c + 1, 4)
                if x == None :
                    Openpyxl_PO.setCellValue(c + 1, 4, str(idCardNo) + " , " + str(left) + " <> " + str(right), ['ffffff', '000000'])
                else:
                    x = str(x) + "\n" + str(idCardNo) + " , " + str(left) + " <> " + str(right)
                    Openpyxl_PO.setCellValue(c + 1, 4, x, ['ffffff', '000000'])

                # 控制台只输出错误结果：
                print(str(k+1) + "行，" + str(l_all[k][0]) + "(" + str(left) + ") <> " + str(l_all[k][1]) + "(" + str(right) + ")")
                # 如 ：357行，ITF_TB_DM_VISIT.targetOrgName(窦*青) <> tb_dc_dm_visit.targetOrgName(None)

            c = c + 1
            Openpyxl_PO.save()
    print("\n")

# # 将结果保存到git
# currDate = Time_PO.getDate()
# currDate = "EHR_" + str(currDate) + ".xlsx"
# os.system('copy EHR.xlsx D:\\myGit\\testTeam\\EHR\\自动化\\comparison\\' + currDate + '&& cd D:\\myGit\\testTeam\ && git add . && git commit -m "add result" && git push')
#
