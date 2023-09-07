# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
# Description: # textwrap 调整换行符的位置来格式化文本
# __all__ = ['TextWrapper', 'wrap', 'fill', 'dedent', 'indent', 'shorten']
# 官网：https://docs.python.org/zh-cn/3.8/library/textwrap.html
# 学习：https://www.cnblogs.com/wj5633/p/6931187.html
# 学习：https://blog.csdn.net/zwbzwbzwbzwbzwbzwb/article/details/52824154
# ***************************************************************u**

# list1 = ['name', 'age','sex']
# print(str(list1))

dict1 = {'a': 1, 'b': 2, 'c': 3}
values = dict1.keys()
print(list(values))  # ['a', 'b', 'c']
str2 = ','.join(list(values))
print(str2) # a,b,c

# import exifread,os
#
# with open('DSC_0127.JPG', 'rb') as file_data:
#     tags = exifread.process_file(file_data)
#     tag_date = 'EXIF DateTimeOriginal'
#     print(tags)
#     if tag_date in tags:
#         print(tag_date)
#         file_rename =str(tags[tag_date]).replace(':','').replace(' ', '_')
#         print(file_rename)
#         # file_rename =str(tags[tag_date]).replace(':','').replace(' ', '_') + os.path.splitext(filename)[1]
#         # new_path = os.path.join(root_dir, file_rename)
#         # os.rename(file_path, new_path）


# from PO.ListPO import *
# List_PO = ListPO()

# d_data = [
#             {'idCard': '310101198004332001'},
#             {'idCard': '310101198004332002'}
#         ]
#
# for i in range(len(d_data)):
#     print(d_data[i])
#     print(d_data[i]['idCard'])

# list1 = ['GW', 'QTY0:0', 'PG_AGE003:11212', 'PG_JWS001:1']
#
# list1.pop(0)
# list1 = List_PO.list2dictByKeyValue(list1)
# print(list1)
# print(x['PG_AGE003'])

# import sys,os,datatime

# s = "['r1',123]"
# print()
#
# # var = {'母亲': ['脑卒中', '冠心病',{'其他':'123'}], '父亲': ['高血压', '糖尿病'], '其他':['12121','2020-12-12']}
# var = {'姓名': '魏梅娣', '民族': '苗族', '文化程度': '小学教育'}
# =======
#
# var = {'母亲': ['脑卒中', '冠心病',{'其他':'123'}], '父亲': ['高血压', '糖尿病'], '其他':['12121','2020-12-12']}
#
# >>>>>>> origin/master
# =======
#
# var = {'母亲': ['脑卒中', '冠心病',{'其他':'123'}], '父亲': ['高血压', '糖尿病'], '其他':['12121','2020-12-12']}
#
# >>>>>>> 135c3a46e4d45a68f5bbf120c543ea6685b3b90f
# =======
#
# var = {'母亲': ['脑卒中', '冠心病',{'其他':'123'}], '父亲': ['高血压', '糖尿病'], '其他':['12121','2020-12-12']}
#
# >>>>>>> 135c3a46e4d45a68f5bbf120c543ea6685b3b90f
# # print(len(var))
# x=1
# for k,v in var.items():
#     x = x+1
#     print(k,v,x)

#
# for i in range(len(var)):
#
#     if isinstance(v[i],dict) == True:

#
# for k,v in var.items():
# <<<<<<< HEAD
# <<<<<<< HEAD
# <<<<<<< HEAD
#     if k == '姓名':
# =======
#     if k == '其他':
# >>>>>>> origin/master
# =======
#     if k == '其他':
# >>>>>>> 135c3a46e4d45a68f5bbf120c543ea6685b3b90f
# =======
#     if k == '其他':
# >>>>>>> 135c3a46e4d45a68f5bbf120c543ea6685b3b90f
#         print(v)


    # if v.type
    # if '其他' in v:
    #     print(1121212)




# 查看9222端口情况，lsof -i tcp:9222
# 删除PID， kill -9 3333   //这里3333是9222的PID
# a = 'Ella聊美语/让我带你读你的第一本英文原著✅ \n（我的英文基础网课、自学指南电子书、一对一请看我首页） \n我初学英文的时候看的原著有\n1 Diary of a Wimpy Kid 词汇量范围 1000-3000\n它是一个青少年小说，而且有出同名电影，里面的用词和表达很日常也很俏皮，单词量范围也不会很大，highly recommend! \n2 Rich Dad Poor Dad (30'
# print(len(a))
# print(a[:5])
# from DrissionPage.easy_set import set_paths
# set_paths(browser_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
# # set_paths(browser_path='/Applications/Firefox.app/Contents/MacOS/firefox')
#
# from DrissionPage import ChromiumPage
# page = ChromiumPage()
# page2 = ChromiumPage()
# page.get('https://www.baidu.com')
# page2.get('https://www.jd.com')
#
# from decimal import Decimal

