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
from PO.ColorPO import *
Color_PO = ColorPO()

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS")  # 测试环境
from PO.OraclePO import *
Oracle_PO = OraclePO("SUNWENBO", "Sunwenbo1204", "192.168.0.235:1521", "ORCL")

import sys

def main(var_s_table, var_o_table, var_s_sql, var_o_sql):

    # 获取sqlserver表注释
    d_s_table = {}
    # print(Sqlserver_PO.getTableComment(var_s_table))  # {'T_CHILD_INFO': '儿童健康档案登记表'}
    if Sqlserver_PO.getTableComment(var_s_table) == {}:
        d_s_table[var_s_table] = 'None'
    else:
        d_s_table[var_s_table] = Sqlserver_PO.getTableComment(var_s_table)[var_s_table]
        # print(Sqlserver_PO.getTableComment(var_s_table)[var_s_table])  # '儿童健康档案登记表'

    # 获取oracle表注释
    d_o_table = {}
    l_t_o_comments = Oracle_PO.execQueryParam("select COMMENTS  from all_tab_comments where Table_Name=:tableName  and owner = 'DIP'", {"tableName": var_o_table})
    # print(l_t_o_comments[0][0])  # GW-31006 糖尿病随访服药信息
    if l_t_o_comments[0][0] == "":
        d_o_table[var_o_table] = 'None'
    else:
        d_o_table[var_o_table] = l_t_o_comments[0][0]

    d_s_table = Sqlserver_PO.getTableComment(var_s_table)
    print(("测试库(" + str(d_s_table) + ") - 比对库(" + str(d_o_table) + ")").center(100, "-"))


    # todo sqlserver表（字段：注释）
    d_s_comment = Sqlserver_PO.getFieldComment(var_s_table)
    # print('d_s_comment = ', d_s_comment)  # {'ID': '主键', 'IDCARD': '身份证号', 'EHR_NUM': '档案编号',...
    # todo sqlserver表（字段：类型）
    d_s_type = Sqlserver_PO.getFieldAndType(var_s_table)
    # print('d_s_type = ', d_s_type)  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char', 'SALARY': 'float' ...
    # todo sqlserver表（字段：值）
    l_temp = Sqlserver_PO.execQuery(var_s_sql)
    # print(var_s_sql)
    # print(l_temp)
    d_s_value = l_temp[0]
    # print('d_s_value = ', d_s_value)  # {'ID': 75, 'IDCARD': '110101199003071234', 'EHR_NUM': '11011600100100005'...



    # todo oracle表（字段：注释）序号乱
    l_t_o_comment = Oracle_PO.execQueryParam("select COLUMN_NAME, COMMENTS from all_col_comments where Table_Name= :tableName order by table_name", {"tableName": var_o_table})
    d_o_comment = dict(l_t_o_comment)
    # print("d_o_comment = ", d_o_comment)  # {'JKKH': '健康卡号', 'ZJHM': '证件号码',
    #todo oracle表（字段：编号）
    l_t_o_no = Oracle_PO.execQueryParam("SELECT column_name,column_id from all_tab_columns a where table_name= :tableName AND OWNER='DIP' order by column_id", {"tableName": var_o_table})
    d_o_no = dict(l_t_o_no)
    # print("d_o_no = ", d_o_no)  # {'YLJGDM': 1, 'GRDAID': 2, 'BZFLX': 3,
    # todo oracle表（字段：注释）序号正确
    for k1, v1 in d_o_comment.items():
        for k, v in d_o_no.items():
            if k == k1:
                d_o_no[k] = v1
    d_o_comment = d_o_no
    # print("d_o_comment = ", d_o_comment)  # {'YLJGDM': 1, 'GRDAID': 2, 'BZFLX': 3,

    # todo oracle表（字段：类型）
    # 获取表信息
    # l_t_field_oracle = Oracle_PO.execQuery("select * from all_tab_cols where table_name='TB_CHSS_INFO'")
    l_t_o_type = Oracle_PO.execQueryParam(
        "select a.column_name, a.DATA_TYPE from all_tab_columns a where table_name= :tableName AND OWNER='DIP' order by column_id",
        {"tableName": var_o_table})
    # l_t_field_oracle = Oracle_PO.execQuery("select a.column_name from all_tab_columns a where table_name='TB_CHSS_INFO' AND OWNER='DIP' order by table_name,column_id")
    # print(l_t_o_type)  # [('YLJGDM', 'VARCHAR2'), ('GRDAID', 'VARCHAR2'),...
    d_o_type = dict(l_t_o_type)
    # print('d_o_type = ', d_o_type)  # {'YLJGDM': 'VARCHAR2', 'GRDAID': 'VARCHAR2', ...

    # todo sqlserver表（字段：值）
    d_oracle = {}
    l_d_oracle = []
    # todo oracle表（值）
    # Oracle_PO.execQuery(sql_oracle)  # [('10', '7566', '1', '-1', '1', '居民身份证', '340823199303196117',...
    # print(Oracle_PO.execQuery(var_o_sql))
    for r in Oracle_PO.execQuery(var_o_sql):
        for i in range(len(l_t_o_type)):
            # print(l_t_o_type[i], r[i])
            d_oracle[l_t_o_type[i][0]] = r[i]
        l_d_oracle.append(d_oracle)
        d_oracle = {}
    # print(l_d_oracle[0])
    d_o_value = l_d_oracle[0]
    # print('d_o_value = ', d_o_value)  # {'YLJGDM': '123456', 'GRDAID': '11011600100100005', ...


    # todo 省平台上报字段对应表（比对）
    l_d_row = Sqlserver_PO.execQuery("select * from a_upload")
    # print("l_d_row", l_d_row)  # [{'s_value': None, 'o_value': None, 's_field': None, 'o_field': None, 's_comment': None, 'o_comment': None, 's_type': None, 'o_type': None, 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'y', 'tester': '郭斐', 's_sql': "SELECT * FROM T_CHILD_INFO where id='1189'", 'o_sql': "SELECT * FROM DIP.TB_EB_ETJBQK where ETBSFID='1189'"}, {'s_value': '1189', 'o_value': '1189', 's_field': 'ID', 'o_field': 'ETBSFID', 's_comment': '主键', 'o_comment': 'None', 's_type': 'int', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '111', 'o_value': '111', 's_field': 'CREATE_ORG_CODE', 'o_field': 'YLJGDM', 's_comment': '创建机构代码', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '马德勇', 'o_value': '马德勇', 's_field': 'NAME', 'o_field': 'XM', 's_comment': '姓名', 'o_comment': 'None', 's_type': 'nvarchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '1', 'o_value': '1', 's_field': 'SEX_CODE', 'o_field': 'XBDM', 's_comment': '性别代码', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'CHAR', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '220621199012163357', 'o_value': '220621199012163357', 's_field': 'IDCARD', 'o_field': 'ZJHM', 's_comment': '身份证', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '测试', 'o_value': '测试', 's_field': 'MOTHER_NAME', 'o_field': 'MQXM', 's_comment': '母亲姓名', 'o_comment': 'None', 's_type': 'nvarchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '222222222222222222', 'o_value': '222222222222222222', 's_field': 'MOTHER_IDCARD', 'o_field': 'MQSFZ_HM', 's_comment': '母亲身份证号', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '370685001001', 'o_value': '370685001001', 's_field': 'PRESENT_VILLAGE_CODE', 'o_field': 'XZDZ_JWBM', 's_comment': '现住址-居委编码', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '文化区社区居民委员会', 'o_value': '文化区社区居民委员会', 's_field': 'PRESENT_VILLAGE_NAME', 'o_field': 'XZDZ_JW', 's_comment': '现住址-居委', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '2024-01-06 00:00:00', 'o_value': '2024-01-06 00:00:00', 's_field': 'BIRTH', 'o_field': 'CSRQSJ', 's_comment': '出生日期', 'o_comment': 'None', 's_type': 'datetime', 'o_type': 'DATE', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}]


    for r, index in enumerate(l_d_row):
        if l_d_row[r]['s_table'] == var_s_table and l_d_row[r]['o_table'] == var_o_table and l_d_row[r]['s_sql'] == None:
            # print(r+1, ['s'], d_s_value[l_d_row[r]['s_field']])
            # print(r+1, ['o'], d_o_value[l_d_row[r]['o_field']])
            if str(d_s_value[l_d_row[r]['s_field']]) == str(d_o_value[l_d_row[r]['o_field']]):
                Sqlserver_PO.execute("update a_upload set result='ok' where s_field='%s' and o_field='%s' and s_table='%s' and o_table='%s'" % (l_d_row[r]['s_field'], l_d_row[r]['o_field'], var_s_table, var_o_table))
            else:
                # print(r+1, "[error] => ", l_d_row[r]['s_field'] + "(" + d_s_type[l_d_row[r]['s_field']] + ") = " + str(d_s_value[l_d_row[r]['s_field']]) + ", " + l_d_row[r]['o_field'] + "(" + d_o_type[l_d_row[r]['o_field']] + ") = " + str(d_o_value[l_d_row[r]['o_field']]))
                Color_PO.consoleColor("31", "31", str(r+1) + " [ERROR], " + var_s_table + "." + d_s_type[l_d_row[r]['s_field']] + "." + d_s_comment[l_d_row[r]['s_field']] + ".(" + l_d_row[r]['s_field'] + " = " + str(d_s_value[l_d_row[r]['s_field']]) + ")"
                                      + ", " + var_o_table + "." + d_o_type[l_d_row[r]['o_field']] + ".(" + l_d_row[r]['o_field'] + " = " + str(d_o_value[l_d_row[r]['o_field']]) + ")", "")
                Sqlserver_PO.execute("update a_upload set result='error' where s_field='%s' and o_field='%s' and s_table='%s' and o_table='%s'" % (l_d_row[r]['s_field'], l_d_row[r]['o_field'], var_s_table, var_o_table))

            Sqlserver_PO.execute("update a_upload set s_comment='%s' where s_table='%s'" % (d_s_table[var_s_table], var_s_table))
            Sqlserver_PO.execute("update a_upload set s_type='%s' where s_field='%s' and s_table='%s' and o_table='%s'" % (d_s_type[l_d_row[r]['s_field']], l_d_row[r]['s_field'], var_s_table, var_o_table))
            Sqlserver_PO.execute("update a_upload set s_value='%s' where s_field='%s' and o_field='%s' and s_table='%s' and o_table='%s'" % (d_s_value[l_d_row[r]['s_field']], l_d_row[r]['s_field'], l_d_row[r]['o_field'], var_s_table, var_o_table))

            Sqlserver_PO.execute("update a_upload set o_comment='%s' where o_table='%s'" % (d_o_table[var_o_table], var_o_table))
            Sqlserver_PO.execute("update a_upload set o_type='%s' where s_field='%s' and s_table='%s' and o_table='%s'" % (d_o_type[l_d_row[r]['o_field']], l_d_row[r]['s_field'], var_s_table, var_o_table))
            Sqlserver_PO.execute("update a_upload set o_value='%s' where s_field='%s' and o_field='%s' and s_table='%s' and o_table='%s'" % (d_o_value[l_d_row[r]['o_field']], l_d_row[r]['s_field'], l_d_row[r]['o_field'],  var_s_table, var_o_table))



