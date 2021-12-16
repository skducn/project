# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: beautifulsoup
# https://cuiqingcai.com/1319.html
#***************************************************************

import requests
from bs4 import BeautifulSoup

url = 'https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
       'cookie':'MONITOR_WEB_ID=bc0ebf54-4beb-4695-9dab-e40fa40f4b48; MONITOR_DEVICE_ID=95754a8d-9842-4e89-989a-0d288d90eae7; douyin.com; ttcid=130e44ae32ad4950a5ec4a602e232cde24; ttwid=1|Eh1Ouec2-ziB4uWFBitPbmXba9wMCha8ZUkabof_Fb0|1639620655|8e3315a1ede4cfbdf421bc4c21b6f58db28769d249e0142c450008162841ff41; _tea_utm_cache_6383=undefined; AB_LOGIN_GUIDE_TIMESTAMP=1639620656172; MONITOR_WEB_ID=ae83c60f-09ea-4225-82ff-d74fa1a41fd3; s_v_web_id=verify_kx8bt03q_EDZ2Uu4P_fxob_41pr_8nJK_PeaKbeLFUohL; passport_csrf_token_default=2386a4b13f60cac7c3d4251f51f187a0; passport_csrf_token=2386a4b13f60cac7c3d4251f51f187a0; THEME_STAY_TIME=299196; IS_HIDE_THEME_CHANGE=1; __ac_nonce=061baad0d003f063b379a; __ac_signature=_02B4Z6wo00f01UcKFxwAAIDBxwjtXI1FrpVHLhOAADB7R928uojvFrV4iIGxAkko1C-KbsGuBlxH3htCQB4dgbVkTJWgpe.qnG8S2IqyEhsZ-lfHkhRiQF-gYZmY7EoMNPrG4mjUHC9yYSmG00; home_can_add_dy_2_desktop=1; tt_scid=4bUDRD1gsLZn4wHYWONAgN7KfK.fWvVhMpNU0weJZa6fjzqxZz8MDSIxoXuiRLdhc58c; pwa_guide_count=2; msToken=7czSYbt_N_VW3Kmthtp-nKMZNKfe_O7DuK3r6LMPDuq3fyPql8hqMQVzgebCEKmikj3L42y5cSJAczVS9tOexeTE6FiwDTDXqGtfwabTFgPOHNbHibg5JhAH'}

html = requests.get(url,headers=headers)
html.encoding = 'utf-8'
text = html.text
# print(text)

soup = BeautifulSoup(text, 'html.parser')
# soup = BeautifulSoup(text, 'lxml')
# soup = BeautifulSoup(text, 'html5lib')
# soup = BeautifulSoup(text)
# print(soup.select('img'))
nameTags = soup.findAll('img',{"alt":True})
for n in nameTags:
    url = n["src"]
    alt = n['alt']
    print(url,alt)
    # Do your processing

# for i in bsop.select('img'):
#     # print(i.get_text())
#     print(i)
#     break








