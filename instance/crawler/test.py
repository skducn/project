# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-7-1
# Description: 爬取 去哪儿 大连景区数据
#***************************************************************

import requests
from bs4 import BeautifulSoup
import openpyxl
from time import sleep
from PO.HtmlPO import *
Html_PO = HtmlPO()
from PO.OpenpyxlPO import *
Openpyxl_PO = OpenpyxlPO("d:\\test.xlsx")



count=1
x = 0
for page in range(1,5):
    params = (('from', 'mpl_search_suggest'), ('keyword', '大连'),('page', str(page)),)
    response = requests.get('https://piao.qunar.com/ticket/list.htm', headers=Html_PO.getHeadersProxies(), params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(response.text)
    zongs = soup.find_all('div', class_='sight_item')

    print(count)
    for i in zongs:
        name = i.find('h3').text
        if i.find(class_='clrfix').find(class_='level') == None:
           xingji = "无星级"
        else:
            xingji = i.find(class_='clrfix').find(class_='level').text
        diqu = i.find(class_='area').find('a').text

        # redu = round(float(i.find(class_='product_star_level').text.split()[-1][:4]) * 5, 2)

        redu = i.find(class_='product_star_level').text

        # dizhi = re.findall('地址：(.*?)地图', i.find(class_='address color999').text)[0]
        dizhi = i.find(class_='address color999').find('span').text

        if i.find(class_='sight_item_price') == None or i.find(class_='sight_item_price').find('em') == None:
           jiage = "无价格"
        else:
            jiage = i.find(class_='sight_item_price').find('em').text
        if i.find(class_='sight_item_sold-num').find('span')== None:
           yuexiao = "无月销"
        else:
           yuexiao = int(i.find(class_='sight_item_sold-num').find('span').text)

        print(name,xingji,diqu,redu,dizhi,jiage,yuexiao)
        x +=1
        Openpyxl_PO.setMoreCellValue([[x, name,xingji,diqu,redu,dizhi,jiage,yuexiao]])
        Openpyxl_PO.save()
    sleep(5)
    count +=1