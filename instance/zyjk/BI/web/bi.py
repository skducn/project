# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2020-4-8
# Description: BI集成平台
# *****************************************************************
# from time import sleep
#
# a = "使用率"
# b = "频率"
# c = "率312频3使用率用2"
#
# if a in c or b in c:
#     print("11111111111")
# else:
#     print("22222222")
#
# sleep(1212)


from instance.zyjk.BI.PageObject.BiPO import *
Bi_PO = BiPO()
List_PO = ListPO()
Time_PO = TimePO()

# 登录 运营决策系统
Bi_PO.login()

# 获取当前数据更新时间
varDataUpdateDate = Bi_PO.Web_PO.getXpathText('//*[@id="app"]/section/section/section/main/div[1]/span')
Bi_PO.Log_PO.logger.info(varDataUpdateDate)
varUpdateDate = str(varDataUpdateDate).split("数据更新时间：")[1].split(" ")[0]



# ===============================================================================================
print("\n")
sleep(2)
Bi_PO.menu1("实时监控指标")
Bi_PO.menu2ByHref("1.1 今日运营分析", "/bi/realTimeMonitoringIndicator/todayOperationalAnalysis", varUpdateDate)


# 1.1.1 医疗业务收入 = 门急诊收入+ 住院收入
Bi_PO.monitor("医疗业务收入(万元)", 'SELECT round((select (a.sum+b.sum)/10000 from(SELECT IFNULL(sum(inPAccount),0) sum  from bi_inpatient_yard where statisticsDate ="%s")a,(SELECT IFNULL(sum(outPAccount),0) sum FROM bi_outpatient_yard WHERE statisticsDate ="%s")b),2)', varUpdateDate, varUpdateDate)

# 1.1.2 药品收入(万元) = 当日急诊费用中药品类收入+住院药品类收入
Bi_PO.monitor("药品收入(万元)", 'select round((select (a.sum +b.sum)/10000 from(SELECT ifnull(sum(outPMedicateAccount),0) sum  from bi_outpatient_yard where statisticsDate ="%s")a,(SELECT IFNULL(sum(inPMedicateAccount),0) sum FROM bi_inpatient_yard WHERE statisticsDate ="%s")b),2)', varUpdateDate, varUpdateDate)

