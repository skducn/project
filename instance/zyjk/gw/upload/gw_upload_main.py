# coding=utf-8
# *****************************************************************
# Author     : John
# Created on : 2024-1-10
# Description: 公卫 - 省平台数据上报
# *****************************************************************

from Gw_upload_PO import *
gw_upload_PO = Gw_upload_PO()


# todo 1, 导入比对数据
# gw_upload_PO.excel2db(Configparser_PO.FILE("case"), Configparser_PO.FILE("sheetName"))

# # todo 2，执行
gw_upload_PO.run()


# 10 ERROR, SQL => 健康教育活动记录表.活动日期(date) T_ACTIVITY_RECORD.ACTIVITY_DATE = 2024-01-11, ORACLE => GW-30701 健康教育活动记录表.HDSJ(TB_JKJY_HDJLB.DATE.(HDSJ = 2024-01-11 00:00:00))