# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: beautifulsoup
#***************************************************************

import requests
from bs4 import BeautifulSoup

url = 'https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg'
html = requests.get(url)
html.encoding = 'utf-8'

text = html.text
bsop = BeautifulSoup(text, 'html.parser')
for i in bsop.select('span[class="_03811320ee25b81d1c705fae532572ec-scss"]'):
    print(i.get_text())
    break

# print(bsop.select('span[class="_03811320ee25b81d1c705fae532572ec-scss"]'))


# print(img_src)
# img = requests.get(img_src)
# with open('a.jpg', 'ab') as f:
#     f.write(img.content)
#     f.close()

