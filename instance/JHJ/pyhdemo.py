﻿# coding: utf-8
#****************************************************************
# jhj_v1_6.py
# Author     : John
# Version    : 1.0.0
# Date       : 2016-4-7
# Description: 自动化测试平台
#****************************************************************
#http://tungwaiyip.info/software/HTMLTestRunner.html

import sys,os

from pyh import *
print sys.path

page = PyH('My wonderful PyH page')
page.addCSS('myStylesheet1.css', 'myStylesheet2.css')
page.addJS('myJavascript1.js', 'myJavascript2.js')
page << h1('My big title', cl='center')
page << div(cl='myCSSclass1 myCSSclass2', id='myDiv1') << p('I love PyH!', id='myP1')
mydiv2 = page << div(id='myDiv2')
mydiv2 << h2('A smaller title') + p('Followed by a paragraph.')
page << div(id='myDiv3')
page.myDiv3.attributes['cl'] = 'myCSSclass3'
page.myDiv3 << p('Another paragraph')
page.printOut()

