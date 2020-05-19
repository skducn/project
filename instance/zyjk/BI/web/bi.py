# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-4-8
# Description: BI集成平台自动化脚本 by pycharm（打印结果，输出日志到log）
# *****************************************************************
# from time import sleep
# sleep(1212)

from instance.zyjk.BI.PageObject.BiPO import *
Bi_PO = BiPO()
List_PO = ListPO()
Time_PO = TimePO()
Net_PO = NetPO()
Data_PO = DataPO()
File_PO = FilePO()
Excel_PO = ExcelPO()


# 登录 运营决策系统
Bi_PO.login()

# 获取当前数据更新时间
varDataUpdateDate = Bi_PO.Web_PO.getXpathText('//*[@id="app"]/section/section/section/main/div[1]/span')
Bi_PO.Log_PO.logger.info(varDataUpdateDate)
varUpdateDate = str(varDataUpdateDate).split("数据更新时间：")[1].split(" ")[0]


# ===============================================================================================
# Bi_PO.menu1("1", "实时监控指标")
# varUpdateDate = str(varDataUpdateDate).split("数据更新时间：")[1].split(" ")[0]
# Bi_PO.menu2ByHref("1.1", "今日运营分析", "/bi/realTimeMonitoringIndicator/todayOperationalAnalysis")
# Bi_PO.monitor("1.1.1", "医疗业务收入(万元)", 'SELECT round((select (a.sum+b.sum)/10000 from(SELECT IFNULL(sum(inPAccount),0) sum  from bi_inpatient_yard where statisticsDate ="%s")a,(SELECT IFNULL(sum(outPAccount),0) sum FROM bi_outpatient_yard WHERE statisticsDate ="%s")b),2)', varUpdateDate, varUpdateDate)
# Bi_PO.monitor("1.1.2", "药品收入(万元)", 'select round((select (a.sum +b.sum)/10000 from(SELECT ifnull(sum(outPMedicateAccount),0) sum  from bi_outpatient_yard where statisticsDate ="%s")a,(SELECT IFNULL(sum(inPMedicateAccount),0) sum FROM bi_inpatient_yard WHERE statisticsDate ="%s")b),2)', varUpdateDate, varUpdateDate)
# Bi_PO.monitor("1.1.3", "今日门急诊量(例)", 'select ifnull(sum(outPCount),0) from bi_outpatient_yard where statisticsDate ="%s" ', varUpdateDate)
# Bi_PO.monitor("1.1.4", "今日门诊量(例)", 'select ifnull(sum(outpatientCount),0) from bi_outpatient_yard where statisticsDate ="%s" ', varUpdateDate)
# Bi_PO.monitor("1.1.5", "今日急诊量(例)", 'select sum(emergencyCount) from bi_outpatient_yard where statisticsDate ="%s" ', varUpdateDate)
# Bi_PO.monitor("1.1.6", "今日门急诊收入(万元)", 'select round(sum(outpaccount)/10000,2) from bi_outpatient_yard where statisticsDate ="%s" ', varUpdateDate)
# Bi_PO.monitor("1.1.7", "今日出院人数(例)", 'select sum(leaveCount) from bi_inpatient_yard where statisticsDate ="%s" ', varUpdateDate)
# Bi_PO.monitor("1.1.8", "今日在院(例)", 'select sum(inPCount) from bi_inpatient_yard where statisticsDate ="%s" ', varUpdateDate)
# Bi_PO.monitor("1.1.9", "当前危重人数(例)", 'select sum(criticalCount) from bi_inpatient_yard where statisticsDate ="%s" ', varUpdateDate)
# Bi_PO.monitor("1.1.10", "今日住院实收入(万元)", 'select round(sum(inPAccount)/10000,2) from bi_inpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# # 2，当前住院欠费明细
# print(Bi_PO.getContent("//tr"))
# Bi_PO.menu1Close("实时监控指标")


# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# print("\n[1.2 门急诊动态监测]" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/realTimeMonitoringIndicator/oaedDynamicMonitoring", varUpdateDate)
#
# # 1，各科室普通门诊业务量
# print(Bi_PO.winByDiv("各科室普通门诊业务量\n", "普通门诊医生接诊人次", "急诊内科"))  # 获取 急诊内科的值
#
# # 2，普通门诊医生接诊人次
# print(Bi_PO.winByDiv("普通门诊医生接诊人次\n", "今日专家门诊业务量", "张**"))  # 获取 张**的值
#
# # 3，门诊使用前十药品排名
# print(Bi_PO.winByDiv("门诊使用前十药品排名\n", "今日门急诊业务量按时间段分布", "[甲]注射用头孢呋辛钠"))  # 获取 [甲]注射用头孢呋辛钠的值
# Bi_PO.winByDiv("门诊使用前十药品排名\n", "今日门急诊业务量按时间段分布", "")  # 获取 门诊使用前十药品排名 列表清单


# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# print("\n1.3 住院动态监测" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/realTimeMonitoringIndicator/dynamicMonitoringInHospital", vatUpdateDate)
#
# tmpList = Bi_PO.getContent("//div")
# # 1，今日床位使用情况-按空床率排序
# tmpStr1 = tmpList[0].split("今日床位使用情况-按空床率排序 ")[1].split("今日在院病人按住院天数分布")[0]
# tmpList1 = list(tmpStr1)
# tmpList1.insert(tmpList1.index('在'), '\n')
# tmpList1 = "".join(tmpList1).split("\n")
# tmpList1.pop()
# print(tmpList1)
#
# # 2，今日各病区出入院人数情况
# tmpStr2 = tmpList[0].split("今日各病区出入院人数情况 ")[1].split(",")[0]
# tmpList2 = list(tmpStr2)
# tmpList2.insert(tmpList2.index('当'), '\n')
# tmpList2 = "".join(tmpList2).split("\n")
# print(tmpList2)


# # #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# print("\n[1.4 医技动态监测]" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/realTimeMonitoringIndicator/operationTrend",vatUpdateDate)
#
# # 1，遍历并分成多个列表（今日检验项目数，今日检验总费用，今日检查项目数，今日检查总费用）
# Bi_PO.winByP()
# a, b, c = Bi_PO.winByP("今日检查项目数")
# print(a, b, c)


# ===============================================================================================

excelFile = File_PO.getLayerPath("../config") + "\\bi.xlsx"
row, col = Excel_PO.getRowCol(excelFile, "bi")
recordList = []

