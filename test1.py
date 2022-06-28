# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2021-1-7
# Description: # textwrap 调整换行符的位置来格式化文本
# __all__ = ['TextWrapper', 'wrap', 'fill', 'dedent', 'indent', 'shorten']
# 官网：https://docs.python.org/zh-cn/3.8/library/textwrap.html
# 学习：https://www.cnblogs.com/wj5633/p/6931187.html
# 学习：https://blog.csdn.net/zwbzwbzwbzwbzwbzwb/article/details/52824154
# *****************************************************************

# d = {2: ['医患交流信息表接口', '群发消息-PC', '/saasuser/afPreoperativeCounselingInfo/addMassMessage', 'post', 'application/json', [{'in': 'body', 'name': 'chatVos', 'description': '数据对象', 'required': False, 'schema': {'type': 'array', 'items': {'$ref': '#/definitions/ChatVO'}}}]]}
#
# for k, v in d.items():
#     for i in range(len(v)):
#         if v[i] != None:
#             print(v[i])
x = '110100000000'
print(x[-6:])

a= {'code': '310101002001', 'name': '云南中路居委会',"village":[{'code': '110101001001', 'name': '多福巷社区居委会'},{'code': '110', 'name': '多福巷社区居委会2'}]}
# b= {'code': '310101002002', 'name': '龙泉园路居委会'}
# c= {'code': '310101002003', 'name': '贵州路居委会'}
# list1 = []
# list1.append(a)
# list1.append(b)
# list1.append(c)
# print(list1)
a.update({"village":[{"a:":"22"}]})
print(a)


# d = [{'type': 'array', 'description': '参会者反馈信息', 'items': {'originalRef': '会议反馈人员记录DTO', '$ref': '#/definitions/会议反馈人员记录DTO'}}]
# # if "items" in d:
# #     if "$ref" in d['items']:
# #         print(121212)
# # print(d['items']['$ref'].split("#/definitions/")[1])
# import json
# print(d)
# b = json.dumps(d, ensure_ascii=False)
# print(b)




# l = ['baidu','taobao']
# if 'baidu' in l :
#     print("121212")

# def sum(x):
#
#     for i in range(1,10):
#         print(x)
#         x = x + 1
#         if x == 10:
#             sum(x)
#
# sum(1)

# s = "tet"
# print(s.split(","))  # ['tet']

# # list0 =
# if "kill" not in ['t','kill']:
#     print("1111")
# else:
#     print("2222")

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
# # a = ["welcome,linuxmi.com,33"]
# # for i in a:
# #     print(i.count(',') + 1)
# #
# #
# # import numpy as np
# # #创建数组
# # a = np.array([2,1,0,5])
# # print(a)
# # print(a[:3])
# # print(a.min())
# # a.sort()
# # b = np.array([1,2,3],[4,5,6])
# print(b*b)