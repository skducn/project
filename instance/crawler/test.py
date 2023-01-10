# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: #Python爬取中高风险地区名单代码
#test
# ***************************************************************


import re
import requests
import time
from bs4 import BeautifulSoup


def getHTML(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def getContent(url):
    html = getHTML(url)
    soup = BeautifulSoup(html, "html.parser")
    paras_tmp = soup.select(".zw-title") + soup.select("p")
    paras = paras_tmp[0:]
    return paras


def saveFile(text):

    datetimes = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    fname = "D:/" + datetimes + r"Webdata.txt"
    f = open(fname, "w")
    for t in text:
        if len(t) > 0:
            f.writelines(t.get_text() + "\n\n")
    f.close()


def main():
    url = "http://www.gd.gov.cn/gdywdt/zwzt/yqfk/yqsj/content/post_3881568.html"
    text = getContent(url)
    saveFile(text)


main()

#
# if __name__ == '__main__':
# 	main()
