�ű�ִ������

1��run.py
2��xls.getCaseParam()  //������ȡ ���ơ�·�������������������key�����value��ȫ�ֱ���
3��xls.result(excelNo, iName, iPath, iMethod, iParam, iKey, iValue, d_globalVar)  // �滻�����������ӿڣ����iKey��iValue
4��reflection.run([iName, iPath, iMethod, iParam, globalVar])
	iDriven.py
5��setCaseParam(excelNo, result, d_res)  # ���±������

=====================================================

�ĵ��ṹ��
1�������ļ� config.ini  
2�����������ļ� readConfig.py
3������������� testcase.xlsx
4���ӿ����� iDriven.py , reflection.py
5��������ļ� xls.py
6��ִ���ļ� run.py
