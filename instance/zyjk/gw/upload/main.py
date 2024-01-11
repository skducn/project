# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-1-10
# Description: 公卫 - 省平台数据上报
# 警告如下：D:\dwp_backup\python study\GUI_wxpython\lib\site-packages\openpyxl\worksheet\_reader.py:312: UserWarning: Unknown extension is not supported and will be removed warn(msg)
# 解决方法：
import warnings
warnings.simplefilter("ignore")
# *****************************************************************

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS")  # 测试环境
from PO.OraclePO import *
Oracle_PO = OraclePO("SUNWENBO", "Sunwenbo1204", "192.168.0.235:1521", "ORCL")

import sys

def main(sqlTableName, oracleTableName, sql_sqlserver, sql_oracle):


    # todo sqlserver表（字段：注释）
    d_fieldComment_sqlserver = Sqlserver_PO.getFieldComment(sqlTableName)
    print('d_fieldComment_sqlserver = ', d_fieldComment_sqlserver)  # {'ID': '主键', 'IDCARD': '身份证号', 'EHR_NUM': '档案编号',...
    # todo sqlserver表（字段：类型）
    d_fieldType_sqlserver = Sqlserver_PO.getFieldAndType(sqlTableName)
    print('d_fieldType_sqlserver = ', d_fieldType_sqlserver)  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char', 'SALARY': 'float' ...
    # todo sqlserver表（字段：值）
    l_d_sqlserver = Sqlserver_PO.execQuery(sql_sqlserver)
    d_fieldValue_sqlserver = l_d_sqlserver[0]
    print('d_fieldValue_sqlserver = ', d_fieldValue_sqlserver)  # {'ID': 75, 'IDCARD': '110101199003071234', 'EHR_NUM': '11011600100100005'...



    # todo oracle表（字段：注释）序号乱
    l_t_fieldComment_oracle = Oracle_PO.execQueryParam("select COLUMN_NAME, COMMENTS from all_col_comments where Table_Name= :tableName order by table_name", {"tableName": oracleTableName})
    d_fieldComment_oracle = dict(l_t_fieldComment_oracle)
    print("d_fieldComment_oracle = ", d_fieldComment_oracle)  # {'JKKH': '健康卡号', 'ZJHM': '证件号码',
    #todo oracle表（字段：编号）
    l_t_fieldNo_oracle = Oracle_PO.execQueryParam("SELECT column_name,column_id from all_tab_columns a where table_name= :tableName AND OWNER='DIP' order by column_id", {"tableName": oracleTableName})
    d_fieldNo_oracle = dict(l_t_fieldNo_oracle)
    print("d_fieldNo_oracle = ", d_fieldNo_oracle)  # {'YLJGDM': 1, 'GRDAID': 2, 'BZFLX': 3,
    # todo oracle表（字段：注释）序号正确
    for k1, v1 in d_fieldComment_oracle.items():
        for k, v in d_fieldNo_oracle.items():
            if k == k1:
                d_fieldNo_oracle[k] = v1
    d_fieldComment_oracle = d_fieldNo_oracle
    print("d_fieldComment_oracle = ", d_fieldComment_oracle)  # {'YLJGDM': 1, 'GRDAID': 2, 'BZFLX': 3,

    # todo oracle表（字段：类型）
    # 获取表信息
    # l_t_field_oracle = Oracle_PO.execQuery("select * from all_tab_cols where table_name='TB_CHSS_INFO'")
    l_t_fieldType_oracle = Oracle_PO.execQueryParam(
        "select a.column_name, a.DATA_TYPE from all_tab_columns a where table_name= :tableName AND OWNER='DIP' order by column_id",
        {"tableName": oracleTableName})
    # l_t_field_oracle = Oracle_PO.execQuery("select a.column_name from all_tab_columns a where table_name='TB_CHSS_INFO' AND OWNER='DIP' order by table_name,column_id")
    # print(l_t_fieldType_oracle)  # [('YLJGDM', 'VARCHAR2'), ('GRDAID', 'VARCHAR2'),...
    d_fieldType_oracle = dict(l_t_fieldType_oracle)
    print('d_fieldType_oracle = ', d_fieldType_oracle)  # {'YLJGDM': 'VARCHAR2', 'GRDAID': 'VARCHAR2', ...

    # todo sqlserver表（字段：值）
    d_oracle = {}
    l_d_oracle = []
    # todo oracle表（值）
    # Oracle_PO.execQuery(sql_oracle)  # [('10', '7566', '1', '-1', '1', '居民身份证', '340823199303196117',...
    # print(len(Oracle_PO.execQuery(sql_oracle)))
    for r in Oracle_PO.execQuery(sql_oracle):
        for i in range(len(l_t_fieldType_oracle)):
            # print(l_t_fieldType_oracle[i], r[i])
            d_oracle[l_t_fieldType_oracle[i][0]] = r[i]
        l_d_oracle.append(d_oracle)
        d_oracle = {}
    print(d_oracle)
    d_fieldValue_oracle = l_d_oracle[0]
    # print('d_fieldValue_oracle = ', d_fieldValue_oracle)  # {'YLJGDM': '123456', 'GRDAID': '11011600100100005', ...


    # todo 省平台上报字段对应表（比对）
    l_d_row = Sqlserver_PO.execQuery("select * from a_upload")
    # print(l_d_row)  # [{'sqlTableComment': '档案信息表', 'sqlTableName': 'T_EHR_INFO',,...

    for r, index in enumerate(l_d_row):
        if l_d_row[r]['sqlTableName'] == sqlTableName:
            # print(1,d_fieldValue_sqlserver[l_d_row[r]['sqlField']])
            # print(2,d_fieldValue_oracle[l_d_row[r]['oracleField']])
            if str(d_fieldValue_sqlserver[l_d_row[r]['sqlField']]) == str(d_fieldValue_oracle[l_d_row[r]['oracleField']]):
                # print("[ok] => ", r['sqlField'] + "=" + r['oracleField'] + "=" + str(d_fieldValue_sqlserver[r['sqlField']]))
                # Sqlserver_PO.execute("update a_upload set sqlValue=%s,oracleValue=%s,result='ok' where sqlField='%s'" % (d_sqlserver0[r['sqlField']], d_oracle0[r['oracleField']], r['sqlField']))
                Sqlserver_PO.execute("update a_upload set result='ok' where sqlField='%s' and oracleTableName='%s'" % (l_d_row[r]['sqlField'], oracleTableName))
            else:
                print(r+1, "[error] => ", l_d_row[r]['sqlField'] + "(" + d_fieldType_sqlserver[l_d_row[r]['sqlField']] + ") = " + str(d_fieldValue_sqlserver[l_d_row[r]['sqlField']]) + ", " + l_d_row[r]['oracleField'] + "(" + d_fieldType_oracle[l_d_row[r]['oracleField']] + ") = " + str(d_fieldValue_oracle[l_d_row[r]['oracleField']]))
                Sqlserver_PO.execute("update a_upload set result='error' where sqlField='%s' and oracleTableName='%s'" % (l_d_row[r]['sqlField'], oracleTableName))

            Sqlserver_PO.execute("update a_upload set sqlComment='%s' where sqlField='%s' and sqlTableName='%s' and oracleTableName='%s'" % (d_fieldComment_sqlserver[l_d_row[r]['sqlField']], l_d_row[r]['sqlField'], sqlTableName, oracleTableName))
            Sqlserver_PO.execute("update a_upload set sqlType='%s' where sqlField='%s' and sqlTableName='%s' and oracleTableName='%s'" % (d_fieldType_sqlserver[l_d_row[r]['sqlField']], l_d_row[r]['sqlField'], sqlTableName, oracleTableName))
            Sqlserver_PO.execute("update a_upload set sqlValue='%s' where sqlField='%s' and sqlTableName='%s' and oracleTableName='%s'" % (d_fieldValue_sqlserver[l_d_row[r]['sqlField']], l_d_row[r]['sqlField'], sqlTableName, oracleTableName))

            Sqlserver_PO.execute("update a_upload set oracleComment='%s' where sqlField='%s' and sqlTableName='%s' and oracleTableName='%s'" % (d_fieldComment_oracle[l_d_row[r]['oracleField']], l_d_row[r]['sqlField'], sqlTableName, oracleTableName))
            Sqlserver_PO.execute("update a_upload set oracleType='%s' where sqlField='%s' and sqlTableName='%s' and oracleTableName='%s'" % (d_fieldType_oracle[l_d_row[r]['oracleField']], l_d_row[r]['sqlField'], sqlTableName, oracleTableName))
            Sqlserver_PO.execute("update a_upload set oracleValue='%s' where sqlField='%s' and sqlTableName='%s' and oracleTableName='%s'" % (d_fieldValue_oracle[l_d_row[r]['oracleField']], l_d_row[r]['sqlField'], sqlTableName, oracleTableName))



