# coding=utf-8
# *****************************************************************
# Author     : John
# Created on : 2024-1-10
# Description: 公卫上传省平台字段比对自动化
# 【腾讯文档】公卫上传省平台字段比对自动化
# https://docs.qq.com/sheet/DQmt3b0ZtaFJ0UUx0?scene=38dd5f6f6c27e537c65a062eHM2mr1&tab=6t6cya
# *****************************************************************

from Gw_upload_PO import *
gw_upload_PO = Gw_upload_PO()


# todo 1, 导入比对数据
# gw_upload_PO.excel2db(Configparser_PO.FILE("case"), Configparser_PO.FILE("sheetName"))

# # todo 2，执行
gw_upload_PO.run()


# 10 ERROR, SQL => 健康教育活动记录表.活动日期(date) T_ACTIVITY_RECORD.ACTIVITY_DATE = 2024-01-11, ORACLE => GW-30701 健康教育活动记录表.HDSJ(TB_JKJY_HDJLB.DATE.(HDSJ = 2024-01-11 00:00:00))