# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
# Description: # textwrap 调整换行符的位置来格式化文本
# __all__ = ['TextWrapper', 'wrap', 'fill', 'dedent', 'indent', 'shorten']
# 官网：https://docs.python.org/zh-cn/3.8/library/textwrap.html
# 学习：https://www.cnblogs.com/wj5633/p/6931187.html
# 学习：https://blog.csdn.net/zwbzwbzwbzwbzwbzwb/article/details/52824154
# *****************************************************************

import time
import logging
import urllib.request
import urllib.error
import requests
from selenium import webdriver

from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
###配置logging日志###
logging.basicConfig(level=logging.ERROR,
                   filename='./log.txt',
                   filemode='a',    # w:每次都会重新写 a：追加模式
                   format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
###读取URL文件，准备访问###
file = r".\url.txt"     # url文本
path = r".\pic"    # 截图路径
list = []   # 定义一个空列表
picnum = 0  #定义图片序号
url404 = 0  #定义404页面数量
url502 = 0  #定义502页面数量
blank = 0   #定义空白页面数量
error_list = set()  #定义错误集合
headers = {"user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36","If-None-Natch":"","If-Modified-Since":""}  #定义浏览器类型
with open(file, 'r+', encoding='utf-8') as f:
    lines = f.readlines()
    for url in lines:
        list.append(url)
print("共有{0}个url开始访问......".format(len(list)))  # 打印url的个数
###浏览器初始化，设置异步模式####
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities["pageLoadStrategy"] = "none"
driver = webdriver.Chrome()   #打开浏览器
driver.maximize_window()      #浏览器窗口最大化
for index, url1 in enumerate(list):    # 遍历索引和值
    ###处理URL http前缀###
    if not url1.startswith("http://"):
        url2 = "http://" + url1.rstrip()
    else:
        url2 = url1.rstrip()
    print("开始第{0}个url访问:{1}".format(index+1,url2))
    ###开始URL访问###
    try:
        driver.get(url2)
    except UnexpectedAlertPresentException:
        wait = WebDriverWait(driver, 3)
        driver.switch_to.alert.accept()   #解决弹框问题
    except TimeoutError:
        print("网页加载超时!")
        picnum += 1
        continue
    time.sleep(5)


    ###处理URI资源名，准备截图保存
    file = url1.rsplit("/", 1)[1]
    if "." in file:
        file = file.rsplit(".", 1)[0]
    try:
        picnum = picnum + 1
        name = r"\\" + str(picnum)+"_" + file + '.png'
        filename = path + name
        driver.get_screenshot_as_file(filename)
        print("保存第{0}个url截图成功".format(index+1))
    except:
        print("保存第{0}个url截图失败".format(index+1))
    ###判断页面状态，保存异常URL
    url3 = driver.current_url
    print("当前URL地址：",url3)
    msg = driver.page_source    # 获取网页源代码
    if 'HTTP Status 404' in msg:   # 判断404页面
        url404 += 1
        error_status = "404" + '\t'+'Not Found'
        error_list.add(str(index+1)+'\t'+url2+'\t'+error_status+"\n")   # 将所有异常域名存入set集合，会自动去重
    elif '502 Bad Gateway' in msg:  # 判断502页面
        url502 += 1
        error_status = "505" + '\t'+'Bad Gateway'
        error_list.add(str(index+1)+'\t'+url2+'\t'+error_status+"\n")
    else:
        try:                        # 使用try except语句避免因异常域名导致整个for大循环报错终止
            file = urllib.request.urlopen(url3, timeout=1.0)
            soup = BeautifulSoup(msg, "html.parser")
            [s.extract() for s in soup('script')]
            text = soup.get_text()      # 获取源代码中的有效字符
            num= len(text.replace('\n','').replace(' ',''))
            if num < 10:
                blank +=1
                error_status = "blank" + '\t'+'No Text Page'
                error_list.add(str(index+1)+'\t'+url3+'\t'+error_status+"\n")
        except urllib.error.URLError as e:          # 异常域名会进入except，可以得到出错原因和出错http状态码
            if hasattr(e, "code"):
                error_code = str(e.code)
            if hasattr(e, "reason"):
                error_reason = str(e.reason)
            error_status = error_code + '\t'+error_reason
            error_list.add(str(index+1)+'\t'+url3+'\t'+error_status+"\n")   # 将所有异常域名存入set集合，会自动去重
    abnormal_list = open('异常URL列表.txt', 'w')    # 如果之前有检测记录，则直接被覆盖
    abnormal_list.writelines(error_list)            # 将set的元素全部一次性写入
    abnormal_list.close()                       # 关闭文件句柄
with open ('异常URL列表.txt','a') as f:     # 记录异常URL及数量
    f.write('404页面数量：{}'.format(url404)+'\n')
    f.write('502页面数量：{}'.format(url502)+'\n')
    f.write('空白页面数量：{}'.format(blank)+'\n')
    f.write('*'*20+'\n')
driver.close()