# todo 省平台上报字段对应表（新建upload表）

def insertTbl(sheetName, tableName):
    Sqlserver_PO.execute("drop table " + tableName)
    Sqlserver_PO.xlsx2db('upload.xlsx', tableName, sheetName)
    Sqlserver_PO.execute("ALTER table %s alter column s_value varchar(111)" % (tableName))  # 修改字段类型
    Sqlserver_PO.execute("ALTER table %s alter column o_value varchar(111)" % (tableName))  # 修改字段类型
    Sqlserver_PO.execute("ALTER table %s alter column s_comment varchar(111)" % (tableName))  # 修改字段类型
    Sqlserver_PO.execute("ALTER table %s alter column o_comment varchar(111)" % (tableName))  # 修改字段类型
    Sqlserver_PO.execute("ALTER table %s alter column s_type varchar(111)" % (tableName))  # 修改字段类型
    Sqlserver_PO.execute("ALTER table %s alter column o_type varchar(111)" % (tableName))  # 修改字段类型
    Sqlserver_PO.execute("ALTER table %s alter column s_tc varchar(111)" % (tableName))  # 修改字段类型
    Sqlserver_PO.execute("ALTER table %s alter column o_tc varchar(111)" % (tableName))  # 修改字段类型
    Sqlserver_PO.execute("ALTER table %s alter column result varchar(111)" % (tableName))  # 修改字段类型

    Sqlserver_PO.execute(
        "EXECUTE sp_addextendedproperty N'MS_Description', N'%s', N'user', N'dbo', N'table', N'%s', NULL, NULL" % (
            sheetName, tableName))  # sheetName=注释，tableName=表名


# todo 1, 导入数据库
insertTbl('省平台上报字段对应表', 'a_upload')

# todo 2，从库中获取sql行数据
l_row = Sqlserver_PO.execQuery("select s_table,o_table,s_sql,o_sql from a_upload where result ='y'")
for i in range(len(l_row)):
    # 3，todo 执行比对
    main(l_row[i]['s_table'], l_row[i]['o_table'], l_row[i]['s_sql'], l_row[i]['o_sql'])

# do to others as you would have them do to you