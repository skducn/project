# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John   # coding: utf-8
# Date       : 2019-2-18
# Description: 爬取西刺免费代理IP  ，http://www.xicidaili.com/nt/
# *****************************************************************

from time import sleep
import requests, re, random, os
from bs4 import BeautifulSoup

# 西刺免费代理IP
url = "http://www.xicidaili.com/nt/"

# 爬取的页数
pagenum = 1

# 构造headers
UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
headers = {'User-Agent': random.choice(UserAgent_List),
           'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           'Accept-Encoding': 'gzip',
           }

def ipTest(ip):
    '''
    检测爬取到的ip地址可否使用，能使用返回True，否则返回False，默认去访问百度测试代理
    '''
    try:
        r = requests.get('https://www.baidu.com', headers=headers, proxies={'http': ip[0]+':'+ip[1]}, timeout=10)
        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def scrawlIp(url, pagenum):
    '''
    爬取代理ip地址
    '''
    l_ip = []
    for n in range(1, pagenum + 1):
        url = url + str(n)
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        content = response.text
        # 正则：('14.118.130.213', '8081'）
        # pattern = re.compile('<td class="country">.*?alt="Cn" />.*?<td>(.*?)</td>.*?<td>(.*?)</td>', re.S)

        # 正则：('14.118.130.213', '8081', '广东江门')
        pattern = re.compile('<td class="country">.*?alt="Cn" />.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?">(.*?)</a>', re.S)
        items = pattern.findall(content)

        for ip in items:
            if ipTest(ip):  # 测试爬取到ip是否可用，测试通过则加入ip_list列表之中
                print('测试通过，IP => ' + str(ip[0]) + ':' + str(ip[1]) + "（"+  str(ip[2]) + ")")
                l_ip.append(ip[0]+':'+ip[1])
        sleep(5)  # 等待5秒爬取下一页
    return l_ip

def get_random_ip(l_ip):
    # 参数列表中随机获取一个IP
    return l_ip[random.randint(0, len(l_ip)-1)]


# *****************************************************************

# 爬取IP代理
total_ip = scrawlIp(url, pagenum)
print(get_random_ip(total_ip))



