# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-7-25
# Description: 社区健康管理中心
# 测试环境 # http://192.168.0.243:8010/#/login
# 'cs', '12345678'
#***************************************************************

from PIL import Image

# 转换图片尺寸，
def resize_image(input_image_path, output_image_path, size):
    with Image.open(input_image_path) as image:
        resized_image = image.resize(size)
        resized_image.save(output_image_path)

# 如将图片尺寸转换成 1440*900
# resize_image('/Users/linghuchong/Downloads/111.jpg', '/Users/linghuchong/Downloads/222.jpg', (1440, 900))

# 获取屏幕尺寸
# from screeninfo import get_monitors
#
# for monitor in get_monitors():
#     print(f"Width: {monitor.width}, Height: {monitor.height}")
#


# 获取图片的高度和宽度
import cv2, pyautogui
# image = cv2.imread('/Users/linghuchong/Downloads/111.jpg')
# height, width = image.shape[:2]
# print(height, width)



import pyautogui

from Chc_web_PO import *
Chc_web_PO = Chc_web_PO()
from bs4 import BeautifulSoup

varUrl = 'http://192.168.0.243:8010/#/'

# 1, 登录
# Chc_web_PO.login(varUrl + 'login', 'admin', 'Zy@123456')
Chc_web_PO.login(varUrl + 'login', 'cs', '12345678')

a = Web_PO.getTextListByX("//span")
print(a)

# # 2, 获取首页源码，点击菜单
# html_source = Web_PO.getSource()
# # print(html_source)
#
# # 获取首页上指标名称与值
# print("1，获取首页信息")
# Chc_web_PO.getTechnicalTarget()
#
# # 首页
# # Chc_web_PO.clkMenu(html_source, '首页')
#
# # # 居民健康服务
# print("2,点击健康服务")
# Chc_web_PO.clkMenu(html_source, '健康服务')
# Chc_web_PO.clkMenu(html_source, '健康评估及干预')
# # 健康评估及干预 - 查询
# # Chc_web_PO.healthEvaluateIntervene_search({'姓名': '儿童', '身份证': '310101', '人群分类': '老年人', '家庭医生': '测试', '签约日期范围start': '2024-05-01', '签约日期范围end': '2024-05-02', '年度评估状态': '未评估', '管理人群': '高血压', '最近一次评估日期start': '2024-05-03', '最近一次评估日期end': '2024-05-05', '最近一次确认日期start': '2024-05-06', '最近一次确认日期end': '2024-05-07'})
# # Chc_web_PO.healthEvaluateIntervene_search({'姓名': '儿童', '家庭医生': '测试', '年度评估状态': '预评估'})



# Chc_web_PO.clkMenu(html_source, '慢病管理')
# Chc_web_PO.clkMenu(html_source, '老年人体检')
# Chc_web_PO.clkMenu(html_source, '重点人群')

# 健康管理门诊
# Chc_web_PO.clkMenu(html_source, '居民登记')
# Chc_web_PO.clkMenu(html_source, '健康评估')

# 用户中心
# Chc_web_PO.clkMenu(html_source, '机构维护')
# Chc_web_PO.clkMenu(html_source, '用户维护')
# Chc_web_PO.clkMenu(html_source, '角色维护')
# Chc_web_PO.clkMenu(html_source, '接口管理')
# Chc_web_PO.clkMenu(html_source, '批量评估')
# Chc_web_PO.clkMenu(html_source, '错误日志')

# 社区配置
# Chc_web_PO.clkMenu(html_source, '常住人口')
# Chc_web_PO.clkMenu(html_source, '家医团队维护')
# Chc_web_PO.clkMenu(html_source, '家医助手')
# Chc_web_PO.clkMenu(html_source, '干预规则配置')
# Chc_web_PO.clkMenu(html_source, '停止评估名单')
# Chc_web_PO.clkMenu(html_source, '社区用户维护')
# Chc_web_PO.clkMenu(html_source, '评估建议')

# 系统监控
# Chc_web_PO.clkMenu(html_source, '定时任务')

# # 统计分析
# Chc_web_PO.clkMenu(html_source, '社区健康评估')
# # 点击 导出Excel
# Web_PO.clkByX("/html/body/div[1]/div/div[2]/section/div/div/main/div/div[2]/div[1]/div/div[1]/div[2]/button", 2)
# # 模拟按下 command + S 完成保存
# pyautogui.keyDown('command')
# pyautogui.press('s')
# pyautogui.keyUp('s')
# pyautogui.keyUp('command')

# pyautogui.moveTo(x=1033, y=627, duration=1)  # 将鼠标移动到确定按钮的位置
# pyautogui.click()
# 如果需要输入文件名，可以使用pyautogui的类型函数
# pyautogui.typewrite('my_filename')
# 然后点击保存




# Chc_web_PO.clkMenu(html_source, '全区健康评估')

# 大屏可视化 - 社区中心 (必须放在最后)
# Web_PO.opn(varUrl + "largeScreen/community")
