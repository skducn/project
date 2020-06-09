1.启动jar包，cmd 输入java -jar （jar包）
2.清除HrRuleRecord表数据       DELETE HrRuleRecord
2.数据库数据自造    update
3.执行质控 访问接口http://localhost:8080/healthRecordRules/rulesApi/execute/档案编号
4查看质控结果 SELECT t2.Comment,t2.Categories, t2.RuleSql FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId