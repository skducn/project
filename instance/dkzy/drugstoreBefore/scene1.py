# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-3-15
# Description: 电科智药，药店前台，场景1
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

from dkzy.drugstoreBefore.config.config import *
from dkzy.drugstoreBefore.PageObject.DrugstorePO import *
from Public.PageObject.ThirdPO import *
from Public.PageObject.DatabasePO import *

Level_PO = LevelPO(driver)
Drugstore_PO = DrugstorePO(Level_PO)
Third_PO = ThirdPO()
Database_PO = DatabasePO('10.111.3.4', 3306, 'cetc', '20121221', 'cetchis')

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# # 环境

'''登录及修改密码'''

Level_PO.openURL(1200, 900, varUrl, 3)
# 登录
Drugstore_PO.login("666003", "q123456")
Level_PO.setMaximize()


# 修改密码


# '''药库管理'''
# Level_PO.clickLinktext("药库管理", 4 )
#
# # 搜索（全部，推荐，药品类型，批准文号，关键字）
# Level_PO.selectNameValue(u"is_recommend", u"1")  # 推荐
# Level_PO.selectNameText(u"classify", u"全部")  # 药品类型
# Level_PO.inputXpath(u"//form[@id='queryForm']/div[3]/input", "H10930120")  # 批准文号
# Level_PO.inputXpath(u"//form[@id='queryForm']/div[4]/input", u"头包包")  # 药品名
# Level_PO.clickId(u"btnQuery", 2)  # 搜索
#
#
# # 添加药品
# varName, varProductName = Drugstore_PO.drugManager_add(u"国药准字H10930120", u"4566464", u"头包包123", u"上海第一药", u"40*8篇", u"上第药", u"12.55")
#
#
# # '编辑药品
# Database_PO.cur.execute('select store_druginfo_id from tt_store_druginfo where name="%s" and product_name="%s" order by store_druginfo_id desc limit 1' % (varName, varProductName))
# t1 = Database_PO.cur.fetchall()
# sleep(2)
# Level_PO.clickXpathsInclude(u"//a[@data-target='#popup-drug-edit']", u"this, " + str(t1[0][0]) + u",", 2)
# Level_PO.clickId(u"doUploadFileId", 2)
#
# # 搜索（全部，推荐，药品类型，批准文号，关键字）
# Level_PO.selectNameText(u"is_recommend", u"是")  # 推荐
# Level_PO.selectNameText(u"classify", u"中药")  # 药品类型
# Level_PO.inputName(u"authentication_code", u"123")  # 批准文号
# Level_PO.inputName(u"name", u"头包包")  # 药品名

# 删除药品


 # 批量导入
 # 翻页、页码、记录数

'''建议搭配'''
Level_PO.clickLinktext(u"建议搭配", 2 )
Level_PO.clickLinktext(u"口腔类", 2)
Level_PO.clickLinktext(u"口腔溃疡", 2)
# Level_PO.clickLinktext(u"添加", 2)
# Level_PO.clickXpaths(u"//span[@onclick='moveToRight(this)']", 2, 2)  # 添加第二个
# Level_PO.clickXpaths(u"//span[@onclick='moveToRight(this)']", 4, 2)  # 添加第四个
# Level_PO.clickXpath(u"//form[@id='recommend-recipe-form']/div[2]/div/button", 2)  # 提交
Level_PO.clickXpaths(u"//tr[@class='ajax-edit-btn']/td[8]/a/i", 1, 2)  # 删除
Level_PO.clickXpath(u"//form[@action='/smart-medicine/web/app.php/advise/recipeDelete']/div[3]/div/button", 2)  # 确定

sleep(1212)
 # 添加
 # 删除

'''处方管理'''
 # 搜索（日期，状态，处方变化/姓名）
 # 详情
 # 打印

'''业务统计'''

 # 药店交易排行榜
 # 药店交易
 # 处方审核
 # 医生咨询
 # 处方通过率

'''注销'''
# Level_PO.clickLinktext("注销", 2 )

