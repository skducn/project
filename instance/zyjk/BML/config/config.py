# coding: utf-8
# *****************************************************************
# Author     : John
# Date       : 2019-7-18
# Description: 白茅岭配置文件
# *****************************************************************

from selenium import webdriver
from PO.LevelPO import *
from PO.ThirdPO import *

# driver = webdriver.Firefox()
# option = webdriver.ChromeOptions()

# driver = webdriver.Chrome(chrome_options=option)

from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('disable-infobars')
extension_path = 'd:/chrom-plug-v74.0.3729.169.crx'
options.add_extension(extension_path)
driver = webdriver.Chrome(chrome_options=options)


# driver = webdriver.Chrome()
driver.implicitly_wait(5)
Level_PO = LevelPO(driver)

# # 各平台上数据初始化（Windows、Linux、Mac）
# if platform.system() == 'Windows' :
#     varGif = "D:\\pic\\1.gif"
#     varJpg = "D:\\pic\\index.jpg"
#     varDoc = "D:\\pic\\test.docx"
# elif platform.system() == 'Darwin' :  # for mac
#     varGif = "/Users/linghuchong/Desktop/pic/1.gif"
#     varJpg = "/Users/linghuchong/Desktop/pic/5.jpg"
#     varDoc = "/Users/linghuchong/Desktop/pic/test.doc"
# varValidDate = "2033-4-11"
#
# def printColor(macColor, winColor, varContent):
#     if platform.system() == 'Darwin':
#         print(macColor) + varContent + '\033[0m'
#     if platform.system() == 'Windows':
#         (eval(winColor))(varContent.encode('gb2312') + "\n")

# # 测试环境
# Database_PO = DatabasePO('10.111.3.4', 3306, 'cetc', '20121221', 'cetc_sy')  # 测试
# connRedis = redis.StrictRedis(host='10.111.3.4', port=6379, db=0, password="b840fc02d524045429941cc15f59e41cb7be6c52")
varURL = "http://192.168.0.81:8324/login"   # 前台登录页
# varURLbehind = "https://cetc.iotcetc.com:8084/shouying-admin/web/app.php/Login/login"  # 测试后台管理
# varURLyaojian = "https://cetc.iotcetc.com:8084/shouying-sfda/web/app.php/login/login"  # 测试后台药监登

# 生产环境
# Database_PO = DatabasePO('140.143.94.177', 3306, 'cetc', '20121221', 'cetc_sy')  # 生产
# connRedis = redis.StrictRedis(host='140.143.94.177', port=6379, db=0, password="b840fc02d524045429941cc15f59e41cb7be6c52")
# varURLfront = "https://sy.iotcetc.com/plfm/"  # 生产前台登录
# varURLbehind = "https://sy.iotcetc.com/admin/"  # 生产后台管理
# varURLyaojian = "https://sy.iotcetc.com/sfda/"  # 生产后台监管



# # for HTML5 way1
# driver.get('http://the-internet.herokuapp.com/drag_and_drop')
# sleep(4)
# pa = os.path.abspath(os.path.join(os.getcwd(), "../../../Public/js"))
# with open(pa + "\\drag_and_drop_helper.js") as f:
#     js = f.read()
# driver.execute_script(js + "$('#column-a').simulateDragDrop({ dropTarget: '#column-b'});")
