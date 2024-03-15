# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> >>
# Author     : John
# Created on : 2024-1-19
# Description: 创建表
# 建立学生-课程数据库基本表 https://blog.csdn.net/yangkeOK/article/details/132509470
# 注意：
# 关于使用双精度，sqlServer没有double类型：
# 使用双精度数据，且不固定小数位，用 float
# 使用双精度数据，且固定小数位，用 numric
# 使用双精度数据，且整数和小数都出现，用 real

# 获取日期时间为：年-月-日 时：分：秒， 如：2024-01-30 14:50：12
# select CONVERT(nvarchar(20), getdate(),120) as Sdatetime from a_student;
# 获取日期时间为：年-月-日 时：分， 如：2024-01-30 14:50
# select substring(convert(varchar,getdate(),120),1,16) as Sdatetime from a_student;
# 获取日期时间为：年-月-日 时， 如：2024-01-30 14
# select substring(convert(varchar,getdate(),120),1,13) as Sdatetime from a_student;

# 警告如下：D:\dwp_backup\python study\GUI_wxpython\lib\site-packages\openpyxl\worksheet\_reader.py:312: UserWarning: Unknown extension is not supported and will be removed warn(msg)
# 解决方法：
import warnings
warnings.simplefilter("ignore")
# *****************************************************************
import sys
from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO("192.168.0.234", "sa", "Zy_123456789", "PHUSERS")  # 测试环境
from PO.DataPO import *
Data_PO = DataPO()


def importDb_student(varFile, varTable, varSheet):
    # 学生表 - 修改类型
    Sqlserver_PO.execute("drop table " + varTable)  # 删除表
    Sqlserver_PO.xlsx2db(varFile, varTable, varSheet)  # excel导入db
    Sqlserver_PO.execute("ALTER table %s alter column Sno char(8) not null" % (varTable))  # 学号(不能空，才能设置主键)
    Sqlserver_PO.execute("ALTER table %s add primary key(Sno)" % (varTable))  # 设置学号主键
    Sqlserver_PO.execute("ALTER table %s alter column Sname varchar(20)" % (varTable))  # 姓名
    Sqlserver_PO.execute("ALTER table %s alter column Sage int(3)" % (varTable))  # 年龄
    Sqlserver_PO.execute("ALTER table %s alter column Ssex varchar(5)" % (varTable))  # 性别
    Sqlserver_PO.execute("ALTER table %s alter column Sdept varchar(10)" % (varTable))  # 院系
    Sqlserver_PO.execute("ALTER table %s alter column Sdate DATE" % (varTable))  # 日期   // 注意sqlserver无法将float改为date，先将float改为char，再将char改为data，
    Sqlserver_PO.execute("ALTER table %s alter column Sdatetime datetime" % (varTable))  # 日期+时间   // 注意sqlserver无法将float改为date，先将float改为char，再将char改为data，
    Sqlserver_PO.execute("ALTER table %s alter column Sdatetime2 datetime2" % (varTable))  # 日期+时间   // 注意sqlserver无法将float改为date，先将float改为char，再将char改为data，
    Sqlserver_PO.execute("EXECUTE sp_addextendedproperty N'MS_Description', N'%s', N'user', N'dbo', N'table', N'%s', NULL, NULL" % ("学生表", varTable))  # 修改对象描述（注释）
def importDb_course(varFile, varTable, varSheet):
    # 课程表 -修改类型
    Sqlserver_PO.execute("drop table " + varTable)  # 删除表
    Sqlserver_PO.xlsx2db(varFile, varTable, varSheet)  # excel导入db
    Sqlserver_PO.execute("ALTER table %s alter column Cno char(4) not null" % (varTable))  # 课程号
    Sqlserver_PO.execute("ALTER table %s add primary key(Cno)" % (varTable))  # 设置课程号主键
    Sqlserver_PO.execute("ALTER table %s alter column Cname varchar(50)" % (varTable))  # 课程名
    Sqlserver_PO.execute("ALTER table %s alter column Cpno varchar(20)" % (varTable))  # 先行课
    Sqlserver_PO.execute("ALTER table %s alter column Ccredit float(5)" % (varTable))  # 学分 (sqlserver没有double,使用float后自动转为real（4），精度24)
    Sqlserver_PO.execute("EXECUTE sp_addextendedproperty N'MS_Description', N'%s', N'user', N'dbo', N'table', N'%s', NULL, NULL" % ('课程表', varTable))  # 修改对象描述（注释）
