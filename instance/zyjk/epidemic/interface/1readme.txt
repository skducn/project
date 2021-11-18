脚本执行流程

1，run.py
2，xls.getCaseParam()  //遍历获取 名称、路径、方法、参数、检查key、检查value、全局变量
3，xls.result(excelNo, iName, iPath, iMethod, iParam, iKey, iValue, d_globalVar)  // 替换参数，解析接口，检查iKey、iValue
4，reflection.run([iName, iPath, iMethod, iParam, globalVar])
	iDriven.py
5，setCaseParam(excelNo, result, d_res)  # 更新表格数据

=====================================================

文档结构：
1，配置文件 config.ini  
2，调用配置文件 readConfig.py
3，测试用例表格 testcase.xlsx
4，接口驱动 iDriven.py , reflection.py
5，表格处理文件 xls.py
6，执行文件 run.py