# 1.1.3 今日门急诊量(例) = 今日挂号为门诊和急诊的人次和
Bi_PO.monitor("今日门急诊量(例)", 'select ifnull(sum(outPCount),0) from bi_outpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# 1.1.4 今日门诊量(例) = 今日挂号为门诊的人次和
Bi_PO.monitor("今日门诊量(例)", 'select ifnull(sum(outpatientCount),0) from bi_outpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# 1.1.5 今日急诊量(例) = 今日挂号为急诊的人次和
Bi_PO.monitor("今日急诊量(例)", 'select sum(emergencyCount) from bi_outpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# 1.1.6 今日门急诊收入(万元) = 今日门急诊收费总和
Bi_PO.monitor("今日门急诊收入(万元)", 'select round(sum(outpaccount)/10000,2) from bi_outpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# 1.1.7 今日出院人数(例) = 今日做出院登记的患者人数之和
Bi_PO.monitor("今日出院人数(例)", 'select sum(leaveCount) from bi_inpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# 1.1.8 今日在院人数(例) = 住院状态为在院的患者人数之和
Bi_PO.monitor("今日在院(例)", 'select sum(inPCount) from bi_inpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# 1.1.9 当前危重人数(例) = 当前危重人数和
Bi_PO.monitor("当前危重人数(例)", 'select sum(criticalCount) from bi_inpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# 1.1.10 今日住院实收入(万元) = 出入院财务中，记录在当日的费用之和
Bi_PO.monitor("今日住院实收入(万元)", 'select round(sum(inPAccount)/10000,2) from bi_inpatient_yard where statisticsDate ="%s" ', varUpdateDate)

# # 2，当前住院欠费明细
print(Bi_PO.getContent("//tr"))

Bi_PO.menu1Close("实时监控指标")




# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
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
#



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
#




# # #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#
# print("\n[1.4 医技动态监测]" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/realTimeMonitoringIndicator/operationTrend",vatUpdateDate)
#
# # 1，遍历并分成多个列表（今日检验项目数，今日检验总费用，今日检查项目数，今日检查总费用）
# Bi_PO.winByP()
# a, b, c = Bi_PO.winByP("今日检查项目数")
# print(a, b, c)




# ===============================================================================================
print("\n")
sleep(2)
Bi_PO.menu1("门诊分析")  # 同期，同比，逻辑未处理？？
varUpdateDate = "2020-03-22"
Bi_PO.menu2ByHref("2.1 门诊业务", "/bi/outpatientAnalysis/outpatientService", varUpdateDate)


# c1,门急诊人次 = 统计期内挂号为门诊和急诊的人次和
Bi_PO.tongqi("门急诊人次(万人)", 'select round((SELECT sum(outPCount)/10000 from bi_outpatient_yard where statisticsDate ="%s"),2)', varUpdateDate)

# c2,门诊人次 = 门诊挂号人次
Bi_PO.tongqi("门诊人次(万人)", 'select round((SELECT sum(outpatientCount)/10000 from bi_outpatient_yard where statisticsDate ="%s"),2)', varUpdateDate)

# c3,急诊人次 = 急诊+留观人次
Bi_PO.tongqi("急诊人次(万人)", 'select round((SELECT sum(emergencyCount)/10000 from bi_outpatient_yard where statisticsDate ="%s"),2)', varUpdateDate)

# c4,门急诊退号率 = 统计期内门急诊退号人次/门急诊总挂号人次
Bi_PO.tongqi("门急诊退号率", 'SELECT sum(backRegisterRatio) from bi_outpatient_yard where statisticsDate="%s" ', varUpdateDate)




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
print("\n")
sleep(2)
varUpdateDate = "2020-03-22"
Bi_PO.menu2ByHref("2.3 门诊处方", "/bi/outpatientAnalysis/outpatientPrescriptions", varUpdateDate)  # 门诊处方


# 2.3.1 门急诊处方数(张) = 统计期内门急诊处方数量之和
Bi_PO.tongqi("门急诊处方数(张)", 'SELECT quantity from bi_hospital_recipe_day WHERE statisticsDate ="%s" ', varUpdateDate)

# 2.3.2 门急诊抗生素处方数(张) = 统计期内处方种含有抗生素药品的处方之和
Bi_PO.tongqi("门急诊抗生素处方数(张)", 'SELECT antibioticRecipe from bi_hospital_recipe_day WHERE statisticsDate="%s" ', varUpdateDate)

# 2.3.3 门急诊药品处方数(张) = 统计期内处方为药品的处方之和
Bi_PO.tongqi("门急诊药品处方数(张)", 'SELECT drugRecipe from bi_hospital_recipe_day WHERE statisticsDate ="%s" ', varUpdateDate)

# 2.3.4 门急诊大额处方数(张) = 统计期内处方为大额处方之和（大额处方看医院的标准，参照上海门诊均次费用的百分之60上限）
Bi_PO.tongqi("门急诊大额处方数(张)", 'SELECT largeRecipe from bi_hospital_recipe_day WHERE statisticsDate="%s" ', varUpdateDate)

prescriptionList = []
tmpList1 = Bi_PO.getContent("//div")
tmpList2 = tmpList1[0].split("%\n门急诊抗生素处方率")[0].split("\n")
prescriptionList.append("门急诊抗生素处方率")
prescriptionList.append(tmpList2[-1])

# 2.3.5 科室门急诊抗生素处方数分析
tmpList2 = tmpList1[0].split("科室门急诊抗生素处方数分析\n")[1].split("%")[0].split("\n")
tmpList2 = List_PO.listConvertElement(tmpList2)
top10Dict2 = List_PO.list2dictBySerial(tmpList2)
Bi_PO.top10("0", top10Dict2, "科室门急诊抗生素处方数分析", 'SELECT deptName,antibioticRecipe from bi_dept_recipe_day WHERE statisticsDate = "%s" ORDER BY antibioticRecipe DESC limit 10', varUpdateDate)

# 2.3.6 科室门急诊药品处方数分析
tmpList3 = tmpList1[0].split("科室门急诊药品处方数分析\n")[1].split("%")[0].split("\n")
tmpList3 = List_PO.listConvertElement(tmpList3)
top10Dict3 = List_PO.list2dictBySerial(tmpList3)
Bi_PO.top10("0", top10Dict3, "科室门急诊药品处方数分析", 'SELECT deptName,drugRecipe from bi_dept_recipe_day WHERE statisticsDate ="%s" ORDER BY antibioticRecipe DESC limit 10', varUpdateDate)

# 2.3.7 科室门急诊大额处方数分析
tmpList4 = tmpList1[0].split("科室门急诊大额处方数分析\n")[1].split("\n")
tmpList4 = List_PO.listConvertElement(tmpList4)
top10Dict4 = List_PO.list2dictBySerial(tmpList4)
Bi_PO.top10("0", top10Dict4, "科室门急诊大额处方数分析", 'SELECT deptName,largeRecipe from bi_dept_recipe_day WHERE statisticsDate ="%s" order by largerecipe desc limit 10', varUpdateDate)

# 2.3.8 门急诊抗生素处方率，门急诊药品处方率，门急诊大额处方率
prescriptionList.append("门急诊药品处方率")
prescriptionList.append(tmpList2[-1])
prescriptionList.append("门急诊大额处方率")
prescriptionList.append(tmpList3[-1])
pageList = List_PO.list2dictBySerial(prescriptionList)

Bi_PO.singleSQL(pageList, "门急诊抗生素处方率", 'SELECT round((SELECT a.sum/b.sum*100 from (SELECT sum(antibioticRecipe) sum from bi_hospital_recipe_day WHERE statisticsDate ="%s")a,(SELECT sum(quantity) sum from bi_hospital_recipe_day WHERE statisticsDate ="%s")b),2) ', varUpdateDate, varUpdateDate)
Bi_PO.singleSQL(pageList, "门急诊药品处方率", 'SELECT round((SELECT a.sum/b.sum*100 from (SELECT sum(drugRecipe) sum from bi_hospital_recipe_day WHERE statisticsDate ="%s")a,(SELECT sum(quantity) sum from bi_hospital_recipe_day WHERE statisticsDate ="%s")b),2)', varUpdateDate, varUpdateDate)
Bi_PO.singleSQL(pageList, "门急诊大额处方率", 'SELECT round((SELECT a.sum/b.sum*100 from (SELECT sum(largeRecipe) sum from bi_hospital_recipe_day WHERE statisticsDate ="%s")a,(SELECT sum(quantity) sum from bi_hospital_recipe_day WHERE statisticsDate ="%s")b),2) ', varUpdateDate, varUpdateDate)



# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print("\n")
sleep(2)
varUpdateDate = "2020-03-22"
Bi_PO.menu2ByHref("2.4 门诊收入", "/bi/outpatientAnalysis/outpatientIncome", varUpdateDate)


# 2.4.1 门急诊收入(万元) = 统计期内门急诊收入之和
Bi_PO.tongqi("门急诊收入(万元)", 'SELECT ROUND((SELECT sum(outPAccount)/10000 from bi_outpatient_yard where statisticsDate ="%s"),2)', varUpdateDate)

# 2.4.2 门诊收入(万元) = 统计期内门诊收入之和
Bi_PO.tongqi("门诊收入(万元)", 'SELECT ROUND((SELECT sum(outpatientAccount)/10000 from bi_outpatient_yard where statisticsDate ="%s"),2)', varUpdateDate)

# 2.4.3 急诊收入(万元) = 统计期内急诊收入之和
Bi_PO.tongqi("急诊收入(万元)", 'SELECT ROUND((SELECT sum(emergencyAccount)/10000 from bi_outpatient_yard where statisticsDate ="%s"),2)', varUpdateDate)

# 2.4.4 门急诊均次费(万元) = 统计期内门急诊收入之和/门急诊挂号人次和
Bi_PO.tongqi("门急诊均次费(元)", 'select round((SELECT sum(outPCountFee) from bi_outpatient_yard where statisticsDate ="%s"),2)', varUpdateDate)

# 2.4.5 门急诊药品收入(万元) = 统计期内门诊药品收入之和
Bi_PO.tongqi("门急诊药品收入(万元)", 'SELECT round((SELECT sum(outPMedicateAccount)/10000 from bi_outpatient_yard where statisticsDate ="%s"),2)', varUpdateDate)

# 2.4.6 门急诊药占比=统计期内门急诊费用中药品费用之和/门急诊收入之和
Bi_PO.tongqi("门急诊药占比", 'SELECT round((SELECT sum(outPMedicateRatio) from bi_outpatient_yard where statisticsDate ="%s"),2)', varUpdateDate)

# 2.4.7 门急诊均次药品费用(元) = 统计期内门急诊药品处方收入之和/门急诊人次
Bi_PO.tongqi("门急诊均次药品费用(元)", 'SELECT round((SELECT a.sum/b.sum from((SELECT sum(outPMedicateAccount) sum from bi_outpatient_yard where statisticsDate ="%s")a,(SELECT sum(outPCount) sum  from bi_outpatient_yard where statisticsDate ="%s")b)),2)', varUpdateDate,varUpdateDate)

# 2.4.8 门急诊收入科室排名
top10Dict248 = Bi_PO.winByDiv("门急诊收入科室排名\n", "门急诊均次费月趋势", "")  # 获取门急诊收入科室排名列表中所有的值
Bi_PO.top10("0", top10Dict248, "门急诊收入科室排名", 'SELECT deptname,round(outPAccount,2) from bi_outpatient_dept where statisticsDate ="%s" GROUP BY deptname ORDER BY outpaccount DESC LIMIT 10', varUpdateDate)

# 2.4.9 门急诊医疗收入构成分析
Bi_PO.Color_PO.consoleColor("31", "33", "[warning], 2.4.9 门急诊医疗收入构成分析, 未提供sql", "")
Bi_PO.Log_PO.logger.warning("2.4.9 门急诊医疗收入构成分析, 未提供sql")
top10Dict249 = Bi_PO.winByDiv("门急诊医疗收入构成分析\n", "", "")
# print(Bi_PO.winByDiv("门急诊医疗收入构成分析\n", "", "检查收入"))  # 获取检查收入的值，如：235157

Bi_PO.menu1Close("门诊分析")



# # # ===============================================================================================
print("\n")
sleep(2)
Bi_PO.menu1("住院分析")
varUpdateDate = "2020-03-22"
Bi_PO.menu2ByHref("3.1 住院业务", "/bi/hospitalizationAnnlysis/inpatientService", varUpdateDate)


# 3.1.1 入院人次 = 统计期内患者进行入院登记的人次数和
Bi_PO.tongqi("入院人次", 'select sum(admissionCount) from bi_inpatient_yard where statisticsDate ="%s"', varUpdateDate)

# 3.1.2 出院人次 = 统计期内进行出院登记的人次和
Bi_PO.tongqi("出院人次", 'select sum(leaveCount) from bi_inpatient_yard where statisticsDate ="%s"', varUpdateDate)

# 3.1.3 出院平均住院日(日) = 统计期内出院患者平均住院日，患者状态为出院的住院天数之和/出院患者总人次
Bi_PO.tongqi("出院平均住院日(日)", 'select round((select sum(leaveInPDayAvg) from bi_inpatient_yard where statisticsDate ="%s"),2)', varUpdateDate)

# 3.1.4 平均住院日科室情况 = 统计期内各科室患者平均住院日排名，科室患者状态为科室出院的住院天数之和/科室出院患者总人次【前N（10）个科室平均住院日排名】
top10Dict5 = Bi_PO.winByDiv("平均住院日科室情况\n", "出院人次科室情况", "")  # 获取门急诊收入科室排名列表中所有的值
Bi_PO.top10("0.00", top10Dict5, "平均住院日科室情况", 'select deptname,round(AVG(avgInPDay),2)t from bi_inpatient_dept where statisticsDate="%s" GROUP BY deptname ORDER BY t DESC LIMIT 10', varUpdateDate)

# 3.1.5 出院人次科室情况
top10Dict5 = Bi_PO.winByDiv("出院人次科室情况\n", "出院平均住院日月趋势", "")  # 获取门急诊收入科室排名列表中所有的值
Bi_PO.top10("0", top10Dict5, "出院人次科室情况", 'SELECT deptname,sum(inPCount) as t from bi_inpatient_dept where statisticsDate ="%s" GROUP BY deptname ORDER BY t DESC LIMIT 10', varUpdateDate)

# # 2，门急诊收入科室排名
# Bi_PO.winByDiv("平均住院日科室情况\n", "出院人次科室情况", "")
#
# # 3，门急诊医疗收入构成分析
# Bi_PO.winByDiv("出院人次科室情况\n", "", "")
# print(Bi_PO.winByDiv("出院人次科室情况\n", "", "骨科"))



# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print("\n")
sleep(2)
varUpdateDate = "2020-03-22"
Bi_PO.menu2ByHref("3.2 床位分析", "/bi/hospitalizationAnnlysis/bedAnalysis", varUpdateDate)


# 3.2.1 实际开放总床日数 = 统计期内医院开放的床日数之和
Bi_PO.tongqi("实际开放总床日数", 'select sum(realBedCount) from bi_inpatient_yard_bed where statisticsDate ="%s"', varUpdateDate)

# 3.2.2,实际占用总床日数 = 统计期内患者占用总床日数和
Bi_PO.tongqi("实际占用总床日数", 'select sum(realOccupyBedCount) from bi_inpatient_yard_bed where statisticsDate ="%s"', varUpdateDate)

# 3.2.3 出院者占用总床日数 = 统计期内所有出院人数的住院床日之总和
Bi_PO.tongqi("出院者占用总床日数", 'SELECT round((SELECT a.sum*b.sum from (select sum(leaveInPDayAvg) sum from bi_inpatient_yard where statisticsDate ="%s")a,(select sum(leaveCount) sum  from bi_inpatient_yard where statisticsDate ="%s")b),2)', varUpdateDate,varUpdateDate)

# 3.2.4 平均开放床位数 = 统计期内实际开放总床日数／统计日数
Bi_PO.tongqi("平均开放床位数", 'select sum(realBedCount) from bi_inpatient_yard_bed where statisticsDate ="%s"', varUpdateDate)

# 3.2.5 病床周转次数 = 统计期内出院人数／平均开放床位数
Bi_PO.tongqi("病床周转次数", 'SELECT round((SELECT a.sum/b.sum from(select sum(leaveCount) sum from bi_inpatient_yard where statisticsDate ="%s")a,(select sum(realBedCount) sum  from bi_inpatient_yard_bed where statisticsDate ="%s")b),2)', varUpdateDate,varUpdateDate)

# 3.2.6 床位使用率 = 统计期内实际占用总床日数／实际开放总床日数
Bi_PO.tongqi("床位使用率", 'SELECT round((select 100*(a.sum/b.sum) from(select sum(realOccupyBedCount) sum from bi_inpatient_yard_bed where statisticsDate ="%s")a,(select sum(realBedCount) sum  from bi_inpatient_yard_bed where statisticsDate ="%s")b),2)', varUpdateDate,varUpdateDate)

# 3.2.7 平均每张床位工作日 = 统计期内出院者占用总床日数/床位数
Bi_PO.tongqi("平均每张床位工作日", 'SELECT round(a.sum/b.sum,2)from (SELECT sum(leaveInPDayAvg*leaveCount) sum from bi_inpatient_yard where statisticsDate ="%s")a,(select sum(realBedCount) sum from bi_inpatient_yard_bed   where statisticsDate ="%s")b', varUpdateDate,varUpdateDate)

# 3.2.8 病床工作日 = 统计期内实际占用总床日数／平均开放床位数
Bi_PO.tongqi("病床工作日", 'SELECT round(a.sum/b.sum,2) from (select sum(realOccupyBedCount) sum from bi_inpatient_yard_bed where statisticsDate ="%s")a,(select sum(realBedCount) sum from bi_inpatient_yard_bed   where statisticsDate ="%s")b', varUpdateDate,varUpdateDate)

# 3.2.9 出院患者平均住院日 = 统计期内出院患者占有总床日数/出院人数
Bi_PO.tongqi("出院患者平均住院日", 'SELECT round(a.sum/b.sum,2) from (SELECT sum(leaveInPDayAvg*leaveCount) sum from bi_inpatient_yard where statisticsDate ="%s")a,(select sum(leaveCount) sum from bi_inpatient_yard where statisticsDate ="%s")b', varUpdateDate,varUpdateDate)



# #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print("\n")
sleep(2)
varUpdateDate = "2020-03-22"
Bi_PO.menu2ByHref("3.3 住院收入", "/bi/hospitalizationAnnlysis/hospitalizationIncome", varUpdateDate)


# 3.3.1医院总收入(万元) = 统计期内住院患者总收入+门诊患者总收入
Bi_PO.tongqi("医院总收入(万元)", 'select round((a.sum+b.sum)/10000,2) from((SELECT sum(inPAccount) sum from bi_inpatient_yard WHERE statisticsDate ="%s")a,(SELECT sum(outPAccount) sum  from bi_outpatient_yard where statisticsDate ="%s")b)', varUpdateDate,varUpdateDate)

# 3.3.2 住院总收入(万元) = 统计期内所有在院和出院的患者总收入和
Bi_PO.tongqi("住院总收入(万元)", 'SELECT ifnull(round((SELECT inPAccount/10000 FROM bi_inpatient_yard where statisticsDate = "%s"),2),0)', varUpdateDate)

# 3.3.3 住院均次费用(元) = 统计期内住院患者总收入和/患者总人次
Bi_PO.tongqi("住院均次费用(元)", 'SELECT  round(sum(inpaccount)/sum(inpcount),2) from bi_inpatient_yard WHERE statisticsDate ="%s"', varUpdateDate)

# 3.3.4 住院药品收入(万元) = 统计期内住院药品收入之和
Bi_PO.tongqi("住院药品收入(万元)", 'SELECT round((SELECT inPMedicateAccount/10000 from bi_inpatient_yard where statisticsDate = "%s"),2)', varUpdateDate)

# 3.3.5 住院均次药品费用(元) = 统计期内住院患者药品总收入和/患者总人次
Bi_PO.tongqi("住院均次药品费用(元)", 'SELECT round(sum(inPMedicateAccount)/sum(inpcount),2) from bi_inpatient_yard where statisticsDate = "%s"', varUpdateDate)

# 3.3.6 住院药占比 = 统计期内住院药品收入/住院总收入
Bi_PO.tongqi("住院药占比", 'SELECT round((SELECT inPMedicateRatio from bi_inpatient_yard where statisticsDate = "%s"),2)', varUpdateDate)

# 3.3.7 住院收入科室情况 = 统计期内各科室住院患者费用之和排名【前N（15）个科室收入】

top10Dict5 = Bi_PO.winByDiv("住院收入科室情况\n", "\n住院医疗收入构成分析", "")
Bi_PO.top10("0", top10Dict5, "住院收入科室情况", 'SELECT deptname,round(sum(inPAccount),2) from bi_inpatient_dept WHERE statisticsDate ="%s" GROUP BY deptname ORDER BY sum(inPAccount) DESC LIMIT 10', varUpdateDate)

Bi_PO.menu1Close("住院分析")



# # # ===============================================================================================
print("\n")
sleep(2)
Bi_PO.menu1("药品分析")
varUpdateDate = "2020-03-22"
Bi_PO.menu2ByHref("4.1 基本用药分析", "/bi/medicationAnalysis/essentialDrugsMedicare", varUpdateDate)
sleep(2)

# 4.1.1 药品收入(万元) = 中成药费用+中草药费用+西药费用
Bi_PO.tongqi("药品收入(万元)", 'SELECT round((SELECT sum(pmcost+wmcost+hmcost)/10000 FROM bi_hospital_drugcosts_day WHERE statisticsDate ="%s"),2)', varUpdateDate)

# 4.1.2 中成药收入(万元) = 统计期内门急诊中成药处方收入+住院中成药医嘱收入
Bi_PO.tongqi("中成药收入(万元)", 'SELECT round((select sum(pmcost)/10000 from bi_hospital_drugcosts_day where statisticsDate ="%s"),2)', varUpdateDate)

# 4.1.3 中药饮片(万元) = 统计期内门急诊中草药处方收入+住院中草药医嘱收入
Bi_PO.tongqi("中药饮片(万元)", 'SELECT round((select sum(hmCost)/10000 from bi_hospital_drugcosts_day where statisticsDate ="%s"),2)', varUpdateDate)

# 4.1.4 西医收入(万元) = 统计期内门急诊西药处方收入+住院西医嘱收入
Bi_PO.tongqi("西医收入(万元)", 'SELECT round((select sum(wmCost)/10000 from bi_hospital_drugcosts_day where statisticsDate ="%s"),2)', varUpdateDate)

# 4.1.5 医保目录外药品收入(万元) = 统计期内门急诊非医保药品处方收入+住院非医保药品医嘱收入
Bi_PO.tongqi("医保目录外药品收入(万元)", 'SELECT round((select sum(insuranceCost)/10000 from bi_hospital_drugcosts_day where statisticsDate ="%s"),2)', varUpdateDate)

# 4.1.6 药占比 = 统计期内（门急诊药品收入+住院药品收入）/（门急诊收入+住院收入）
Bi_PO.tongqi("药占比", 'SELECT round((SELECT (SUM(drug.hmCost+drug.pmCost+drug.wmCost)/(`out`.outPAccount+inp.inPAccount))*100 FROM bi_hospital_drugcosts_day AS drug LEFT JOIN(SELECT outPAccount,statisticsDate FROM bi_outpatient_yard WHERE statisticsDate BETWEEN "%s" AND "%s" ) AS `out` ON `out`.statisticsDate = drug.statisticsDate LEFT JOIN (SELECT inPAccount,statisticsDate FROM bi_inpatient_yard WHERE statisticsDate BETWEEN "%s" AND "%s") AS inp ON inp.statisticsDate = drug.statisticsDate WHERE drug.statisticsDate BETWEEN "%s" AND "%s"),2)', varUpdateDate, varUpdateDate, varUpdateDate, varUpdateDate, varUpdateDate, varUpdateDate)

# # 2，门急诊收入科室排名
# Bi_PO.winByDiv("药占比科室情况\n", "各类药品收入月趋势", "")
#
# # 3，药品用量分析
# Bi_PO.winByDiv("药品用量分析\n", "", "")



# # #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print("\n")
sleep(2)
varUpdateDate = "2020-03-22"
Bi_PO.menu2ByHref("4.2 抗菌药物用药分析", "/bi/medicationAnalysis/antimicrobialAgent", varUpdateDate)


# 4.2.1 抗菌药物药占比 = 统计期内（门诊抗菌药品费用+住院抗菌药品费用）/（门诊药品总费用+住院有药品总费用）
Bi_PO.tongqi("抗菌药物药占比", 'SELECT b.sum/a.sum from (SELECT sum(pmcost+wmcost+hmcost) sum FROM bi_hospital_drugcosts_day WHERE statisticsDate ="%s")a,(select sum(antibacterialCost) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type in(1,3))b',varUpdateDate,varUpdateDate)

# 4.2.2 门急诊抗菌药物均次费(元) = 门急诊抗菌药物费用/门急诊使用抗菌药物人次
Bi_PO.tongqi("门急诊抗菌药物均次费(元)", 'SELECT ifnull(round((SELECT b.sum/a.sum from (SELECT sum(antibacterialPeople) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type in (1,2))a,(SELECT sum(antibacterialCost) sum  from bi_hospital_drugcosts_day WHERE statisticsDate ="%s")b),2),0)',varUpdateDate,varUpdateDate)

# 4.2.3 门诊患者抗菌药物使用率 = 统计期内门诊患者使用抗菌药物人次/同期门诊总人次
Bi_PO.tongqi("门诊患者抗菌药物使用率", 'SELECT round((SELECT b.sum/a.sum from((SELECT sum(outpatientCount) sum from bi_outpatient_yard WHERE statisticsDate ="%s")a,(SELECT sum(antibacterialPeople) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=1)b)),2)',varUpdateDate,varUpdateDate)

# 4.2.4 急诊患者抗菌药物使用率 = 统计期内急诊患者使用抗菌药物人次/同期急诊总人次
Bi_PO.tongqi("急诊患者抗菌药物使用率", 'SELECT b.sum/a.sum from((SELECT sum(emergencyCount) sum from bi_outpatient_yard WHERE statisticsDate ="%s")a,(SELECT sum(antibacterialPeople) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=2)b)',varUpdateDate,varUpdateDate)

# 4.2.5 住院患者抗菌药物使用率 = 统计期内住院患者使用抗菌药物人次/同期住院总人次
Bi_PO.tongqi("住院患者抗菌药物使用率", 'SELECT round((SELECT b.sum/a.sum from((SELECT sum(inpCount) sum from bi_inpatient_yard WHERE statisticsDate ="%s")a,(SELECT sum(antibacterialPeople) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=3)b)),2)',varUpdateDate,varUpdateDate)

# 4.2.6 Ⅰ类切口手术患者预防使用抗菌药物使用率
Bi_PO.Color_PO.consoleColor("31", "33", "[warning], 4.2.6 Ⅰ类切口手术患者预防使用抗菌药物使用率, 未提供SQL", "")
Bi_PO.Log_PO.logger.warning("4.2.6 Ⅰ类切口手术患者预防使用抗菌药物使用率, 未提供SQL")


# # #  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
print("\n")
sleep(2)
varUpdateDate = "2020-03-22"
Bi_PO.menu2ByHref("4.3 注射输液用药分析", "/bi/medicationAnalysis/injectionMedication", varUpdateDate)


# 4.3.1 门急诊使用注射药物的百分比 = 用法为注射（肌肉、静脉）的门急诊人次/门急诊总人次
Bi_PO.tongqi("门急诊使用注射药物的百分比", 'SELECT round((SELECT a.sum/b.sum from (SELECT sum(injection+vein) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type in(1,2))a,(SELECT sum(outPCount) sum from bi_outpatient_yard where statisticsDate ="%s")b),2)', varUpdateDate, varUpdateDate)

# 4.3.2 门诊患者静脉输液使用率 = 门诊患者静脉输液使用人次/同期门诊患者总人次
Bi_PO.tongqi("门诊患者静脉输液使用率", 'SELECT round((SELECT a.sum/b.sum from(SELECT sum(vein) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=1)a,(SELECT sum(outpatientCount) sum from bi_outpatient_yard where statisticsDate ="%s")b),2)' ,varUpdateDate, varUpdateDate)

# 4.3.3 住院患者抗菌药物使用率 = 统计期内住院患者使用抗菌药物人次/同期住院总人次
Bi_PO.tongqi("住院患者抗菌药物使用率", 'SELECT round((SELECT b.sum/a.sum from((SELECT sum(inpCount) sum from bi_inpatient_yard WHERE statisticsDate ="%s")a,(SELECT sum(antibacterialPeople) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=3)b)),2)', varUpdateDate, varUpdateDate)

# 4.3.4 住院患者静脉输液平均每床日使用袋（瓶）数 = 住院患者静脉输液总袋（瓶）数/同期住院患者实际开放总床日数
Bi_PO.tongqi("住院患者静脉输液平均每床日使用袋（瓶）数", 'SELECT ifnull(round((SELECT  a.sum/b.sum from (SELECT sum(arrAntibacterialVeinNumber) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=3)a,(select sum(realBedCount) sum  from bi_inpatient_yard_bed  where statisticsDate ="%s")b),2),0)', varUpdateDate, varUpdateDate)

# 4.3.5 住院患者抗菌药物静脉输液占比=住院患者抗菌药物静脉输液例数/同期住院患者静脉输液总例数
Bi_PO.tongqi("住院患者抗菌药物静脉输液占比", 'SELECT a.sum/b.sum from(SELECT sum(vein) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=3)a,(SELECT sum(arrAntibacterialVein) sum from bi_hospital_drugcosts_day where statisticsDate ="%s")b', varUpdateDate, varUpdateDate)

# 4.3.6 急诊患者静脉输液使用率=急诊患者静脉输液使用人次/同期急诊患者总人次
Bi_PO.tongqi("急诊患者静脉输液使用率", 'SELECT ifnull(round((SELECT a.sum/b.sum from(SELECT sum(vein) sum from bi_hospital_drugcosts_day WHERE statisticsDate ="%s" and type=2)a,(SELECT sum(emergencyCount) sum from bi_outpatient_yard where statisticsDate ="%s")b),2),0)', varUpdateDate, varUpdateDate)



# # # ===============================================================================================
# #
# Bi_PO.menu1("手术分析")
#
# print("\n5.1 手术分析" + " -" * 100)
# Bi_PO.menu2ByHref("/bi/operativeAnalysisTip/operativeAnalysis", varUpdateDate)
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
# Bi_PO.menu1("医技分析")
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