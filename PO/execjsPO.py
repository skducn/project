# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2024-5-30
# Description   : execjs 执行 javaScript
# pip3 install PyExecJS
# 2、本地安装Node.js：
# 执行js有时需要浏览器环境,需要window对象和document对象，所以需要安装Node.js环境
# Node.js 安装包及源码下载地址为：https://nodejs.org/en/download/，历史版本下载地址：https://nodejs.org/dist/
# 3、Node中安装jsdom模块 npm install jsdom
# https://www.jianshu.com/p/6e12c6a69f10
# *********************************************************************

import execjs


# 创建execjs环境
env = execjs.get()
# print(execjs.get().name)  # Node.js (V8)
# print(execjs.get())  # ExternalRuntime(Node.js (V8))


# 加载 js文件或包含js代码的字符串
ctx = env.compile("""function add(x, y) {return x + y;}""")
# 执行js代码
print(ctx.call("add", 1, 2))


print(env.eval("'red yellow blue'.split(' ')"))  # ['red', 'yellow', 'blue']
print(env.eval("1 + 2"))  # 3
print(eval("'red yellow blue'.split(' ')"))  # ['red', 'yellow', 'blue']
