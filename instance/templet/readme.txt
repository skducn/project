【新质控测试流程说明】
1，启动jar包，如：java -jar {D:\51\python\project\instance\zyjk\EHR\controlRuleNew1\config\healthRecordRules.jar}

2，清除HrRuleRecord表数据，如：DELETE HrRuleRecord

3，修改数据库判断规则sql1/sql2， 如：{update HrCover set name=null}

4，执行质控接口，如：curl http://localhost:8080/healthRecordRules/rulesApi/execute/{档案编号}

5，查看质控结果 ，如：SELECT t2.Comment,t2.Categories, t2.RuleSql FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId

6，恢复数据库判断规则sql1/sql2，如：{UPDATE  HrCover set name='舒阳'}
===========================================================================

【新质控测试流程语句】
java -jar D:\51\python\project\instance\zyjk\EHR\controlRuleNew1\config\healthRecordRules.jar
DELETE HrRuleRecord
update HrCover set name=null
curl http://localhost:8080/healthRecordRules/rulesApi/execute/31011310200312009116
SELECT t2.Comment,t2.Categories, t2.RuleSql FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId
UPDATE  HrCover set name='舒阳'

===========================================================================

【新质控自动化说明之config.ini】
ruleType的规则：判断规则类型，可选项：规范性，完整性，一致性，有效性，追溯性，空或其他值。
如：ruleType = 完整性    //表示只执行规则类型为完整性的用例，其他规则类型用例忽略。
ruleType =          //空或其他值表示执行所有规则类型。

isRun的规则：判断测试结果，可选项：error，ok，empty，空或其他值。
如：isRun = error   //表示只执行表格中测试结果为error的用例
isRun = ok   //表示只执行表格中测试结果中为ok的用例
isRun = empty   //表示只执行表格中测试结果为空的用例
isRun =     //空或其他值表示执行所有用例

caseFrom和caseTo的规则：两者需配套使用，表示执行某区间的用例，表格里默认用例起始编号是 2，caseFrom 是起始用例编号，caseTo  是结束用例编号。如：
正常取值范围，表示只执行表格里从用例2到用例4
caseFrom = 2
caseTo = 5
或 ， 表示只执行表格里从用例2到最后的用例
caseFrom = 2
caseTo =
或， 表示只执行表格里从用例2到用例50
caseFrom =
caseTo = 50

所有异常取值范围都表示执行所有用例
caseFrom = 0
caseTo = 0
或
caseFrom = 0
caseTo = -2
或
caseFrom = 36
caseTo = 2
或
caseFrom = 300     //如表格里只有100条用例，起始编号超出用例数量
caseTo = 2000

===========================================================================

【新质控自动化说明之执行脚本】
test.py   //依据配置文件config.ini执行表格里用例
testOk.py  //执行表格里测试结果为ok的用例
testError.py  //执行表格里测试结果为error的用例
testAll.py  //执行表格里所有用例