# import hashlib
# import execjs
#
#
# def getMd5(varText):
#     """2.4.1，生成MD5加密值"""
#     # 分析：加密输出是16进制的md5值，这里传入的字符串前加个b将其转为二进制，或者声明为utf-8, 否则回报错误TypeError: Unicode-objects must be encoded before hashing
#
#     m = hashlib.md5(
#         varText.encode(encoding="utf-8")
#     )  # 等同于 m = hashlib.md5(b'123456')
#     return m.hexdigest()
#
# print(getMd5("https://cn.pornhub.com/view_video.php?viewkey=640c1194860f9"))  # e10adc3949ba59abbe56e057f20f883e

# print("*" * 100)
# print("* [ignore] => " )
# print("*" * 0 )

# md = "3888ab363c8d6425133f2f83b685e39a".hashvalue
# print(md)
#
#
# def get_js():
#     # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
#     f = open("./helpers.js", 'r', encoding='UTF-8')
#     line = f.readline()
#     htmlstr = ''
#     while line:
#         htmlstr = htmlstr + line
#         line = f.readline()
#     return htmlstr
# jsstr = get_js()
# ctx = execjs.compile(jsstr)
# print(ctx.call('640c1194860f9'))

# from md5util import Md5Util
# print(Md5Util("640c1194860f9"))

# dingding机器人
# url = "https://oapi.dingtalk.com/robot/send?access_token=0708efc5088d851887a18f31a2effc31a9f1d2ba2340ab5643a5b53b3e88cb7d"
# url = "https://oapi.dingtalk.com/robot/send?access_token=528fb490067de67a0bce13c344504aeacd45d268150d86a57b949d75553a9d12"
# sign = "SEC31686f219dcb7356c3a4281f8fe4e7cc42bc40cb9f9fa63f7bca29665c06aa9e"
#
# json_text={
#     "at": {
#         "atMobiles":[
#             "180xxxxxx"
#         ],
#         "atUserIds":[
#             "user123"
#         ],
#         "isAtAll": False
#     },
#     "text": {
#         "content":"测试机器人推送服务"
#     },
#     "msgtype":"text"
# }
#
# from jsonpath import jsonpath
# print(jsonpath(json_text, '$..text'))

# import requests, json, sys
# m = requests.post(url, json.dumps(json_text), headers={"Content-Type": "application/json"}).content
# print(m)
#
# sys.exit(0)
#
#
#
# print((m.decode("utf-8", 'strict')))

# requests.post(url, json.dumps(json_text), headers={"Content-Type":"application/json;charset=utf-8"})





# x = 10.555
# print(1/8*100)
# f = 12.5
# f = 13.5
# f = (1/8*100)
#
# ff = int(f)
# if ff % 2 == 0:
#     print(round(f+1)-1)
# else:
#     print(round(f))
#
#
# print(round(12.5*100)/100)
# print(round(Decimal("12.5"),0))
# print(Decimal("12.5").quantize(Decimal("0")))
# s = '{"currPage": 0, "deptId": "", "endTime": "", "pageSize": 0, "searchId": "", "searchName": "", "starTime": ""}'
#
# print()














#
# from docx import Document
# from docx.shared import Inches
#
# def test():
#     ...
#
# def tt():
#
#
#
#
# document = Document('demo.docx')
#
# document.add_heading('Document Title', 0)
#
# p = document.add_paragraph('A plain paragraph having some ')
# p.add_run('bold').bold = True
# p.add_run(' and some ')
# p.add_run('italic.').italic = True
#
# document.add_heading('Heading, level 1', level=1)
# document.add_paragraph('Intense quote', style='Intense Quote')
#
# document.add_paragraph(
#     'first item in unordered list', style='List Bullet'
# )
# document.add_paragraph(
#     'first item in ordered list', style='List Number'
# )
#
# document.add_picture('test.jpg', width=Inches(1.25))
#
# records = (
#     (3, '101', 'Spam'),
#     (7, '422', 'Eggs'),
#     (4, '631', 'Spam, spam, eggs, and spam')
# )
#
# table = document.add_table(rows=1, cols=3)
# hdr_cells = table.rows[0].cells
# hdr_cells[0].text = 'Qty'
# hdr_cells[1].text = 'Id'
# hdr_cells[2].text = 'Desc'
# for qty, id, desc in records:
#     row_cells = table.add_row().cells
#     row_cells[0].text = str(qty)
#     row_cells[1].text = id
#     row_cells[2].text = desc
#
# document.add_page_break()
#
# document.save('demo.docx')



