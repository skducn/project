# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2021-8-26
# Description: 电子健康档案数据比对自动化，ITF与DC库中表字段数据比对。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from PO.OpenpyxlPO import *
from PO.SqlserverPO import *
from PO.DataPO import *
from time import sleep


# 初始化数据
Openpyxl_PO = OpenpyxlPO("data.xlsx")
Openpyxl_PO.clsColData(4, "test")
Sqlserver_PO_itf = SqlServerPO("192.168.0.234", "sa", "Zy@123456", "EHRITF")
Sqlserver_PO_dc = SqlServerPO("192.168.0.234", "sa", "Zy@123456", "EHRDC")
varRandomIdCard = 15  # 随机获取N条身份证


#1， 随机从 ITF_TB_EHR_MAIN_INFO 库获取 N 条身份证
r_itf_ITF_TB_EHR_MAIN_INFO_icCardNo = Sqlserver_PO_itf.ExecQuery("SELECT idCardNo  FROM ITF_TB_EHR_MAIN_INFO")
suiji = random.sample(range(1, len(r_itf_ITF_TB_EHR_MAIN_INFO_icCardNo)), varRandomIdCard)
suiji.sort()
for i in range(len(r_itf_ITF_TB_EHR_MAIN_INFO_icCardNo)):
    for j in range(len(suiji)):
        if suiji[j] == i :
            idCardNo = (r_itf_ITF_TB_EHR_MAIN_INFO_icCardNo[i][0])
            # print(str(j+1) + "), " + str(idCardNo))

            r_itf_ITF_TB_EHR_MAIN_INFO = Sqlserver_PO_itf.ExecQuery("SELECT *  FROM ITF_TB_EHR_MAIN_INFO where idCardNo='%s'" % (idCardNo))
            # print(r_itf_ITF_TB_EHR_MAIN_INFO)

            # convert(nvarchar(20), Name) 乱码
            # convert(nvarchar(20), ArchiveUnit) 乱码
            r_dc_HrCover = Sqlserver_PO_dc.ExecQuery("SELECT * FROM HrCover where ArchiveNum='%s'" % (idCardNo))
            # print(r_dc_HrCover)

            r_dc_HrPersonBasicInfo = Sqlserver_PO_dc.ExecQuery("SELECT *  FROM HrPersonBasicInfo where ArchiveNum='%s'" % (idCardNo))
            # print(r_dc_HrPersonBasicInfo)


            # ITF_TB_EHR_MAIN_INFO 字段名
            l_itf_fieldName = Sqlserver_PO_itf.getAllFields('ITF_TB_EHR_MAIN_INFO')
            l_itf_fieldName.insert(0, 1)
            Openpyxl_PO.setMoreCellValue([l_itf_fieldName], "ITF_TB_EHR_MAIN_INFO")
            # ITF_TB_EHR_MAIN_INFO 值
            Openpyxl_PO.delRowData(2, 1, "ITF_TB_EHR_MAIN_INFO")
            l_itf_ITF_TB_EHR_MAIN_INFO = list(r_itf_ITF_TB_EHR_MAIN_INFO[0])
            l_itf_ITF_TB_EHR_MAIN_INFO.insert(0, 2)
            Openpyxl_PO.setMoreCellValue([l_itf_ITF_TB_EHR_MAIN_INFO], "ITF_TB_EHR_MAIN_INFO")


            # HrCover 字段名
            l_dc_HrCover_fieldName = Sqlserver_PO_dc.getAllFields('HrCover')
            l_dc_HrCover_fieldName.insert(0, 1)
            Openpyxl_PO.setMoreCellValue([l_dc_HrCover_fieldName], "HrCover")
            # HrCover 值
            Openpyxl_PO.delRowData(2, 1, "HrCover")
            l_dc_HrCover = list(r_dc_HrCover[0])
            l_dc_HrCover.insert(0, 2)
            l_dc_HrCover[4] = (l_dc_HrCover[4].encode('latin-1').decode('gbk'))
            l_dc_HrCover[18] = (l_dc_HrCover[18].encode('latin-1').decode('gbk'))
            Openpyxl_PO.setMoreCellValue([l_dc_HrCover], "HrCover")


            # HrPersonBasicInfo 字段名
            l_dc_HrPersonBasicInfo_fieldName = Sqlserver_PO_dc.getAllFields('HrPersonBasicInfo')
            l_dc_HrPersonBasicInfo_fieldName.insert(0, 1)
            Openpyxl_PO.setMoreCellValue([l_dc_HrPersonBasicInfo_fieldName], "HrPersonBasicInfo")
            # HrPersonBasicInfo 值
            Openpyxl_PO.delRowData(2, 1, "HrPersonBasicInfo")
            l_dc_HrPersonBasicInfo = list(r_dc_HrPersonBasicInfo[0])
            l_dc_HrPersonBasicInfo.insert(0, 2)
            l_dc_HrPersonBasicInfo[2] = (l_dc_HrPersonBasicInfo[2].encode('latin-1').decode('gbk'))
            Openpyxl_PO.setMoreCellValue([l_dc_HrPersonBasicInfo], "HrPersonBasicInfo")

            Openpyxl_PO.save()


            # 2，读取excel数据转换字典
            l_itf = (Openpyxl_PO.l_getRowData("ITF_TB_EHR_MAIN_INFO"))
            d_itf = {}
            for i in range(len(l_itf[0])):
                d_itf[l_itf[0][i]] = l_itf[1][i]
            # print(d_itf)

            l_dcfeng = (Openpyxl_PO.l_getRowData("HrCover"))
            # print(l_dcfeng)
            d_dcfeng = {}
            for i in range(len(l_dcfeng[0])):
                d_dcfeng[l_dcfeng[0][i]] = l_dcfeng[1][i]
            # print(d_dcfeng)

            l_dcjiben = (Openpyxl_PO.l_getRowData("HrPersonBasicInfo"))
            # print(l_dcjiben)
            d_dcjiben = {}
            for i in range(len(l_dcjiben[0])):
                d_dcjiben[l_dcjiben[0][i]] = l_dcjiben[1][i]
            # print(d_dcjiben)


            # 3，执行比对
            l_all = Openpyxl_PO.l_getRowData("test")
            c = 0
            for i in range(len(l_all)):
                # if l_all[i][2] == "比对结果" or l_all[i][2] == "error":
                if l_all[i][2] == "比对结果" :
                    c = c + 1
                else:
                    if str(l_all[i][0]).split(".")[0] == "ITF_TB_EHR_MAIN_INFO":
                        left = (d_itf[str(l_all[i][0]).split(".")[1]])
                    if str(l_all[i][1]).split(".")[0] == "HrCover":
                        right = (d_dcfeng[str(l_all[i][1]).split(".")[1]])
                    if str(l_all[i][1]).split(".")[0] == "HrPersonBasicInfo":
                        right = (d_dcjiben[str(l_all[i][1]).split(".")[1]])
                    if left == right or (left == "" and right == None) :
                        if Openpyxl_PO.getCellValue(c + 1, 4) == None:
                            Openpyxl_PO.setCellValue(c + 1, 3, "ok", "test")
                        else:
                            Openpyxl_PO.setCellValue(c + 1, 3, "error", "test")
                    else:
                        Openpyxl_PO.setCellValue(c + 1, 3, "error", "test")
                        x = Openpyxl_PO.getCellValue(c + 1, 4)
                        if x == None :
                            Openpyxl_PO.setCellValue(c + 1, 4, str(idCardNo) + " , " + str(left) + " <> " + str(right), "test")
                        else:
                            x = str(x) + "\n" + str(idCardNo) + " , " + str(left) + " <> " + str(right)
                            Openpyxl_PO.setCellValue(c + 1, 4, x, "test")

                        # 控制台只输出错误结果：
                        print(str(j + 1) + ", " + str(idCardNo) + " , " + str(l_all[i][0]).split(".")[0] + "." + str(l_all[i][0]).split(".")[1] + "(" + str(left) + ") <> "
                              + str(l_all[i][1]).split(".")[0] + "." + str(l_all[i][1]).split(".")[1] + "(" + str(right) + ")")
                    c = c + 1
                    Openpyxl_PO.save()

