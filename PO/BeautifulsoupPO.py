# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: beautifulsoup  HTML 解析器 封装包
# beautifulsoup官网：https://beautifulsoup.readthedocs.io/zh_CN/latest/
# 使用方法：https://cuiqingcai.com/1319.html

# 三个html解释器比较：
# pip3.9 install beautifulsoup4  特点：Python 的内置标准库，执行速度适中，文档容错能力强，Python 2.7.3 or 3.2.2) 前 的版本中文档容错能力差；
# pip3.9 install lxml  lxml 特点：速度快，文档容错能力强，需要安装 C 语言库，推荐安装；
# pip3.9 install html5lib , 特点：最好的容错性，以浏览器的方式解析文档，生成 HTML5 格式的文档，速度慢，不依赖外部扩展；

# Beautiful Soup四大对象：
# Tag，HTML 中的一个个标签，如<title>The Dormouse's story</title> 中的title标签
# NavigableString，获取标签内容
# BeautifulSoup，表示的是一个文档的全部内容，它是一个特色Tag对象，可获取 类型，名称，属性
# Comment，是文档中的备注类型，它是一个特殊类型的 NavigableString ，输出注释内容，但不输注释符号，如 注释<!-- Elsie -->，输出 Elsie
#***************************************************************

import requests
from bs4 import BeautifulSoup
from PO.HtmlPO import *
Html_PO = HtmlPO()
import bs4

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

# url = 'https://www.douyin.com/user/MS4wLjABAAAA9kW-bqa5AsYsoUGe_IJqCoqN3cJf8KSf59axEkWpafg'
# headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
#        'cookie':'MONITOR_WEB_ID=bc0ebf54-4beb-4695-9dab-e40fa40f4b48; MONITOR_DEVICE_ID=95754a8d-9842-4e89-989a-0d288d90eae7; douyin.com; ttcid=130e44ae32ad4950a5ec4a602e232cde24; ttwid=1|Eh1Ouec2-ziB4uWFBitPbmXba9wMCha8ZUkabof_Fb0|1639620655|8e3315a1ede4cfbdf421bc4c21b6f58db28769d249e0142c450008162841ff41; _tea_utm_cache_6383=undefined; AB_LOGIN_GUIDE_TIMESTAMP=1639620656172; MONITOR_WEB_ID=ae83c60f-09ea-4225-82ff-d74fa1a41fd3; s_v_web_id=verify_kx8bt03q_EDZ2Uu4P_fxob_41pr_8nJK_PeaKbeLFUohL; passport_csrf_token_default=2386a4b13f60cac7c3d4251f51f187a0; passport_csrf_token=2386a4b13f60cac7c3d4251f51f187a0; THEME_STAY_TIME=299196; IS_HIDE_THEME_CHANGE=1; __ac_nonce=061baad0d003f063b379a; __ac_signature=_02B4Z6wo00f01UcKFxwAAIDBxwjtXI1FrpVHLhOAADB7R928uojvFrV4iIGxAkko1C-KbsGuBlxH3htCQB4dgbVkTJWgpe.qnG8S2IqyEhsZ-lfHkhRiQF-gYZmY7EoMNPrG4mjUHC9yYSmG00; home_can_add_dy_2_desktop=1; tt_scid=4bUDRD1gsLZn4wHYWONAgN7KfK.fWvVhMpNU0weJZa6fjzqxZz8MDSIxoXuiRLdhc58c; pwa_guide_count=2; msToken=7czSYbt_N_VW3Kmthtp-nKMZNKfe_O7DuK3r6LMPDuq3fyPql8hqMQVzgebCEKmikj3L42y5cSJAczVS9tOexeTE6FiwDTDXqGtfwabTFgPOHNbHibg5JhAH'}


