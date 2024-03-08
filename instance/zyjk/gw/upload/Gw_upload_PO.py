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

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB_SQL("host"), Configparser_PO.DB_SQL("user"), Configparser_PO.DB_SQL("password"), Configparser_PO.DB_SQL("database"))  # 测试环境
from PO.OraclePO import *
Oracle_PO = OraclePO(Configparser_PO.DB_ORACLE("host"), Configparser_PO.DB_ORACLE("user"), Configparser_PO.DB_ORACLE("password"), Configparser_PO.DB_ORACLE("database"))  # 测试环境


class Gw_upload_PO():

    def __init__(self):

        self.dbTable = Configparser_PO.DB_SQL("table")

    def main(self, var_s_table, var_o_table, var_s_sql, var_o_sql):

        # 执行省平台上报字段对应表

        # 获取sqlserver表注释
        d_s_table = {}
        # print(Sqlserver_PO.getTableComment(var_s_table))  # {'T_CHILD_INFO': '儿童健康档案登记表'}
        if Sqlserver_PO.getTableAndComment(var_s_table) == {}:
            d_s_table[var_s_table] = 'None'
        else:
            d_s_table[var_s_table] = Sqlserver_PO.getTableAndComment(var_s_table)[var_s_table]
            # print(Sqlserver_PO.getTableComment(var_s_table)[var_s_table])  # '儿童健康档案登记表'

        # 获取oracle表注释
        d_o_table = {}
        l_t_o_comments = Oracle_PO.execQueryParam("select COMMENTS  from all_tab_comments where Table_Name=:tableName  and owner = 'DIP'", {"tableName": var_o_table})
        # print(l_t_o_comments[0][0])  # GW-31006 糖尿病随访服药信息
        # print(l_t_o_comments)
        if l_t_o_comments[0][0] == "":
            d_o_table[var_o_table] = 'None'
        else:
            d_o_table[var_o_table] = l_t_o_comments[0][0]


        # print(("测试库(" + str(d_s_table) + ") - 比对库(" + str(d_o_table) + ")").center(100, "-"))


        # todo sqlserver表（字段：注释）
        d_s_comment = Sqlserver_PO.getFieldAndComment(var_s_table)
        # print('d_s_comment = ', d_s_comment)  # {'ID': '主键', 'IDCARD': '身份证号', 'EHR_NUM': '档案编号',...
        # todo sqlserver表（字段：类型）
        d_s_type = Sqlserver_PO.getFieldsAndTypes(var_s_table)
        # print('d_s_type = ', d_s_type)  # {'ID': 'int', 'NAME': 'text', 'AGE': 'int', 'ADDRESS': 'char', 'SALARY': 'float' ...
        # todo sqlserver表（字段：值）
        l_temp = Sqlserver_PO.select(var_s_sql)
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
        # l_t_field_oracle = Oracle_PO.select("select a.column_name from all_tab_columns a where table_name='TB_CHSS_INFO' AND OWNER='DIP' order by table_name,column_id")
        # print(l_t_o_type)  # [('YLJGDM', 'VARCHAR2'), ('GRDAID', 'VARCHAR2'),...
        d_o_type = dict(l_t_o_type)
        # print('d_o_type = ', d_o_type)  # {'YLJGDM': 'VARCHAR2', 'GRDAID': 'VARCHAR2', ...

        # todo sqlserver表（字段：值）
        d_oracle = {}
        l_d_oracle = []
        # todo oracle表（值）
        # Oracle_PO.select(sql_oracle)  # [('10', '7566', '1', '-1', '1', '居民身份证', '340823199303196117',...
        # print(Oracle_PO.select(var_o_sql))
        for r in Oracle_PO.select(var_o_sql):
            for i in range(len(l_t_o_type)):
                # print(l_t_o_type[i], r[i])
                d_oracle[l_t_o_type[i][0]] = r[i]
            l_d_oracle.append(d_oracle)
            d_oracle = {}
        # print(l_d_oracle[0])
        d_o_value = l_d_oracle[0]
        # print('d_o_value = ', d_o_value)  # {'YLJGDM': '123456', 'GRDAID': '11011600100100005', ...


        # todo 省平台上报字段对应表（比对）
        l_d_row = Sqlserver_PO.select("select * from %s" % (self.dbTable))
        # print("l_d_row", l_d_row)  # [{'s_value': None, 'o_value': None, 's_field': None, 'o_field': None, 's_comment': None, 'o_comment': None, 's_type': None, 'o_type': None, 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'y', 'tester': '郭斐', 's_sql': "SELECT * FROM T_CHILD_INFO where id='1189'", 'o_sql': "SELECT * FROM DIP.TB_EB_ETJBQK where ETBSFID='1189'"}, {'s_value': '1189', 'o_value': '1189', 's_field': 'ID', 'o_field': 'ETBSFID', 's_comment': '主键', 'o_comment': 'None', 's_type': 'int', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '111', 'o_value': '111', 's_field': 'CREATE_ORG_CODE', 'o_field': 'YLJGDM', 's_comment': '创建机构代码', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '马德勇', 'o_value': '马德勇', 's_field': 'NAME', 'o_field': 'XM', 's_comment': '姓名', 'o_comment': 'None', 's_type': 'nvarchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '1', 'o_value': '1', 's_field': 'SEX_CODE', 'o_field': 'XBDM', 's_comment': '性别代码', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'CHAR', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '220621199012163357', 'o_value': '220621199012163357', 's_field': 'IDCARD', 'o_field': 'ZJHM', 's_comment': '身份证', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '测试', 'o_value': '测试', 's_field': 'MOTHER_NAME', 'o_field': 'MQXM', 's_comment': '母亲姓名', 'o_comment': 'None', 's_type': 'nvarchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '222222222222222222', 'o_value': '222222222222222222', 's_field': 'MOTHER_IDCARD', 'o_field': 'MQSFZ_HM', 's_comment': '母亲身份证号', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '370685001001', 'o_value': '370685001001', 's_field': 'PRESENT_VILLAGE_CODE', 'o_field': 'XZDZ_JWBM', 's_comment': '现住址-居委编码', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '文化区社区居民委员会', 'o_value': '文化区社区居民委员会', 's_field': 'PRESENT_VILLAGE_NAME', 'o_field': 'XZDZ_JW', 's_comment': '现住址-居委', 'o_comment': 'None', 's_type': 'varchar', 'o_type': 'VARCHAR2', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}, {'s_value': '2024-01-06 00:00:00', 'o_value': '2024-01-06 00:00:00', 's_field': 'BIRTH', 'o_field': 'CSRQSJ', 's_comment': '出生日期', 'o_comment': 'None', 's_type': 'datetime', 'o_type': 'DATE', 's_table': 'T_CHILD_INFO', 'o_table': 'TB_EB_ETJBQK', 's_tc': None, 'o_tc': None, 'result': 'ok', 'tester': '郭斐', 's_sql': None, 'o_sql': None}]

        for r, index in enumerate(l_d_row):

            if l_d_row[r]['s_table'] == var_s_table and l_d_row[r]['o_table'] == var_o_table and l_d_row[r]['s_sql'] == None:
                # if l_d_row[r]['s_field'] == None:
                #     print(r + 1, ("测试库(" + str(d_s_table) + ") - 比对库(" + str(d_o_table) + ")").center(100, "-"))
                # print(r+2, ['s'], d_s_value[l_d_row[r]['s_field']])
                # print(r+2, ['o'], d_o_value[l_d_row[r]['o_field']])
                if str(d_s_value[l_d_row[r]['s_field']]) == str(d_o_value[l_d_row[r]['o_field']]):
                    Sqlserver_PO.execute("update %s set result='ok' where s_field='%s' and o_field='%s' and s_table='%s' and o_table='%s'" % (self.dbTable, l_d_row[r]['s_field'], l_d_row[r]['o_field'], var_s_table, var_o_table))
                else:
                    # print(r+1, "[error] => ", l_d_row[r]['s_field'] + "(" + d_s_type[l_d_row[r]['s_field']] + ") = " + str(d_s_value[l_d_row[r]['s_field']]) + ", " + l_d_row[r]['o_field'] + "(" + d_o_type[l_d_row[r]['o_field']] + ") = " + str(d_o_value[l_d_row[r]['o_field']]))
                    # Color_PO.consoleColor("31", "31", str(r+1) + " ERR, SQL => " + str(d_s_table[var_s_table]) + "." + d_s_comment[l_d_row[r]['s_field']] + "(" + d_s_type[l_d_row[r]['s_field']] + ") " + var_s_table + "." + l_d_row[r]['s_field'] + " = " + str(d_s_value[l_d_row[r]['s_field']]) , "")
                    Color_PO.consoleColor2({"31": str(r+1) + " ERR", "38": "SQL => " + str(d_s_table[var_s_table]) + "." + d_s_comment[l_d_row[r]['s_field']] + "(" + d_s_type[l_d_row[r]['s_field']] + ") " + var_s_table + ".", "36": l_d_row[r]['s_field'] + " = " + str(d_s_value[l_d_row[r]['s_field']]), "39": ", ORACLE => " + str(d_o_table[var_o_table]) + "." + d_o_comment[l_d_row[r]['o_field']] + "(" + d_o_type[l_d_row[r]['o_field']] + ") " + var_o_table + ".", "35": l_d_row[r]['o_field'] + " = " + str(d_o_value[l_d_row[r]['o_field']])})

                    # 10 ERROR, SQL => 健康教育活动记录表.活动日期(date) T_ACTIVITY_RECORD.ACTIVITY_DATE = 2024-01-11,
                    # ORACLE => GW-30701 健康教育活动记录表.HDSJ(TB_JKJY_HDJLB.DATE.(HDSJ = 2024-01-11 00:00:00))

                    Sqlserver_PO.execute("update %s set result='error' where s_field='%s' and o_field='%s' and s_table='%s' and o_table='%s'" % (self.dbTable, l_d_row[r]['s_field'], l_d_row[r]['o_field'], var_s_table, var_o_table))

                Sqlserver_PO.execute("update %s set s_comment='%s' where s_table='%s'" % (self.dbTable, d_s_table[var_s_table], var_s_table))
                Sqlserver_PO.execute("update %s set s_type='%s' where s_field='%s' and s_table='%s' and o_table='%s'" % (self.dbTable, d_s_type[l_d_row[r]['s_field']], l_d_row[r]['s_field'], var_s_table, var_o_table))
                Sqlserver_PO.execute("update %s set s_value='%s' where s_field='%s' and o_field='%s' and s_table='%s' and o_table='%s'" % (self.dbTable, d_s_value[l_d_row[r]['s_field']], l_d_row[r]['s_field'], l_d_row[r]['o_field'], var_s_table, var_o_table))

                Sqlserver_PO.execute("update %s set o_comment='%s' where o_table='%s'" % (self.dbTable, d_o_table[var_o_table], var_o_table))
                Sqlserver_PO.execute("update %s set o_type='%s' where s_field='%s' and s_table='%s' and o_table='%s'" % (self.dbTable, d_o_type[l_d_row[r]['o_field']], l_d_row[r]['s_field'], var_s_table, var_o_table))
                Sqlserver_PO.execute("update %s set o_value='%s' where s_field='%s' and o_field='%s' and s_table='%s' and o_table='%s'" % (self.dbTable, d_o_value[l_d_row[r]['o_field']], l_d_row[r]['s_field'], l_d_row[r]['o_field'],  var_s_table, var_o_table))

                # 更新时间
                Sqlserver_PO.execute("update %s set updateDate='%s' where s_field != '' " % (self.dbTable, date.today()))

    def excel2db(self, varFile, varSheet):

        # 文件导入db
        # 1, db中删除表
        Sqlserver_PO.execute("drop table if exists " + self.dbTable)

        # 2, excel导入db
        Sqlserver_PO.xlsx2db(varFile, self.dbTable, varSheet)

        # 3, 设置表注释
        Sqlserver_PO.setTableComment(self.dbTable, '(测试用例)公卫上传省平台字段对比')

        # 4, 设置字段类型与描述
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 'result', 'varchar(50)', '结果')
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 'updateDate', 'varchar(100)', '更新时间')
        Sqlserver_PO.execute("ALTER table %s alter column updateDate DATE" % (self.dbTable))  # 注意sqlserver无法将float改为date，先将float改为char，再将char改为data，
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 's_value', 'varchar(555)', 'sql值')
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 'o_value', 'varchar(555)', 'oracle值')
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 's_field', 'varchar(100)', 'sql字段')
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 'o_field', 'varchar(100)', 'oracle字段')
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 's_comment', 'varchar(555)', 'sql注释')
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 'o_comment', 'varchar(555)', 'oracle注释')
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 's_type', 'varchar(100)', 'sql类型')
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 'o_type', 'varchar(100)', 'oracle类型')
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 's_table', 'varchar(100)', 'sql表')
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 'o_table', 'varchar(100)', 'oracle表')
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 's_tc', 'varchar(999)', 'sql表注释')
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 'o_tc', 'varchar(999)', 'oracle表注释')
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 'tester', 'varchar(50)', '测试者')
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 's_sql', 'varchar(999)', 'sql语句')
        Sqlserver_PO.setFieldTypeComment(self.dbTable, 'o_sql', 'varchar(999)', 'oracle语句')

    def run(self):
        l_row = Sqlserver_PO.select("select s_table,o_table,s_sql,o_sql from %s where result ='y'" % (self.dbTable))
        for i in range(len(l_row)):
            self.main(l_row[i]['s_table'], l_row[i]['o_table'], l_row[i]['s_sql'], l_row[i]['o_sql'])




