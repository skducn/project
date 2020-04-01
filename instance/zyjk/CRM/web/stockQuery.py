# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Created on : 2019-5-7
# Description: CRM 库存和采购查询
# 依据：商务管理（库存查询）需求文档-1025.docx
# 商务管理（采购查询）需求文档-1017.docx
# https://blog.csdn.net/firehood_/article/details/8433077  Tesseract-OCR 字符识别---样本训练
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from PO.excelPO import *
from instance.zyjk.CRM.PageObject.thirdSitePO import *
thirdSite_PO = ThirdSitePO()
excel_PO = ExcelPO()


# # if hasattr(excel_PO, "readRowValue"):
#
# func = getattr(excel_PO, "readRowValue")
# x = func("third.xlsx", 1, "Sheet1")
# print(x)
#
# sleep(1212)

scount = sum = s = bum = b = 0
excel2 = excel3 = ""
q2 = []
i, j = excel_PO.readRowCol("third.xlsx")
for a in range(1, i):
    q = excel_PO.readRowValue("third.xlsx", a, "Sheet1")
    if q[2] == "" and q[3] == "" and q[5] != "":
        # 多个账号
        q2.pop()
        q2.pop()
        q2.append(q[5])
        q2.append(q[6])
        # print(q2)
        func = getattr(thirdSite_PO, q2[1])
        s, b = func(q2)
        scount = scount + 1
        sum = s + sum
        bum = b + bum
        if scount == int(q2[0]):
            # 库存
            mysql_PO.cur.execute('select count(id) from data_stock where business="%s"' % (q2[2]))
            s1 = mysql_PO.cur.fetchone()
            if int(sum) == int(s1[0]):
                print("pass，库存，第三方合计：" + str(sum) + " ， 我方合计：" + str(s1[0]))
            else:
                print("errorrrrrrrrrrr，库存，第三方合计：" + str(sum) + "，我方合计：" + str(s1[0]))
            print("*" * 100)
            sum = 0
    else:
        # 单个账号
        func = getattr(thirdSite_PO, q[1])
        s, b = func(q)
        #   以上2句等同于 s = thirdSite_PO.gy(q)
        q2 = q
        scount = 1
        sum = s + sum
        bum = b + bum
        if scount == int(q2[0]):
            # 库存
            mysql_PO.cur.execute('select count(id) from data_stock where business="%s"' % (q2[2]))
            s1 = mysql_PO.cur.fetchone()
            if int(sum) == int(s1[0]):
                print("pass，库存，第三方合计：" + str(sum) + " ， 我方合计：" + str(s1[0]))
            else:
                print("errorrrrrrrrrrr，库存，第三方合计：" + str(sum) + "，我方合计：" + str(s1[0]))
            # 采购
            mysql_PO.cur.execute('select count(id) from data_buy where business="%s"' % (q2[2]))
            b1 = mysql_PO.cur.fetchone()
            if int(bum) == int(b1[0]):
                print("OK，采购，第三方平台合计：" + str(b) + "，我方爬取合计：" + str(b1[0]))
            else:
                print("errorrrrrrrrrrr，采购，第三方平台合计：" + str(b) + "，我方爬取合计：" + str(b1[0]))

            print("*" * 100)
            sum = 0
            bum = 0






# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# 2、测试库存和采购查询，共5家 （统计截至到今天的数据）

# thirdSite_PO.sy("2.2，上药控股有限公司", "http://passport.shaphar.com", "817036", "shengyun3303")  # ?
thirdSite_PO.zsytws("2.7，舟山英特卫盛医药有限公司",  "http://old.drugoogle.com", "aosaws", "a654321")
thirdSite_PO.hdds("2.9，华东岱山医药有限公司", "http://app1.yy5u.com:8080/NetSrvWeb/syslogin.aspx?result=5&txtCompanyID=24", "fcp","123456")


# # 以下2家需手工测试。
# # 库存查询中，是否显示批号选为：明细
# # 采购查询中，单据类型选：进货， 去掉开始时间
# varName = "浙江英特医药有限公司"
# mysql_PO.cur.execute('select count(id) from data_stock where business="%s"' % (varName))
# s1 = mysql_PO.cur.fetchone()
# mysql_PO.cur.execute('select count(id) from data_buy where business="%s"' % (varName))
# b1 = mysql_PO.cur.fetchone()
# print("2.11，浙江英特医药有限公司（http://www.drugoogle.com:8888/login，SZSAS，123456），我方库存合计：" + str(s1[0]) + "，采购合计：" + str(b1[0]))
#
# varName = "湖州英特药谷有限公司"
# mysql_PO.cur.execute('select count(id) from data_stock where business="%s"' % (varName))
# s1 = mysql_PO.cur.fetchone()
# mysql_PO.cur.execute('select count(id) from data_buy where business="%s"' % (varName))
# b1 = mysql_PO.cur.fetchone()
# print("2.6，湖州英特药谷有限公司（http://www.drugoogle.com:8888/login，huszas9，123456），我方库存合计：" + str(s1[0]) + "，采购合计：" + str(b1[0]))
#


# # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# 10，浙江嘉信医药有限公司 （需求不需要测试）
# varThird = "浙江嘉信医药有限公司"
# varURL = "http://www.jxyy.net/"
# print("第三方平台：" + varThird + " " + varURL)
# # s = hdds("jmc89873", "zjjxyy", varURL)
# print(varThird + " 平台合计数量：" + str(s))
# mysql_PO.cur.execute('select count(id) from data_stock where business="%s"' % (varThird))
# t1 = mysql_PO.cur.fetchone()
# print("我方数据库数量：" + str(t1[0]))