# for para in document.paragraphs:
#     print(para.text)
#     if 'first' in para.text:
#         for run in para.runs:
#             if 'first' in run.text:
#                 run.text = run.text.replace('first', '金浩')
#
# for t in document.tables:
#     for i in range(len(t.rows)):
#         for j in range(len(t.columns)):
#             print(t.cell(i, j).text)
#             if 'first' in t.cell(i, j).text:
#                 t.cell(i, j).text = t.cell(i, j).text.replace('first', '金浩')
#
#
# document.save('demo.docx')

# import PyV8
# ctxt = PyV8.JSContext()
# ctxt.enter()
# func = ctxt.eval("""
#     (function(){
#         function hello(){
#             return "Hello world.";
#         }
#         return hello();
#     })
# """)
# print(func())

# def test(*var):
#     print(len(var))
#     print(var)


# test("aaa")
# test("aaa","bbb")

# a = {5:[{"member_id":1212}], 6:[{"loan_amount":12},{"loan_":333}] }
# print(a)
# from PO.DataPO import *
# Data_PO = DataPO()
#
# d= {7:[1,2,3],8:["44",66]}
# print(d[8])

# import json
# # str1 = "{'userNo':'$.data','tt':'success','orgno':'\"wgzx\" + str(Data_PO.autoNum(3))'}"
# str1 = '{"userNo":"$.data","tt":"success","orgno":"\'wgzx\' + str(Data_PO.autoNum(3))"}'
# d = json.loads(str1)
# dd = dict(eval(str1))
# print(dd)
# # print(d)
# # print(d['orgno'])
# #
# # x = eval(d['orgno'])
# # print(x)
#
# for k, v in d.items():
#     if "str(" in v:
#         d[k] = eval(d[k])
#
# print(d)

# import json
# dict1 = {}
# # a = {"xx":"select COUNT(*) FROM ep_resident_user"}
# a = '{"xx":"select COUNT(*) FROM ep_resident_user","yy":123}'
# d_a = json.loads(a)
# print(d_a)
# for k,v in d_a.items():
#     print(k,v)
#     test=555
#     dict1[k]= test
#
# print(dict1)

# d= {"a":1, "b":2}
# print(d)
# d["b"]=3
# print(d)
#
# x = '[{"detail": "123123","endTime": "","id": 0,"isDelete": 0,"startTime": "" }]'
#
# dd = '{"a":1, "b":2}'
# import json
#
# target_list = json.loads(dd)
# print(type(target_list))
# print(target_list)

# import functools
#
# def three_way_cmp(x, y):
#     """Return -1 if x < y, 0 if x == y and 1 if x > y"""
#     # return (x > y) - (x < y)
#     return x<y
#
# case = ["1","2","3","10"]
# case.sort(key=functools.cmp_to_key(three_way_cmp))
# print(case)

# def test_1():
#     print("121212")
#
# def test_2():
#     print("99999999999")
#
#
# # for funcType in ('handler', 'request'):
#
#     # a='%s_version'%funcType
# url = eval('test_%s' % range(10))()  ###wval把string变量转换成相应函数



# x = "$.code:200"
# print(len(x.split(",")))
# print(x.split(":")[0])
# print(x.split(":")[1])
#
# a = '$.code:200,$.data.name:"政监中心4"'
# print(len(a.split(",")))
# for i in range(len(a.split(","))):
#     print(a.split(",")[i].split(":")[0])
#     print(a.split(",")[i].split(":")[1])
#

# import jsonpath
#
# dd = {'code': 200, 'msg': 'success', 'data': {'totalCount': 1, 'pageSize': 1, 'totalPage': 1, 'currPage': 1, 'list': [{'id': 16, 'name': '证监自动246更', 'code': 'ZJ0011638780963018', 'responsiblePerson': '张三丰', 'address': '北京市', 'area': '莆田区', 'contactPerson': '北京人', 'contactPhone': '13316161616', 'status': 1}]}}
# iResValue = jsonpath.jsonpath(dd, expr="$.data.list[0].name")
# print(iResValue)