# todo 省平台上报字段对应表（新建upload表）

def insertTbl(sheetName, tableName):
    Sqlserver_PO.execute("drop table " + tableName)
    Sqlserver_PO.xlsx2db('upload.xlsx', tableName, sheetName)
    Sqlserver_PO.execute("ALTER table %s alter column sqlComment varchar(111)" % (tableName))  # 修改字段类型
    Sqlserver_PO.execute("ALTER table %s alter column sqlValue varchar(111)" % (tableName))  # 修改字段类型
    Sqlserver_PO.execute("ALTER table %s alter column sqlType varchar(111)" % (tableName))  # 修改字段类型

    Sqlserver_PO.execute("ALTER table %s alter column oracleComment varchar(111)" % (tableName))  # 修改字段类型
    Sqlserver_PO.execute("ALTER table %s alter column oracleType varchar(111)" % (tableName))  # 修改字段类型
    Sqlserver_PO.execute("ALTER table %s alter column oracleValue varchar(111)" % (tableName))  # 修改字段类型

    Sqlserver_PO.execute("ALTER table %s alter column result varchar(111)" % (tableName))  # 修改字段类型
    Sqlserver_PO.execute("ALTER table %s alter column memo varchar(111)" % (tableName))  # 修改字段类型


    Sqlserver_PO.execute(
        "EXECUTE sp_addextendedproperty N'MS_Description', N'%s', N'user', N'dbo', N'table', N'%s', NULL, NULL" % (
            sheetName, tableName))  # sheetName=注释，tableName=表名
