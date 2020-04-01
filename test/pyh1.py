# coding: utf-8
#****************************************************************
# jhj_v1_6.py
# Author     : John
# Version    : 1.0.0
# Date       : 2016-4-7
# Description: Pyh 是一个强大且简约的python模块，你可以使用它在python程序中生成HTML内容。在python代码中手写HTML代码非常
# 乏味并且使代码可读性变得非常糟糕。而且，当你尝试要去看一下HTML源码的时候，可读性同样很差。PyH为这一切提供了非常不错的解决方案。
# 注意：文件名不能是pyh.py
# 页面格式化 http://www.tuicool.com/articles/IRvEBr
# 好像不支持 python 3.x
#****************************************************************


from pyh import *
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