# for i in range(2, 13):
for i in range(2, row+1):
    recordList = Excel_PO.getRowValue(excelFile, i, "bi")

    if recordList[2] != "":  # 一级编号
        Bi_PO.menu1(str(recordList[2]), recordList[3])

    if "1.1." in str(recordList[7]) and recordList[4] != "":  # 二级编号
        Bi_PO.menu2ByHref(str(recordList[4]), recordList[5], recordList[6])
    elif recordList[4] != "":
        Bi_PO.menu2ByHref(str(recordList[4]), recordList[5], recordList[6], recordList[10])
    # else:
    #     print("[ERROR], " + sys._getframe().f_code.co_filename + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe().f_code.co_name)

    if "1.1." in str(recordList[7]) :  # 将当前数据更新时间写入统计日期
        tmpList = Excel_PO.getRowValue(excelFile, i, "bi")
        x = tmpList[9].count("%")
        # print(x)
        if x == 2:
            Excel_PO.writeXlsx(excelFile, "bi", i, 11, str(varUpdateDate)+"," + str(varUpdateDate))
        else:
            Excel_PO.writeXlsx(excelFile, "bi", i, 11, str(varUpdateDate))
        recordList = Excel_PO.getRowValue(excelFile, i, "bi")
        # print(recordList)
        result, info = Bi_PO.monitor(str(recordList[7]), recordList[8], recordList[9], recordList[10])
        Excel_PO.writeXlsx(excelFile, "bi", i, 1, result)
        Excel_PO.writeXlsx(excelFile, "bi", i, 2, info)

    elif "1.1." not in str(recordList[7]) and recordList[10] != "":  # 统计日期
        result, info = Bi_PO.currentValue(str(recordList[7]), recordList[8], recordList[9], recordList[10])
        Excel_PO.writeXlsx(excelFile, "bi", i, 1, result)
        Excel_PO.writeXlsx(excelFile, "bi", i, 2, info)
    elif recordList[11] != "":  # 统计前一日
        Bi_PO.currentValue(str(recordList[7]), recordList[8], recordList[9], recordList[11])
    elif recordList[12] != "":  # 同期
        result, info = Bi_PO.tongqi(str(recordList[7]), recordList[8], recordList[9], recordList[12])
        Excel_PO.writeXlsx(excelFile, "bi", i, 1, result)
        Excel_PO.writeXlsx(excelFile, "bi", i, 2, info)
    elif recordList[13] != "":   # 同比
        result, info = Bi_PO.tongbi(str(recordList[7]), recordList[8], recordList[9], recordList[13])
        Excel_PO.writeXlsx(excelFile, "bi", i, 1, result)
        Excel_PO.writeXlsx(excelFile, "bi", i, 2, info)
    elif recordList[14] != "":   # top10
        result, info = Bi_PO.top10(str(recordList[7]), "0", recordList[8], recordList[9], recordList[14])
        Excel_PO.writeXlsx(excelFile, "bi", i, 1, result)
        Excel_PO.writeXlsx(excelFile, "bi", i, 2, info)
    elif recordList[15] != "":   # 处方率
        result, info = Bi_PO.prescriptionRate(str(recordList[7]), recordList[8], recordList[9], recordList[15])
        Excel_PO.writeXlsx(excelFile, "bi", i, 1, result)
        Excel_PO.writeXlsx(excelFile, "bi", i, 2, info)
    elif recordList[16] != "":   # top10right
        result, info = Bi_PO.top10right(str(recordList[7]), "0.00", recordList[8], recordList[9], recordList[16])
        Excel_PO.writeXlsx(excelFile, "bi", i, 1, result)
        Excel_PO.writeXlsx(excelFile, "bi", i, 2, info)

    recordList = []


print("end")
sleep(1212)
#
# Bi_PO.menu1("2", "门诊分析")
# sleep(2)

# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# varUpdateDate = "2020-03-22"
# Bi_PO.menu2ByHref("2.2 门诊预约", "/bi/outpatientAnalysis/outpatientAppointment",varUpdateDate)
#
#
# # 1，遍历并分成多个列表（门诊预约人次，院内窗口预约）
# # 门诊预约人次 = 统计期内门诊预约人次和
# SELECT sum(subscribeCount) from bi_outpatient_yard where statisticsDate ='2019-09-15'
#
# # 院内窗口预约人次=统计期使用院内自助机预约和窗口预约人次和
# SELECT sum(windowSubscribeCount) from bi_outpatient_yard where statisticsDate ='2019-09-15'

# # 2，门诊预约率
# reserveList = []
# tmpList2 = Bi_PO.getContent("//div")
# reserveList.append("门诊预约率")
# reserveList.append(tmpList2[0].split("门急预约人次月趋势\n")[1].split("\n门诊预约率")[0])
# print(List_PO.listBorderDict(reserveList))


# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Bi_PO.menu1("2", "门诊分析")
#
# varUpdateDate = "2020-03-22"
# Bi_PO.menu2ByHref("2.4","门诊收入", "/bi/outpatientAnalysis/outpatientIncome", varUpdateDate)
#
# tmpList = Bi_PO.getContent(u"//div[@class='el-card__header']")
#
# # tmpList = Bi_PO.getContent(u"//div[contains(@class,'el-card__body')]")
# print(tmpList)
#
# # print("__________________________")
# # tmpList = Bi_PO.getContent(u"//div")
# # print(tmpList)
# print("end")
# sleep(1212)
# Bi_PO.winByDiv("门急诊收入科室排名\n", "门急诊均次费月趋势")