# insertTbl('省平台上报字段对应表', 'a_upload')

# 档案信息表
# main("T_EHR_INFO", "TB_CHSS_INFO", "SELECT * FROM T_EHR_INFO where IDCARD='110101199003071234'", "SELECT * FROM DIP.TB_CHSS_INFO where ZJHM='110101199003071234'")
#
# # 糖尿病患者报病卡
# main("TB_TNB_HZBBK", "TB_TNB_HZBBK", "SELECT * FROM TB_TNB_HZBBK where BKBH='1' AND YLJGDM='xxfs'", "SELECT * FROM DIP.TB_TNB_HZBBK where BKBH='1' AND YLJGDM='xxfs'")

# 糖尿病患者管理卡
# main("TB_TNB_HZGLK", "TB_TNB_HZGLK", "SELECT * FROM TB_TNB_HZGLK where YLJGDM='1231' AND GLKBH='1234'", "SELECT * FROM DIP.TB_TNB_HZGLK where YLJGDM='1231' AND GLKBH='1234'")

# 儿童健康档案登记表
# main("T_CHILD_INFO", "TB_EB_ETJBQK", "SELECT * FROM T_CHILD_INFO where id='1189'", "SELECT * FROM DIP.TB_EB_ETJBQK where ETBSFID='1189'")

# 儿童家庭访视记录表
# main("T_CHILD_HOME_VISIT", "TB_EB_ETJBQK", "SELECT * FROM T_CHILD_HOME_VISIT where INFO_ID='1189'", "SELECT * FROM DIP.TB_EB_ETJBQK where ETBSFID='1189'")

# 个人健康档案首页表
main("T_EHR_GRJKDA", "TB_CHSS_GRJKDA", "SELECT * FROM T_EHR_GRJKDA where zjhm='110101199003071234'", "SELECT * FROM DIP.TB_CHSS_GRJKDA where ZJHM='110101199003071234'")

# 糖尿病患者随访卡
# main("TB_TNB_HZSFK", "TB_TNB_HZSFK", "SELECT * FROM TB_TNB_HZSFK where YLJGDM='1234' AND SFJLID='1234'", "SELECT * FROM DIP.TB_TNB_HZSFK where YLJGDM='1234' AND SFJLID='1234'")

# # 儿童健康档案登记表 ??
# main("T_CHILD_INFO", "TB_EB_ETTGJCJL", "SELECT * FROM T_CHILD_INFO where id='1189'", "SELECT * FROM DIP.TB_EB_ETTGJCJL where TJDJBDH='1189' and TGJCJLBH='1101'")
# main("T_CHILD_EXAMINATION", "TB_EB_ETTGJCJL", "SELECT * FROM T_CHILD_EXAMINATION where id='1101'", "SELECT * FROM DIP.TB_EB_ETTGJCJL where TGJCJLBH='1101' and YLJGDM = '111'")