# #
# import textwrap
#
# text = """abcdefg
# hijklmn
# opqrstuvwxyz
# """
#
# print(text)
# #
# # # # # todo: fill() 调整换行符,每行显示给定宽度，注意下一行前会有空格
# print("fill() 调整换行符,每行显示给定宽度".center(100, "-"))
# print(textwrap.fill(text, width=6))
# # # abcdef
# # # g hijk
# # # lmn op
# # # qrstuv
# # # wxyz
#
# # # # todo:dedent() 去除缩进
# print("dedent()去除缩进".center(100, "-"))
# sample_text = '''    aaabbb    cccddd'''
# print(textwrap.dedent(sample_text))
# # # # aaabbb    cccddd
#
# # # # todo:indent() 给定前缀
# print(":indent() 给定前缀".center(100, "-"))
# print(textwrap.indent(text, prefix='----'))
# # ----abcdefg
# # ----hijklmn
# # ----opqrstuvwxyz
#
#
# s = 'hello\n\n \nworld'
#
# # # 默认忽略空白符（包括任何行结束符）组成的行（\n）
# print(textwrap.indent(s, '+ '))
# # + hello
#
# # + world
#
#
# # # 函数对象 = lambda 参数：表达式
# print(textwrap.indent(s, '+ ', lambda line: True))
# # + hello
# # +
# # +
# # + world
#
# #
# # # todo:首行缩进，其余行添加前缀22，每行限制字符10个。
# # print("首行缩进，其余行添加前缀22，每行限制字符10个。".center(100, "-"))
# # # subsequent_indent:初始化除了第一行的所有行
# # detent_text = textwrap.dedent(text).strip()
# # print(textwrap.fill(detent_text, initial_indent='  ', subsequent_indent='22', width=10))
# # #   abcdefg
# # # 22hijklmn
# # # 22opqrstuv
# # # 22wxyz
# #
# #
# # # todo:shorten() 多余的省略号
# # print("shorten() 多余的省略号".center(100, "-"))
# # print(textwrap.shorten(text, width=20))
# # # abcdefg [...]
# # print(textwrap.shorten("Hello world", width=10, placeholder="..."))
# # # Hello...
# #
# # # todo:wrap() 将一个字符串按照width的宽度进行切割，切割后返回list
# # print("wrap() 将一个字符串按照width的宽度进行切割，切割后返回list".center(100, "-"))
# # print(textwrap.wrap(text, width=10))
# # # ['abcdefg', 'hijklmn op', 'qrstuvwxyz']
# # # 分析：结果并不是保证了每个list元素都是按照width的，因为不但要考虑到width，也要考虑到空格（换行），也就是一个单词。
# #
# # sample_text = 'aaabbbcccdddeeeedddddfffffggggghhhhhhkkkkkkk'
# # print(textwrap.wrap(sample_text, width=5))
# # # ['aaabb', 'bcccd', 'ddeee', 'edddd', 'dffff', 'fgggg', 'ghhhh', 'hhkkk', 'kkkk']
# #
# #
# # print("定义 class textwrap.TextWrapper(…)".center(100, "-"))
# # # class textwrap.TextWrapper(…) # 这个类的构造函数接受一系列的关键字参数来初始化自己的属性信息
# # sample_text = '''aaa'''
# # textWrap = textwrap.TextWrapper()
# # textWrap.initial_indent = 'bbb'
# # print(textWrap.wrap(sample_text))
# # # ['bbbaaa']
# #
# # sample_text = '''aaa
# # kkk
# # jjj'''
# # textWrap = textwrap.TextWrapper(width = 2)
# # textWrap.initial_indent = 'bbb'
# # textWrap.subsequent_indent = 'ccc'
# # print(textWrap.wrap(sample_text))
# # # ['bbba', 'ccca', 'ccca', 'ccck', 'ccck', 'ccck', 'cccj', 'cccj', 'cccj']
# #
# #
# #


# a = ["welcome,linuxmi.com,33"]
# for i in a:
#     print(i.count(',') + 1)



# import numpy as np
# # 列表排序
# a = np.array([2,1,0,5])
# print(a)
# print(a[:3])
# print(a.min())
# a.sort()
# print(a)
# b = np.array([1,2,3])
# print(b*b)