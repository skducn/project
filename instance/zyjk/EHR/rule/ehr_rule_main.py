# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-2-21
# Description: EHR 质控规则自动化
# 【腾讯文档】EHR质控规则自动化
# https://docs.qq.com/sheet/DYm93RkZ3bENGSHd4?tab=BB08J2
#***************************************************************

from Ehr_rule_PO import *
ehr_rule_PO = Ehr_rule_PO()


# todo 1, excel导入db
ehr_rule_PO.excel2db(Configparser_PO.FILE("case"), Configparser_PO.DB_SQL("table"))


# todo 2, 运行主程序
# ehr_rule_PO.main(Configparser_PO.DB_SQL("table"), 'error')  # 执行错误记录
ehr_rule_PO.main(Configparser_PO.DB_SQL("table"), 'all')  # 执行全部记录


# todo 3, 导出html
ehr_rule_PO.db2html()


# # if c > 0:
# # #     # todo 4，如结果中有错误记录，则发邮件
# from PO.NetPO import *
# Net_PO = NetPO()
# Net_PO.sendEmail("测试组23", ['h.jin@zy-healthtech.com'], None,
#           "EHR规则自动化测试报告", "htmlFile", "<h3>您好，h.jin：</h3>", Configparser_PO.FILE("html"), """<br>
#    <h3>本邮件由智赢测试系统自动发出，请勿直接回复！</h3>
#    <h3>如您不愿意接收此类邮件，请联系我们，如有打扰请谅解。</h3>
#    <h3>谢谢</h3>
#    """)


os.system("open " + Configparser_PO.FILE("html"))