def importDb_sc(varFile, varTable, varStudent, varCourse, varSheet):
    # 选课表 - 修改类型
    Sqlserver_PO.execute("drop table " + varTable)  # 删除表
    Sqlserver_PO.xlsx2db(varFile, varTable, varSheet)  # excel导入db
    Sqlserver_PO.execute("ALTER table %s alter column Sno char(8)" % (varTable))  # 学号
    Sqlserver_PO.execute("ALTER table %s alter column Cno char(4)" % (varTable))  # 课程号
    Sqlserver_PO.execute("ALTER table %s alter column Grade int(3)" % (varTable))  # 成绩
    Sqlserver_PO.execute("ALTER table %s ADD FOREIGN key(Sno) references %s(Sno)" % (varTable, varStudent))
    Sqlserver_PO.execute("ALTER table %s ADD FOREIGN key(Cno) references %s(Cno)" % (varTable, varCourse))
    Sqlserver_PO.execute("EXECUTE sp_addextendedproperty N'MS_Description', N'%s', N'user', N'dbo', N'table', N'%s', NULL, NULL" % ('选课表', varTable))  # 修改对象描述（注释）


def genStudent(varTable):
    Sqlserver_PO.execute("delete from %s" % (varTable))  # 删除记录
    xh_init = 20240101
    for i in range(10):
        l_department = Data_PO.getElement(['数学系', '农业系', '外语系', '体育系'], 1)
        l_sex = Data_PO.getElement(['男', '女'], 1)
        varDate = Data_PO.getDate()  # 随机生成一个日期
        dtime = datetime.datetime.now()  # 2017-09-15 09:41:27.336784
        intTimestamp = time.mktime(dtime.timetuple())  # 1505439687.0
        varDateTime = datetime.datetime.fromtimestamp(intTimestamp)
        sleep(0.1)
        Sqlserver_PO.execute("insert into %s values ('%s','%s',%s,'%s','%s','%s','%s','%s')" % (varTable, xh_init, Data_PO.getChineseName(), Data_PO.getFigures(2), l_sex[0], l_department[0], varDate, varDateTime, varDateTime))
        xh_init = xh_init + 1

def genCourse(varTable):
    Sqlserver_PO.execute("delete from %s" % (varTable))  # 删除记录
    Sqlserver_PO.execute("insert into %s values ('1001','数据库原理及应用', '数据结构', 2)" % (varTable))
    Sqlserver_PO.execute("insert into %s values ('1002','LINUX操作系统与程序设计', '操作系统', 4)" % (varTable))
    Sqlserver_PO.execute("insert into %s values ('1003','离散数学', '高等数学', 2)" % (varTable))
    Sqlserver_PO.execute("insert into %s values ('1004','Java程序设计语言', 'c语言和c++语言', 2)" % (varTable))
    Sqlserver_PO.execute("insert into %s values ('1005','网络安全', '计算机网络', 4)" % (varTable))

def genSc(varTable, varStudent, varCourse):
    Sqlserver_PO.execute("delete from %s" % (varTable))  # 删除记录
    sno = Sqlserver_PO.execQuery("select Sno from %s" % (varStudent))
    # print(sno)  # [{'Sno': '20240101'}, {'Sno': '20240102'},...
    cno = Sqlserver_PO.execQuery("select Cno from %s" % (varCourse))
    # print(cno)  # [{'Cno': '1001 '}, {'Cno': '1002 '}, {'Cno': '1003 '}, {'Cno': '1004 '}, {'Cno': '1005 '}]
    for i in range(len(sno)):
        # print(sno[i]['Sno'])
        for j in range(len(cno)):
            # print(sno[i]['Sno'], cno[j]['Cno'])
            Sqlserver_PO.execute("insert into %s values ('%s','%s', %s)" % (varTable, sno[i]['Sno'], cno[j]['Cno'], Data_PO.getFigures(2)))


# # todo 1, 初始化（删除外键关系）
# fk = Sqlserver_PO.getForeignKey()  # 获取所有外键关联表
# Sqlserver_PO.dropKey(fk, 'a_sc')  # 删除外键关系
# Sqlserver_PO.dropKey(fk, 'a_upload_course')  # 删除外键关系
# Sqlserver_PO.dropKey(fk, 'a_upload_student')  # 删除外键关系
#
# # todo 2, 导入表结构
# importDb_student('test.xlsx', 'a_student', 'student')
# importDb_course('test.xlsx', 'a_course', 'course')
# importDb_sc('test.xlsx', 'a_sc', 'a_student', 'a_course', 'sc')
#
# # todo 3, 生成测试数据
# genStudent('a_student')
# genCourse('a_course')
# genSc('a_sc', 'a_student', 'a_course')
#
# # # todo 4, 清理数据（删除表）
# Sqlserver_PO.execute("drop table a_student")
# # Sqlserver_PO.execute("drop table a_course")
# # Sqlserver_PO.execute("drop table a_sc")

