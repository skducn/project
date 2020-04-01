# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018-3-15
# Subject    : 首营资料交换平台
# Description: firefox 52 , selenium 3.11.0  /usr/local/bin/geckodriver
# https://blog.csdn.net/huilan_same/article/details/52305176  selenium之 玩转鼠标键盘操作（ActionChains）
# PYTHONPATH 中写入：D:\51\Python\09project ,设置环境变量以便引入Public下的包。
# sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "../../..")))  # 将d:\51\python\09project加入环境变量。
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import sys, redis
# reload(sys)
# sys.setdefaultencoding("utf-8")
sys.path.append("..")
from Public.cmdColor import *
# from Public.PageObject.DatabasePO import *
from Public.PageObject.LevelPO import *
from Public.PageObject.ThirdPO import *
Third_PO = ThirdPO()

# 各平台上数据初始化（Windows、Linux、Mac）
if platform.system() == 'Windows' :
    varGif = "D:\\pic\\1.gif"
    varJpg = "D:\\pic\\index.jpg"
    varDoc = "D:\\pic\\test.docx"
elif platform.system() == 'Darwin' :  # for mac
    varGif = "/Users/linghuchong/Desktop/pic/1.gif"
    varJpg = "/Users/linghuchong/Desktop/pic/5.jpg"
    varDoc = "/Users/linghuchong/Desktop/pic/test.doc"
varValidDate = "2033-4-11"

def printColor(macColor, winColor, varContent):
    if platform.system() == 'Darwin':
        print(macColor) + varContent + '\033[0m'
    if platform.system() == 'Windows':
        (eval(winColor))(varContent.encode('gb2312'))
        # (eval(winColor))(varContent.encode('utf-8'))

# 测试环境
# Database_PO = DatabasePO('10.111.3.4', 3306, 'cetc', '20121221', 'cetc_sy')  # 测试
# connRedis = redis.StrictRedis(host='10.111.3.4', port=6379, db=0, password="b840fc02d524045429941cc15f59e41cb7be6c52")
varURLfront = "http://192.168.0.65"   # 测试前台登录页

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