class BeautifulsoupPO:

    def __init__(self,url):

        # self.soup = BeautifulSoup(html, 'lxml')

        html = Html_PO.rspGet(url)
        html.encoding = 'utf-8'
        html = html.text
        self.soup = BeautifulSoup(html, 'html.parser')



    def getValue(self, url, tag1, attr1, value1, tag2, attr2):

        # 获取页面上标签中属性的值
        # 如：获取url中div标签中id为post_content_87286618651下img标签中src的值
        # Beautifulsoup_PO.getValue('http://tieba.baidu.com/p/4468445702',"div",'id','post_content_87286618651',"img","src")
        html = requests.get(url)
        html.encoding = 'utf-8'
        html = html.text
        soup = BeautifulSoup(html, 'html.parser')
        l_value = soup.find(tag1, {attr1:value1}).findAll(tag2)
        return l_value[0].attrs[attr2]

    def getValue2(self, tag1, attr1, value1):

        # 获取页面上标签中属性的值
        # 如：获取url中div标签中id为post_content_87286618651下img标签中src的值
        # Beautifulsoup_PO.getValue('http://tieba.baidu.com/p/4468445702',"div",'id','post_content_87286618651',"img","src")

        # print(soup.span.string)
        # l_value = soup.find_all(tag1, {attr1:value1})
        # l_value = self.soup.find_all(['span'])
        # l_value = self.soup.find_all(tag1, class_=value1)
        # l_value = self.soup.find_all(tag1, attrs={attr1:value1})
        # l_value = self.soup.find('div', class_='sound-list  H_g').find('ul')

        for s in self.soup.stripped_strings:
            print(repr(s))
        # l_value = self.soup.find_all('ul')
        # l_value = self.soup.find_all('div', {'class': 'text _nO'})

        # .find_all("a").attrs['title']
        #
        #
        # findAll("")[0].attrs['alt']
        # print(l_value)


    def downPic(self, picUrl, tosave):

        # 下载在线图片

        img = requests.get(picUrl)
        with open(tosave, 'ab') as f:
            f.write(img.content)
            f.close()