# # 这里有问题？
# Bi_PO.top10("2.4.8", "0", Bi_PO.winByDiv("门急诊收入科室排名\n", "门急诊均次费月趋势"), "门急诊收入科室排名", 'SELECT deptname,round(outPAccount,2) from bi_outpatient_dept where statisticsDate ="%s" GROUP BY deptname ORDER BY outpaccount DESC LIMIT 10', varUpdateDate)
#
# # 2.4.9 门急诊医疗收入构成分析
# Bi_PO.Color_PO.consoleColor("31", "33", "[warning], 2.4.9 门急诊医疗收入构成分析, 未提供sql", "")
# Bi_PO.Log_PO.logger.warning("2.4.9 门急诊医疗收入构成分析, 未提供sql")
# top10Dict249 = Bi_PO.winByDiv("门急诊医疗收入构成分析\n", "")
#
# Bi_PO.menu1Close("门诊分析")


# ===============================================================================================
Bi_PO.menu1("3", "住院分析")
varUpdateDate = "2020-03-22"
# Bi_PO.menu2ByHref("3.1","住院业务", "/bi/hospitalizationAnnlysis/inpatientService", varUpdateDate)



# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
varUpdateDate = "2020-03-22"
Bi_PO.menu2ByHref("3.2 床位分析", "/bi/hospitalizationAnnlysis/bedAnalysis", varUpdateDate)


# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
varUpdateDate = "2020-03-22"
Bi_PO.menu2ByHref("3.3 住院收入", "/bi/hospitalizationAnnlysis/hospitalizationIncome", varUpdateDate)

Bi_PO.menu1Close("住院分析")


# ===============================================================================================
Bi_PO.menu1("4", "药品分析")
varUpdateDate = "2020-03-22"
Bi_PO.menu2ByHref("4.1 基本用药分析", "/bi/medicationAnalysis/essentialDrugsMedicare", varUpdateDate)

# # 2，门急诊收入科室排名
# Bi_PO.winByDiv("药占比科室情况\n", "各类药品收入月趋势", "")
#
# # 3，药品用量分析
# Bi_PO.winByDiv("药品用量分析\n", "", "")


# # #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
varUpdateDate = "2020-03-22"
Bi_PO.menu2ByHref("4.2 抗菌药物用药分析", "/bi/medicationAnalysis/antimicrobialAgent", varUpdateDate)
Bi_PO.currentValue("4.2.1", "抗菌药物药占比", 'SELECT b.sum/a.sum from (SELECT sum(pmcost+wmcost+hmcost) sum FROM bi_hospital_drugcosts_day WHERE statisticsDate ="%s")a,(select sum(antibacterialCost) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type in(1,3))b',varUpdateDate,varUpdateDate)
Bi_PO.currentValue("4.2.2", "门急诊抗菌药物均次费(元)", 'SELECT ifnull(round((SELECT b.sum/a.sum from (SELECT sum(antibacterialPeople) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type in (1,2))a,(SELECT sum(antibacterialCost) sum  from bi_hospital_drugcosts_day WHERE statisticsDate ="%s")b),2),0)',varUpdateDate,varUpdateDate)
Bi_PO.currentValue("4.2.3", "门诊患者抗菌药物使用率", 'SELECT round((SELECT b.sum/a.sum from((SELECT sum(outpatientCount) sum from bi_outpatient_yard WHERE statisticsDate ="%s")a,(SELECT sum(antibacterialPeople) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=1)b)),2)',varUpdateDate,varUpdateDate)
Bi_PO.currentValue("4.2.4", "急诊患者抗菌药物使用率", 'SELECT b.sum/a.sum from((SELECT sum(emergencyCount) sum from bi_outpatient_yard WHERE statisticsDate ="%s")a,(SELECT sum(antibacterialPeople) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=2)b)',varUpdateDate,varUpdateDate)
Bi_PO.currentValue("4.2.5", "住院患者抗菌药物使用率", 'SELECT round((SELECT b.sum/a.sum from((SELECT sum(inpCount) sum from bi_inpatient_yard WHERE statisticsDate ="%s")a,(SELECT sum(antibacterialPeople) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=3)b)),2)',varUpdateDate,varUpdateDate)

