# -*- coding: utf-8 -*-
# python3调用js的库之execjs
# pip3 install PyExecJS
# 2、本地安装Node.js：
# 执行js有时需要浏览器环境,需要window对象和document对象，所以需要安装Node.js环境
# Node.js 安装包及源码下载地址为：https://nodejs.org/en/download/，历史版本下载地址：https://nodejs.org/dist/
# 3、Node中安装jsdom模块 npm install jsdom
# https://www.jianshu.com/p/6e12c6a69f10


import execjs
import requests
import re


print(execjs.get().name)

x = execjs.eval("'red yellow blue'.split(' ')")
print(x)

print(execjs.get())

print(execjs.get().eval("1 + 2"))


ctx = execjs.compile(
    """
function add(x, y) {return x + y;}
"""
)
print(ctx.call("add", 1, 2))


print(eval("'red yellow blue'.split(' ')"))