if __name__ == '__main__':


    Beautifulsoup_PO = BeautifulsoupPO("https://www.ximalaya.com/album/13738175")


    # print('.prettify() 格式化输出对象的内容'.center(100, "-"))
    # # print(Beautifulsoup_PO.soup.prettify())
    #
    # print('获取标签及内容（默认获取第一个标签）'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.title)  # <title>The Dormouse's story</title>
    # print(Beautifulsoup_PO.soup.head)  # <head><title>The Dormouse's story</title></head>
    # print(Beautifulsoup_PO.soup.a)  # <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>
    # print(Beautifulsoup_PO.soup.p)  # <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
    #
    #
    # print('标签类型是Tag'.center(100, "-"))
    # print(type(Beautifulsoup_PO.soup.a))  # <class 'bs4.element.Tag'>
    #
    #
    # print('标签属性name和attrs'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.name)  # [document]  ，soup 对象的 name 即为 [document]，对于其他内部标签，输出的值便为标签本身的名称。
    # print(Beautifulsoup_PO.soup.head.name)  # head
    # print(Beautifulsoup_PO.soup.p.attrs)  # {'class': ['title'], 'name': 'dromouse'} , 将标签中的属性转为字典，即可获取key或value
    #
    #
    # print('获取标签中属性的值'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.p.get('class'))  # ['title'] , 通过get获取值
    # print(Beautifulsoup_PO.soup.p['class'])  # ['title']
    #
    #
    # print('修改标签中属性的值'.center(100, "-"))
    # Beautifulsoup_PO.soup.p['class'] = "newClass"  # 修改class的值
    # print(Beautifulsoup_PO.soup.p['class'])  # newClass
    # print(Beautifulsoup_PO.soup.p)  # <p class="newClass" name="dromouse"><b>The Dormouse's story</b></p>
    #
    #
    # print('删除标签中属性的值'.center(100, "-"))
    # del Beautifulsoup_PO.soup.p['class']
    # print(Beautifulsoup_PO.soup.p)  # <p name="dromouse"><b>The Dormouse's story</b></p>
    #
    #
    # print('获取标签内容'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.p.string)  # The Dormouse's story
    # print(type(Beautifulsoup_PO.soup.p.string))  # <class 'bs4.element.NavigableString'>
    #
    #
    # print('BeautifulSoup 对象表示的是一个文档的全部内容'.center(100, "-"))
    # print(type(Beautifulsoup_PO.soup.name))  # <class 'str'> , 获取name的类型
    # print(Beautifulsoup_PO.soup.name)  # [document] ， 获取name名称
    # print(Beautifulsoup_PO.soup.attrs)  # {}，获取soup属性，空字典
    #
    #
    # print('标签a的值是注释，但也被作为值输出'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.a)  # <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>
    # print(Beautifulsoup_PO.soup.a.string)  #  Elsie
    # print(type(Beautifulsoup_PO.soup.a.string))  # <class 'bs4.element.Comment'> ， 对比一下soup.p.string 这个是NavigableString对象，而soup.a.string是Comment对象，只因为a的值是注释；
    #
    # # 判断标签值的类型，再决定输出 ， 需要导入import bs4模块
    # if type(Beautifulsoup_PO.soup.a.string) == bs4.element.Comment:
    #     print(123)
    #
    #
    # print('.contents 获取tag的子节点以列表的方式输出'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.head.contents)  # [<title>The Dormouse's story</title>]
    # print(Beautifulsoup_PO.soup.head.contents[0])  # <title>The Dormouse's story</title>
    #
    #
    # print('.children 获取tag子节点通过遍历输出'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.head.children)  # <list_iterator object at 0x000001AD4AEA9B50>, list生成器对象
    # for child in Beautifulsoup_PO.soup.body.children:
    #     print(child)
    # # <p name="dromouse"><b>The Dormouse's story</b></p>
    # #
    # #
    # # <p class="story">Once upon a time there were three little sisters; and their names were
    # # <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
    # # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
    # # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
    # # and they lived at the bottom of a well.</p>
    # #
    # #
    # # <p class="story">...</p>
    #
    # print('.stridescendantsng 获取所有子孙节点'.center(100, "-"))
    # # for child in Beautifulsoup_PO.soup.descendants:
    # #     print(child)
    #
    # print('.string 获取节点内容'.center(100, "-"))
    # # .string属性要点：
    # # 举例：<head><title>The Dormouse's story</title></head>
    # # 1，如果一个标签里没有其他标签，如<title> ,则.string输出标签内容；
    # # 2，如果一个标签里只有一个标签，如 <head>里只有一个<title>，则.string输出标签内容；
    # print(Beautifulsoup_PO.soup.head.string)  # The Dormouse's story
    # print(Beautifulsoup_PO.soup.title.string)  # The Dormouse's story
    # print(Beautifulsoup_PO.soup.html.string)  # None , 如果1个标签里有多个标签的话，tag无法确定返回哪个，即返回None
    #
    # print('.strings 获取多个内容，注意不包括注释'.center(100, "-"))
    # for string in Beautifulsoup_PO.soup.strings:
    #     print(repr(string))
    #
    # # "The Dormouse's story"
    # # '\n'
    # # '\n'
    # # "The Dormouse's story"
    # # '\n'
    # # 'Once upon a time there were three little sisters; and their names were\n'
    # # ',\n'
    # # 'Lacie'
    # # ' and\n'
    # # 'Tillie'
    # # ';\nand they lived at the bottom of a well.'
    # # '\n'
    # # '...'
    # # '\n'
    #
    # print('.stripped_strings 获取所有内容，并去除多余空白内容，即换行符。'.center(100, "-"))
    # for string in Beautifulsoup_PO.soup.stripped_strings:
    #     print(repr(string))
    #
    # # "The Dormouse's story"
    # # "The Dormouse's story"
    # # 'Once upon a time there were three little sisters; and their names were'
    # # ','
    # # 'Lacie'
    # # 'and'
    # # 'Tillie'
    # # ';\nand they lived at the bottom of a well.'
    # # '...'
    #
    # print('.parent属性 获取父节点 '.center(100, "-"))
    # p = Beautifulsoup_PO.soup.p
    # print(p.parent.name)  # body , p标签的父节点是body
    # content = Beautifulsoup_PO.soup.head.title.string
    # print(content.parent.name)  # title，title标签内容的父节点即当前标签title
    #
    #
    # print('.parents属性 获取全部父节点 '.center(100, "-"))
    # content = Beautifulsoup_PO.soup.head.title.string
    # for p in content.parents:
    #     print(p.name)
    #
    # # title
    # # head
    # # html
    # # [document]
    #
    #
    # print('.next_sibling .prev_sibling 属性 获取前后节点 '.center(100, "-"))
    # print(Beautifulsoup_PO.soup.p.next_sibling)  #       //实际就是空，因为空白或者换行也可以被视作一个节点
    # print(Beautifulsoup_PO.soup.p.prev_sibling)  # None  ， 即前面没有节点，返回None
    # print(Beautifulsoup_PO.soup.p.next_sibling.next_sibling)  # // 下下一个节点
    # # <p class="story">Once upon a time there were three little sisters; and their names were
    # # <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
    # # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
    # # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
    # # and they lived at the bottom of a well.</p>
    #
    # print('.next_siblings .prev_siblings 属性 获取前后迭代节点 '.center(100, "-"))
    # for sibling in Beautifulsoup_PO.soup.a.next_siblings:
    #     print(repr(sibling))
    # # ',\n'
    # # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
    # # ' and\n'
    # # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
    # # ';and they lived at the bottom of a well.'
    # # None
    #
    #
    # print('.next_element .previous_element 属性 获取所有节点 '.center(100, "-"))
    # print(Beautifulsoup_PO.soup.head.next_element)  # <title>The Dormouse's story</title>
    # print(Beautifulsoup_PO.soup.body.next_element.next_element)  # <p name="dromouse"><b>The Dormouse's story</b></p> , 因为body的下一节点是换行（也算节点），所这里是下下节点
    # print(Beautifulsoup_PO.soup.title.previous_element)  # <head><title>The Dormouse's story</title></head>
    # print(Beautifulsoup_PO.soup.title.previous_element.previous_element)
    # # <html><head><title>The Dormouse's story</title></head>
    # # <body>
    # # <p name="dromouse"><b>The Dormouse's story</b></p>
    # # <p class="story">Once upon a time there were three little sisters; and their names were
    # # <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
    # # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
    # # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;and they lived at the bottom of a well.</p>
    # # <p class="story">...</p>
    # # </body></html>
    #
    #
    # print('.next_elements .previous_elements 属性 获取所有迭代节点 '.center(100, "-"))
    # for ele in Beautifulsoup_PO.soup.a.next_elements:
    #     print(repr(ele))
    # # ' Elsie '
    # # ',\n'
    # # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>
    # # 'Lacie'
    # # ' and\n'
    # # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>
    # # 'Tillie'
    # # ';and they lived at the bottom of a well.'
    # # '\n'
    # # <p class="story">...</p>
    # # '...'
    # # '\n'
    #
    #
    #
    # print('find_all () 方法搜索当前 tag 的所有 tag 子节点之传标签名'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.find_all('b'))  # [<b>The Dormouse's story</b>]
    # print(Beautifulsoup_PO.soup.find_all('a'))  # [<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
    #
    #
    # print('find_all () 方法搜索当前 tag 的所有 tag 子节点之传正则表达式，适配所有b开头的标签'.center(100, "-"))
    # import re
    # for tag in Beautifulsoup_PO.soup.find_all(re.compile("^b")):
    #     print(tag.name)
    #     print(Beautifulsoup_PO.soup.find_all((tag.name)))
    # # body
    # # [<body>
    # # <p name="dromouse"><b>The Dormouse's story</b></p>
    # # <p class="story">Once upon a time there were three little sisters; and their names were
    # # <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
    # # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
    # # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;and they lived at the bottom of a well.</p>
    # # <p class="story">...</p>
    # # </body>]
    # # b
    # # [<b>The Dormouse's story</b>]
    #
    # print('find_all () 方法搜索当前 tag 的所有 tag 子节点之传列表参数'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.find_all(["a", "b"])) # [<b>The Dormouse's story</b>, <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
    #
    # print('find_all () 方法搜索当前 tag 的所有 tag 子节点之传列表True'.center(100, "-"))
    # for tag in Beautifulsoup_PO.soup.find_all(True):
    #     print(tag.name)
    # # html
    # # head
    # # title
    # # body
    # # p
    # # b
    # # p
    # # a
    # # a
    # # a
    # # p
    #
    # print('find_all () 方法搜索当前 tag 的所有 tag 子节点之传方法，包含class属性却不包含id属性'.center(100, "-"))
    # def hasClassButNoId(tag):
    #     return tag.has_attr('class') and not tag.has_attr('id')
    #
    # print(Beautifulsoup_PO.soup.find_all(hasClassButNoId))
    # # [<p class="story">Once upon a time there were three little sisters; and their names were
    # # <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
    # # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
    # # <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>;and they lived at the bottom of a well.</p>, <p class="story">...</p>]
    #
    #
    #
    # print('find_all () 方法搜索当前 tag 的所有 tag 子节点之传方法keyword参数，'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.find_all(id='link2'))  # [<a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
    # print(Beautifulsoup_PO.soup.find_all(href=re.compile("elsie")))  # [<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
    # print(Beautifulsoup_PO.soup.find_all(href=re.compile("elsie"), id='link1'))  # [<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
    # print(Beautifulsoup_PO.soup.find_all('a', class_='sister'))  # [<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
    # # 注意：由于class是python的关键字，这里要加下划线即class_
    #
    #
    # print('find_all () 方法，HTML5中 data-*属性的标签需使用attrs参数定义字典来搜索包含特殊属性的tag'.center(100, "-"))
    # data_soup = BeautifulSoup('<div data-foo="value">foo!</div>', "lxml")
    # print(data_soup.find_all(attrs={"data-foo" : "value"}))  # [<div data-foo="value">foo!</div>]
    #
    #
    # print('find_all () 方法，text参数搜索文档中字符串内容，不包含注释'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.find_all(text="Lacie"))  # ['Lacie']
    # print(Beautifulsoup_PO.soup.find_all(text="Elsie"))  # []  //Elsie是在注释里的字符串
    # print(Beautifulsoup_PO.soup.find_all(text=re.compile("Dormouse")))  # ["The Dormouse's story", "The Dormouse's story"]
    #
    #
    # print('find_all () 方法，limit参数限制数量'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.find_all("a",limit=2))  # [<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
    #
    #
    # print('find_all () 方法，recursive参数只搜索直接子节点'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.html.find_all("title"))  # [<title>The Dormouse's story</title>]
    # print(Beautifulsoup_PO.soup.html.find_all("title", recursive=False))  # []
    # print(Beautifulsoup_PO.soup.html.find_all("head", recursive=False))  # [<head><title>The Dormouse's story</title></head>]
    # print(Beautifulsoup_PO.soup.html.find_all("head", recursive=True))  # [<head><title>The Dormouse's story</title></head>]
    #
    #
    # print('.select CSS选择器,通过标签名查找'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.select('title'))  # [<title>The Dormouse's story</title>]
    # print(Beautifulsoup_PO.soup.select('a'))  # [<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
    #
    #
    # print('.select CSS选择器,通过类名查找'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.select('.sister'))  # [<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
    #
    # print('.select CSS选择器,通过id查找'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.select('#link1'))  # [<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
    #
    # print('.select CSS选择器,通过组合查找,查找p标签中id等于link1的内容'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.select('p #link1'))  # [<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
    #
    # print('.select CSS选择器,通过组合查找,直接子标签查找'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.select("head > title"))  # [<title>The Dormouse's story</title>]
    #
    #
    # print('.select CSS选择器,标签和属性查找'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.select('a[class="sister"]'))  #[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a class="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
    # print(Beautifulsoup_PO.soup.select('p a[href="http://example.com/elsie"]'))  #[<a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
    #
    #
    # print('.select CSS选择器,get_text () 方法来获取它的内容'.center(100, "-"))
    # soup = BeautifulSoup(html, 'lxml')
    # print(type(Beautifulsoup_PO.soup.select('title')))  #<class 'bs4.element.ResultSet'>
    # print(soup.select('title')[0].get_text())  # The Dormouse's story
    #
    # for t in Beautifulsoup_PO.soup.select('title'):
    #     print(t.get_text())  # The Dormouse's story
    #
    # for t in Beautifulsoup_PO.soup.select('a'):
    #     print(t.get_text())
    # #
    # # Lacie
    # # Tillie


    # print('获取url中div标签中id为post_content_87286618651下img标签中src的值'.center(100, "-"))
    # picUrl = Beautifulsoup_PO.getValue('http://tieba.baidu.com/p/4468445702', "div", 'id', 'post_content_87286618651', "img", "src")
    # print(picUrl)

    # print('将在线图片下载到本地'.center(100, "-"))
    # Beautifulsoup_PO.downPic(picUrl, "d://1/123.jpg")






    # bsop.find('div', {'class': 'img'}).find("p").findAll("img")[0].attrs['alt']

    # Beautifulsoup_PO.getValue2('https://www.ximalaya.com/album/13738175', "span", 'class_', 'title _nO')
    # Beautifulsoup_PO.getValue2("h1", 'class', 'title dC_')
    Beautifulsoup_PO.getValue2("div", 'id', 'anchor_sound_list')
    # Beautifulsoup_PO.getValue2("span", 'class_', 'title _nO')
    # Beautifulsoup_PO.getValue2("", 'class_','title _nO')

