# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-1-6
# Description: BeautifulSoup定位页面元素，如下载页面上图片
#***************************************************************

import requests
from bs4 import BeautifulSoup

url = 'http://tieba.baidu.com/p/4468445702'
html = requests.get(url)
html.encoding = 'utf-8'

text = html.text
bsop = BeautifulSoup(text, 'html.parser')
img_list = bsop.find('div',{'id':'post_content_87286618651'}).findAll('img')
img_src = img_list[0].attrs['src']
print("文件名：" + img_src)

# 下载
img = requests.get(img_src)
with open('d://a.jpg', 'ab') as f:
    f.write(img.content)
    f.close()