# 4.2.6 Ⅰ类切口手术患者预防使用抗菌药物使用率
Bi_PO.Color_PO.consoleColor("31", "33", "[warning], 4.2.6 Ⅰ类切口手术患者预防使用抗菌药物使用率, 未提供SQL", "")
Bi_PO.Log_PO.logger.warning("4.2.6 Ⅰ类切口手术患者预防使用抗菌药物使用率, 未提供SQL")


# # #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
varUpdateDate = "2020-03-22"
Bi_PO.menu2ByHref("4.3 注射输液用药分析", "/bi/medicationAnalysis/injectionMedication", varUpdateDate)
Bi_PO.currentValue("4.3.1", "门急诊使用注射药物的百分比", 'SELECT round((SELECT a.sum/b.sum from (SELECT sum(injection+vein) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type in(1,2))a,(SELECT sum(outPCount) sum from bi_outpatient_yard where statisticsDate ="%s")b),2)', varUpdateDate, varUpdateDate)
Bi_PO.currentValue("4.3.2", "门诊患者静脉输液使用率", 'SELECT round((SELECT a.sum/b.sum*100 from(SELECT sum(vein) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=1)a,(SELECT sum(outpatientCount) sum from bi_outpatient_yard where statisticsDate ="%s")b),2)' ,varUpdateDate, varUpdateDate)
Bi_PO.currentValue("4.3.3", "住院患者抗菌药物使用率", 'SELECT round((SELECT b.sum/a.sum from((SELECT sum(inpCount) sum from bi_inpatient_yard WHERE statisticsDate ="%s")a,(SELECT sum(antibacterialPeople) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=3)b)),2)', varUpdateDate, varUpdateDate)
Bi_PO.currentValue("4.3.4", "住院患者静脉输液平均每床日使用袋（瓶）数", 'SELECT ifnull(round((SELECT  a.sum/b.sum from (SELECT sum(arrAntibacterialVeinNumber) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=3)a,(select sum(realBedCount) sum  from bi_inpatient_yard_bed  where statisticsDate ="%s")b),2),0)', varUpdateDate, varUpdateDate)
Bi_PO.currentValue("4.3.5", "住院患者抗菌药物静脉输液占比", 'SELECT a.sum/b.sum from(SELECT sum(vein) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=3)a,(SELECT sum(arrAntibacterialVein) sum from bi_hospital_drugcosts_day where statisticsDate ="%s")b', varUpdateDate, varUpdateDate)
Bi_PO.currentValue("4.3.6", "急诊患者静脉输液使用率", 'SELECT ifnull(round((SELECT a.sum/b.sum from(SELECT sum(vein) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=2)a,(SELECT sum(emergencyCount) sum from bi_outpatient_yard where statisticsDate ="%s")b),2),0)', varUpdateDate, varUpdateDate)


# ===============================================================================================
Bi_PO.menu1("5", "手术分析")
varUpdateDate = "2019-09-09"
Bi_PO.menu2ByHref("5.1 手术分析", "/bi/operativeAnalysisTip/operativeAnalysis", varUpdateDate)
Bi_PO.currentValue("5.1.1", "住院手术例数(例)", 'SELECT count(id) 手术例数 from book_operation WHERE bookingDate = "%s" and surgicalType = 2', varUpdateDate)
Bi_PO.currentValue("5.1.2", "住院患者手术人次数(人次)", 'SELECT count(*) from (SELECT patientId from book_operation WHERE bookingDate = "%s" and surgicalType = 2 GROUP BY patientId)as a ', varUpdateDate)
Bi_PO.currentValue("5.1.3", "日间手术例数(例)", 'SELECT count(id) from book_operation WHERE bookingDate = "%s" and surgicalType = 3', varUpdateDate)
Bi_PO.currentValue("5.1.4", "日间手术人次数(人次)", 'SELECT count(*) from (SELECT patientId from book_operation WHERE bookingDate BETWEEN "%s" AND surgicalType = 3 GROUP BY patientId) as a', varUpdateDate)
Bi_PO.currentValue("5.1.5", "三四级手术占比(例)", 'SELECT round(sum(threeLevelSurgical+fourLevelSurgical)/sum(oneLevelSurgical+twoLevelSurgical+threeLevelSurgical+fourLevelSurgical)*100,2) from bi_patient_surgical_hospital WHERE surgicalDate = "%s"', varUpdateDate)
Bi_PO.currentValue("5.1.6", "麻醉总例数(例)", 'SELECT sum(anaesthesiaNum) from bi_anaesthesia_hostipal WHERE anaesthesiaDate = "%s"', varUpdateDate)
Bi_PO.top10("5.1.7", "0", Bi_PO.winByDiv("手术例数科室分析\n", "\n手术主刀医生排名"), "手术例数科室分析", 'SELECT deptName,sum(oneLevelSurgical+twoLevelSurgical+threeLevelSurgical+fourLevelSurgical) as number from bi_patient_surgical_dept WHERE surgicalDate = "%s" GROUP BY deptname ORDER BY number  DESC LIMIT 10', varUpdateDate)
Bi_PO.top10("5.1.8", "0", Bi_PO.winByDiv("手术主刀医生排名\n", "\n手术排名", ""), "手术主刀医生排名", 'SELECT doctorName,sum(oneLevelSurgical+twoLevelSurgical+threeLevelSurgical+fourLevelSurgical) as number from bi_patient_surgical_doctor WHERE surgicalDate = "%s" GROUP BY doctorName ORDER BY number DESC LIMIT 10', varUpdateDate)
Bi_PO.top10("5.1.9", "0", Bi_PO.winByDiv("手术排名\n", "", ""), "手术排名", 'SELECT surgicalName,sum(surgicalNum) from bi_surgical_name_hospital WHERE surgicalLevel in (1,2,3,4) and surgicalDate = "%s" GROUP BY surgicalName ORDER BY sum(surgicalNum) DESC LIMIT 10', varUpdateDate)



# # # ===============================================================================================
# #
# Bi_PO.menu1("医保分析")
# #
# print("\n6.1 住院医保" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/medicalInsuranceAnalysis/hospitalizationInsurance", varUpdateDate)
#
# # # 1，遍历并分成多个列表（住院医保患者人次，住院医保患者总费用，住院医保患者均次费，住院医保支付金额，住院医保患者药占比，住院医保患者自费占比）
# Bi_PO.winByP()
#
# # # 2，门急诊收入科室排名
# Bi_PO.winByDiv("各科室住院医保患者均次费分析\n", "", "")
#

# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# # 门急诊医保
# Bi_PO.menu2ByHref("/bi/medicalInsuranceAnalysis/outpatientEmergeInsurance", varUpdateDate)
#
# # ===============================================================================================
#
# Bi_PO.l("医技分析")
#
# # 检验分析
# Bi_PO.menu2ByHref("/bi/medicalTechnologyAnalysis/InspectionAnalysis", varUpdateDate)
#
# # 检查分析
# Bi_PO.menu2ByHref("/bi/medicalTechnologyAnalysis/ExamineAnalysis", varUpdateDate)
#
# # ===============================================================================================
#
# Bi_PO.menu1("医疗质量")
#
# # 治疗质量
# Bi_PO.menu2ByHref("/bi/medicalQuality/treatmentQuality", varUpdateDate)
#
# # 诊断质量
# Bi_PO.menu2ByHref("/bi/medicalQuality/diagnosticQuality", varUpdateDate)


# # ===============================================================================================
print("\n")
print(" 测试完毕 ".center(100, "-"))
varINFO = Data_PO.getNumByText(os.getcwd() + logFile, "INFO")
varERROR = Data_PO.getNumByText(os.getcwd() + logFile, "ERROR")
varWARNING = Data_PO.getNumByText(os.getcwd() + logFile, "WARNING")
email_subject = email_subject + "ERROR(" + str(varERROR) + "),INFO(" + str(varINFO) + "),WARNING(" + str(varWARNING) + ")"
Net_PO.sendEmail(email_nickNameByFrom, email_sender, email_receiver, email_subject, email_content, email_attachment)