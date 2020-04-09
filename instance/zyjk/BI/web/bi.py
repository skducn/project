# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-4-8
# Description: BI集成平台
# https://blog.csdn.net/xc_zhou/article/details/82415870 chrome浏览器的options参数
# varURL = https://192.168.0.183/admin/login?return=https%3A%2F%2F192.168.0.183%2Fbi%2FrealTimeMonitoringIndicator%2FtodayOperationalAnalysis&system=bi
# 016，123456
# *****************************************************************
# from time import sleep
#
#
#
# x = ('%.4f' % float(ff))
# print(x)
# sleep(1212)
# x = "123123123123123\n2344325\n345\n100%56345345345"
# x = x.split("%")[0].split("\n")
# a = x[-1]
# print(a)
# x = ['门急诊抗生素处方率', '门急诊药品处方率', '门急诊大额处方率',12]
# a= x[-1]
# print(a)
# # a = x[1]
# # print(a)
# # print(type(x[1]))
# sleep(1212)
# # x.pop()
# # x.pop()
# print(x)
# sleep(1212)
# varStr =' 总空床率95.58%\n总床位数1232 在用床位数57\n'
# str_list = list(varStr)
# nPos = str_list.index('在')
# str_list.insert(nPos, '\n')
# list1 = "".join(str_list).split("\n")
# list1.pop()
# print(list1)


# x = "急诊内科\n545\n急诊儿科(新)\n249\n"
# a = x.split("\n")
# a.pop(0)
# print(a)
# sleep(1212)
# # x = "工作台今日运营分析门急诊动态监测\n数据更新时间：2019-09-16 11:06:36\n各科室普通门诊业务量\n急诊内科\n545\n急诊儿科(新)\n249\n妇科\n253\n皮肤科\n223\n骨科\n223\n急诊骨科(新)\n202\n呼吸内科\n168\n儿科\n166\n心内科\n160\n急诊外科(新)\n152\n普通门诊医生接诊人次\n王**\n196\n王**\n196\n罗**\n139\n张**\n128\n刘**\n128\n李**\n127\n陈**\n107\n肖**\n102\n毛**\n90\n毛**\n90\n"
# # print(x.split("各科室普通门诊业务量")[1])
# #
# #

# # ===============================================================================================

from instance.zyjk.BI.PageObject.BiPO import *
Bi_PO = BiPO()
List_PO = ListPO()
Time_PO = TimePO()

# 登录 运营决策系统
Bi_PO.login()

# # ===============================================================================================

Bi_PO.menu1("实时监控指标")
#
print("[1.1 今日运营分析]" + " -" * 100)
Bi_PO.menu2ByHref("/bi/realTimeMonitoringIndicator/todayOperationalAnalysis")

# 1，遍历并分成多个列表（医院总收入，药品收入，今日门急诊量，今日门诊量，今日急诊量，今日门急诊收入，今日出院人数，今日在院，当前危重人数，今日住院实收入）
# Bi_PO.winByP()
# # 2，当前住院欠费明细
# print(Bi_PO.getContent("//tr"))

# c1,医院总收入 = 门急诊收入+住院收入
Bi_PO.checkValue("医院总收入(万元)", 'select a.sum+b.sum from(SELECT sum(totalaccount) sum  from bi_inpatient_yard where statisticsDate ="%s")a,(SELECT sum(outPAccount) sum from bi_outpatient_yard where statisticsDate ="%s")b ', varUpdateDate, varUpdateDate)

# c2,药品收入 = 当日急诊费用中药品类收入+住院药品类收入
Bi_PO.checkValue("药品收入(万元)", 'select a.sum +b.sum from(SELECT sum(outPMedicateAccount) sum  from bi_outpatient_yard where statisticsDate ="%s")a,(SELECT sum(inPMedicateAccount) sum FROM bi_inpatient_yard WHERE statisticsDate ="%s")b', varUpdateDate, varUpdateDate)

# c3,今日门急诊量 = 今日挂号为门诊和急诊的人次和
Bi_PO.checkValue("今日门急诊量", 'select sum(outPCount) from bi_outpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# c4,今日门诊量 = 今日挂号为门诊的人次和
Bi_PO.checkValue("今日门诊量", 'select sum(outpatientCount) from bi_outpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# c5,今日急诊量 = 今日挂号为急诊的人次和
Bi_PO.checkValue("今日急诊量", 'select sum(emergencyCount) from bi_outpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# c6,今日门急诊收入 = 今日门急诊收费总和
Bi_PO.checkValue("今日门急诊收入(万元)", 'select sum(outpaccount) from bi_outpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# c7,今日出院人数 = 今日做出院登记的患者人数之和
Bi_PO.checkValue("今日出院人数", 'select sum(leaveCount) from bi_inpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# c8,今日在院人数 = 住院状态为在院的患者人数之和
Bi_PO.checkValue("今日在院", 'select sum(inPCount) from bi_inpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# c9,当前危重人数 = 当前危重人数和
Bi_PO.checkValue("当前危重人数", 'select sum(criticalCount) from bi_inpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# c10,今日住院实收入 = 出入院财务中，记录在当日的费用之和
Bi_PO.checkValue("今日住院实收入(万元)", 'select sum(inPAccount) from bi_inpatient_yard where statisticsDate ="%s" ', varUpdateDate)



#
# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# print("\n[1.2 门急诊动态监测]" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/realTimeMonitoringIndicator/oaedDynamicMonitoring")
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
#
# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# print("\n1.3 住院动态监测" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/realTimeMonitoringIndicator/dynamicMonitoringInHospital")
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
#
# # #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# print("\n[1.4 医技动态监测]" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/realTimeMonitoringIndicator/operationTrend")
#
# # 1，遍历并分成多个列表（今日检验项目数，今日检验总费用，今日检查项目数，今日检查总费用）
# Bi_PO.winByP()
# a, b, c = Bi_PO.winByP("今日检查项目数")
# print(a, b, c)

# # ===============================================================================================
# #
# Bi_PO.menu1("门诊分析")
#
# print("\n[2.1 门诊业务]" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/outpatientAnalysis/outpatientService")
#
# # 1，遍历并分成多个列表（门诊预约人次，门诊人次，急诊人次，门急诊退号率）
# Bi_PO.winByP()
# a, b, c = Bi_PO.winByP("门急诊退号率")
# print(a, b, c)
#
# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# print("\n[2.2 门诊预约]" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/outpatientAnalysis/outpatientAppointment")
#
# # 1，遍历并分成多个列表（门诊预约人次，院内窗口预约）
# Bi_PO.winByP()
#
# # 2，门诊预约率
# reserveList = []
# tmpList2 = Bi_PO.getContent("//div")
# reserveList.append("门诊预约率")
# reserveList.append(tmpList2[0].split("门急预约人次月趋势\n")[1].split("\n门诊预约率")[0])
# print(List_PO.listBorderDict(reserveList))
#
# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# print("\n2.3 门诊处方" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/outpatientAnalysis/outpatientPrescriptions")  # 门诊处方
#
# # # 1，遍历并分成多个列表（门急诊处方数，门急诊抗生素处方数，门急诊药品处方数，门急诊大额处方数）
# Bi_PO.winByP()
#
# # 2，科室门急诊抗生素处方数分析
# prescriptionList = []
# tmpList1 = Bi_PO.getContent("//div")
#
# tmpList2 = tmpList1[0].split("%\n门急诊抗生素处方率")[0].split("\n")
# prescriptionList.append("门急诊抗生素处方率")
# prescriptionList.append(tmpList2[-1])
# tmpList2 = tmpList1[0].split("科室门急诊抗生素处方数分析\n")[1].split("%")[0].split("\n")
# prescriptionList.append("门急诊药品处方率")
# prescriptionList.append(tmpList2[-1])
# print(List_PO.listBorderDict(tmpList2))
#
# # 3，科室门急诊药品处方数分析
# tmpList3 = tmpList1[0].split("科室门急诊药品处方数分析\n")[1].split("%")[0].split("\n")
# prescriptionList.append("门急诊大额处方率")
# prescriptionList.append(tmpList3[-1])
# print(List_PO.listBorderDict(tmpList3))
#
# # 4，科室门急诊大额处方数分析
# tmpList4 = tmpList1[0].split("科室门急诊大额处方数分析\n")[1].split("\n")
# print(List_PO.listBorderDict(tmpList4))
#
# # 5，3个处方率（门急诊抗生素处方率，门急诊药品处方率，门急诊大额处方率）
# print(List_PO.listBorderDict(prescriptionList))
#
# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# print("\n2.4 门诊收入" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/outpatientAnalysis/outpatientIncome")
#
# # 1，遍历并分成多个列表（门急诊收入，门诊收入，急诊收入，门急诊均次费,，门急诊药品收入，门急诊药占比，门急诊均次药品费用）
# Bi_PO.winByP()
#
# # 2，门急诊收入科室排名
# Bi_PO.winByDiv("门急诊收入科室排名\n", "门急诊均次费月趋势", "")  # 获取门急诊收入科室排名列表中所有的值
#
# # 3，门急诊医疗收入构成分析
# print(Bi_PO.winByDiv("门急诊医疗收入构成分析\n", "", "检查收入"))  # 获取检查收入的值，如：235157


# # # ===============================================================================================
# #
# Bi_PO.menu1("住院分析")
#
# print("\n3.1 住院业务" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/hospitalizationAnnlysis/inpatientService")
#
# #  # 1，遍历并分成多个列表（入院人次，出院人次，出院平均住院日）
# Bi_PO.winByP()
#
# # 2，门急诊收入科室排名
# Bi_PO.winByDiv("平均住院日科室情况\n", "出院人次科室情况", "")
#
# # 3，门急诊医疗收入构成分析
# Bi_PO.winByDiv("出院人次科室情况\n", "", "")
# print(Bi_PO.winByDiv("出院人次科室情况\n", "", "骨科"))
#
# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# print("\n3.2 床位分析" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/hospitalizationAnnlysis/bedAnalysis")
#
# # #  # 1，遍历并分成多个列表（实际开放总床日数，实际占用总床日数，出院者占用总床日数，平均开放床位数，病床周转次数，床位使用率，平均每张床位工作日，病床工作日，出院患者平均住院日）
# Bi_PO.winByP()
# #
# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# #
# print("\n3.3 住院收入" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/hospitalizationAnnlysis/hospitalizationIncome")
#
# # 1，遍历并分成多个列表（医院总收入，住院总收入，住院均次费用，住院药品收入，住院均次药品费用，住院药占比）
# Bi_PO.winByP()
#
# # 2，门急诊收入科室排名
# Bi_PO.winByDiv("住院收入科室情况\n", "\n住院医疗收入构成分析", "")

#
# # # ===============================================================================================
# #
# Bi_PO.menu1("药品分析")
#
# print("\n4.1 基本用药分析" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/medicationAnalysis/essentialDrugsMedicare")
#
# # 1，遍历并分成多个列表（药品收入，中成药收入，中草药收入，西医收入，医保目录外药品收入，药占比）
# Bi_PO.winByP()
#
# # 2，门急诊收入科室排名
# Bi_PO.winByDiv("药占比科室情况\n", "各类药品收入月趋势", "")
#
# # 3，药品用量分析
# Bi_PO.winByDiv("药品用量分析\n", "", "")
#
# # #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# # #
# # print("\n4.2 抗菌药物用药分析" + " -" * 100)
# # Bi_PO.menu2ByHref("/bi/medicationAnalysis/antimicrobialAgent")
# # #
# # #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# # #
# print("\n4.3 注射输液用药分析" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/medicationAnalysis/injectionMedication")
# # # 1，遍历并分成多个列表（门急诊使用注射药物的百分比，门诊患者静脉输液使用率，住院患者抗菌药物使用率，住院患者静脉输液平均每床日使用袋（瓶）数，住院患者抗菌药物静脉输液占比，急诊患者静脉输液使用率）
# Bi_PO.winByP()

# # # ===============================================================================================
# #
# Bi_PO.menu1("手术分析")
#
# print("\n5.1 手术分析" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/operativeAnalysisTip/operativeAnalysis")
#
# # # 1，遍历并分成多个列表（住院手术例数，住院患者手术人次数，日间手术例数，日间手术人次数，三四级手术占比，麻醉总例数）
# Bi_PO.winByP()
#
# # 2，门急诊收入科室排名
# Bi_PO.winByDiv("手术例数科室分析\n", "\n手术主刀医生排名", "")
# Bi_PO.winByDiv("手术主刀医生排名\n", "\n手术排名", "")
# Bi_PO.winByDiv("手术排名\n", "", "")
#
# # # ===============================================================================================
# #
# Bi_PO.menu1("医保分析")
# #
# print("\n6.1 住院医保" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/medicalInsuranceAnalysis/hospitalizationInsurance")
#
# # # 1，遍历并分成多个列表（住院医保患者人次，住院医保患者总费用，住院医保患者均次费，住院医保支付金额，住院医保患者药占比，住院医保患者自费占比）
# Bi_PO.winByP()
#
# # # 2，门急诊收入科室排名
# Bi_PO.winByDiv("各科室住院医保患者均次费分析\n", "", "")
#

# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# # 门急诊医保
# Bi_PO.menu2ByHref("/bi/medicalInsuranceAnalysis/outpatientEmergeInsurance")
#
# # ===============================================================================================
#
# Bi_PO.menu1("医技分析")
#
# # 检验分析
# Bi_PO.menu2ByHref("/bi/medicalTechnologyAnalysis/InspectionAnalysis")
#
# # 检查分析
# Bi_PO.menu2ByHref("/bi/medicalTechnologyAnalysis/ExamineAnalysis")
#
# # ===============================================================================================
#
# Bi_PO.menu1("医疗质量")
#
# # 治疗质量
# Bi_PO.menu2ByHref("/bi/medicalQuality/treatmentQuality")
#
# # 诊断质量
# Bi_PO.menu2ByHref("/bi/medicalQuality/diagnosticQuality")