1.����jar����cmd ����java -jar ��jar����
2.���HrRuleRecord������       DELETE HrRuleRecord
2.���ݿ���������    update
3.ִ���ʿ� ���ʽӿ�http://localhost:8080/healthRecordRules/rulesApi/execute/�������
4�鿴�ʿؽ�� SELECT t2.Comment,t2.Categories, t2.RuleSql FROM HrRuleRecord t1 JOIN HrRule t2 ON t1.RuleId=t2.RuleId