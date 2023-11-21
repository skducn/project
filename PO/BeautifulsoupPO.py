# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2020-12-30
# Description: beautifulsoup  HTML 解析器 封装包
# beautifulsoup官网：https://beautifulsoup.readthedocs.io/zh_CN/latest/
# 使用方法：https://cuiqingcai.com/1319.html
# 官网 https://www.crummy.com/software/BeautifulSoup/bs4/doc/#next-sibling-and-previous-sibling
# bs4查找标签属性值 https://blog.csdn.net/qq_45060674/article/details/118671494
# Selenium+BeautifulSoup解析动态HTML页面【附完整代码】 https://blog.csdn.net/weixin_44259720/article/details/127075628

# 三个html解释器比较：
# pip3.9 install beautifulsoup4  特点：Python 的内置标准库，执行速度适中，文档容错能力强，Python 2.7.3 or 3.2.2) 前 的版本中文档容错能力差；
# pip3.9 install lxml  lxml 特点：速度快，文档容错能力强，需要安装 C 语言库，推荐安装；
# pip3.9 install html5lib , 特点：最好的容错性，以浏览器的方式解析文档，生成 HTML5 格式的文档，速度慢，不依赖外部扩展；

# Beautiful Soup四大对象：
# Tag，HTML 中的一个个标签，如<title>The Dormouse's story</title> 中的title标签
# NavigableString，获取标签内容
# BeautifulSoup，表示的是一个文档的全部内容，它是一个特色Tag对象，可获取 类型，名称，属性
# Comment，是文档中的备注类型，它是一个特殊类型的 NavigableString ，输出注释内容，但不输注释符号，如 注释<!-- Elsie -->，输出 Elsie
# ***************************************************************

"""

1 获取标签属性的值
2 获取标签的文本内容

"""


import requests
from bs4 import BeautifulSoup

from PO.HttpPO import *
Http_PO = HttpPO()


class BeautifulsoupPO:

    def __init__(self, url):

        html = Http_PO.getHtml(url)
        # self.soup = BeautifulSoup(html.text, "html.parser")
        self.soup = BeautifulSoup(html, 'lxml')

    # print(soup.span.string)

    # return self.soup.find_all(tag1).attrs['title']

    # self.soup.span.string
    # print(l_value)
    # return l_value[0].attrs[attr2]

    # x = Beautifulsoup_PO.getValue2("h1", 'class_', 'core_title_txt  ')

    # for s in self.soup.stripped_strings:
    #     print(repr(s))
    # l_value = self.soup.find_all('ul')
    # l_value = self.soup.find_all('div', {'类与实例': 'text _nO'})

    # .find_all("a").attrs['title']
    #
    #
    # findAll("")[0].attrs['alt']
    # print(l_value)


if __name__ == "__main__":

    html = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p 类与实例="title" name="dromouse"><b>The Dormouse's story</b></p>
    <p 类与实例="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" 类与实例="sister" id="link1"><!-- Elsie --></a>,
    <a href="http://example.com/lacie" 类与实例="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" 类与实例="sister" id="link3">Tillie</a>;and they lived at the bottom of a well.</p>
    <p 类与实例="story">...</p>
    """

    # soup = BeautifulSoup(open('./data/video76932809__.mhtml', encoding="utf-8"), 'lxml')
    soup = BeautifulSoup(open('./data/video76932809__.mhtml'),  'html.parser')
    # print(soup.text)
    # print(soup.original_encoding)
    # print(soup.title).encode('gb18030')
    #
    # print(soup.originalEncoding)
    # print(soup.prettify())
    # print(soup.title).encode('gb18030')

    # 文件名
    setVideoTitle = soup.text.split("html5player.setVideoTitle('")[1].split("')")[0]
    print(setVideoTitle)

    setVideoHLS = soup.text.split("html5player.setVideoHLS(")[1].split(')')[0]
    # print(setVideoHLS)
    url = setVideoHLS.replace("'htt=\nps:", "https:").replace("\n", "").replace("hls.m3u8'", "")
    print(url + "test.html")

    setUploaderName = soup.text.split("html5player.setUploaderName('")[1].split("')")[0]
    print(setUploaderName)

    setVideoURL = soup.text.split("html5player.setVideoURL('")[1].split("')")[0]
    print(setVideoURL)


    # print(soup.find_all('script'))
    # print(soup.head.script)


    # Beautifulsoup_PO = BeautifulsoupPO(open("y.html", encoding='utf-8'))

    # Beautifulsoup_PO = BeautifulsoupPO("https://wall.alphacoders.com/by_resolution.php?w=3840&h=2160&lang=Chinese&page=3")
    # print(Beautifulsoup_PO.soup.find_all('a'))
    # for link in Beautifulsoup_PO.soup.find_all('a'):
    #     print(link.get('href'))

    # img_list = Beautifulsoup_PO.soup.find_all("a").attrs['href']
    # print(img_list)

    # # # print('1,获取标签属性的值, 获取div id=post_content_87286618651下img src的值'.center(100, "-"))
    # Beautifulsoup_PO = BeautifulsoupPO("http://tieba.baidu.com/p/4468445702")
    # x = Beautifulsoup_PO.soup.find("div", {'id': 'post_content_87286618651'}).find_all('img')[0].attrs['src']
    # print(x)  # https://imgsa.baidu.com/forum/w%3D580/sign=b2310eb7be389b5038ffe05ab534e5f1/680c676d55fbb2fbc7f64cbb484a20a44423dc98.jpg

    #
    #
    # # print('2 获取标签的文本内容'.center(100, "-"))
    # x = Beautifulsoup_PO.soup.find_all("h1", {'类与实例':'core_title_txt'})
    # print(x[0].text)  # 为什么pycharm显示找不到reduce函数？如图
    #
    # x = Beautifulsoup_PO.soup.find("h1", {'类与实例':'core_title_txt'}).contents[0]
    # print(x)  # 为什么pycharm显示找不到reduce函数？如图

    # print('3 格式化html'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.prettify())

    # print('4 获取所有文本内容，并去除多余空白内容，即换行符。'.center(100, "-"))
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

    # print('获取标签及内容（默认获取第一个标签）'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.title)  # <title>The Dormouse's story</title>
    # print(Beautifulsoup_PO.soup.head)  # <head><title>The Dormouse's story</title></head>
    # print(Beautifulsoup_PO.soup.img)  # <a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>
    # print(Beautifulsoup_PO.soup.p)  # <p 类与实例="title" name="dromouse"><b>The Dormouse's story</b></p>
    #
    #
    # print('标签类型是Tag'.center(100, "-"))
    # print(type(Beautifulsoup_PO.soup.a))  # <类与实例 'bs4.element.Tag'>
    #
    #
    # print('标签属性name和attrs'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.name)  # [document]  ，soup 对象的 name 即为 [document]，对于其他内部标签，输出的值便为标签本身的名称。
    # print(Beautifulsoup_PO.soup.head.name)  # head
    # print(Beautifulsoup_PO.soup.img.attrs)  # {'类与实例': ['title'], 'name': 'dromouse'} , 将标签中的属性转为字典，即可获取key或value
    #
    #
    # print('获取标签中属性的值'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.p.get('类与实例'))  # ['title'] , 通过get获取值
    # print(Beautifulsoup_PO.soup.p['类与实例'])  # ['title']
    #
    #
    # print('修改标签中属性的值'.center(100, "-"))
    # Beautifulsoup_PO.soup.p['类与实例'] = "newClass"  # 修改class的值
    # print(Beautifulsoup_PO.soup.p['类与实例'])  # newClass
    # print(Beautifulsoup_PO.soup.p)  # <p 类与实例="newClass" name="dromouse"><b>The Dormouse's story</b></p>
    #
    #
    # print('删除标签中属性的值'.center(100, "-"))
    # del Beautifulsoup_PO.soup.p['类与实例']
    # print(Beautifulsoup_PO.soup.p)  # <p name="dromouse"><b>The Dormouse's story</b></p>
    # print(Beautifulsoup_PO.soup.video)  # <p name="dromouse"><b>The Dormouse's story</b></p>
    #
    #
    # print('获取标签内容'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.p.string)  # The Dormouse's story
    # print(type(Beautifulsoup_PO.soup.p.string))  # <类与实例 'bs4.element.NavigableString'>
    #
    #
    # print('BeautifulSoup 对象表示的是一个文档的全部内容'.center(100, "-"))
    # print(type(Beautifulsoup_PO.soup.name))  # <类与实例 'str'> , 获取name的类型
    # print(Beautifulsoup_PO.soup.name)  # [document] ， 获取name名称
    # print(Beautifulsoup_PO.soup.attrs)  # {}，获取soup属性，空字典
    #
    #
    # print('标签a的值是注释，但也被作为值输出'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.a)  # <a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>
    # print(Beautifulsoup_PO.soup.a.string)  #  Elsie
    # print(type(Beautifulsoup_PO.soup.a.string))  # <类与实例 'bs4.element.Comment'> ， 对比一下soup.p.string 这个是NavigableString对象，而soup.a.string是Comment对象，只因为a的值是注释；
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
    # # <p 类与实例="story">Once upon a time there were three little sisters; and their names were
    # # <a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
    # # <a 类与实例="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
    # # <a 类与实例="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
    # # and they lived at the bottom of a well.</p>
    # #
    # #
    # # <p 类与实例="story">...</p>
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
    # # <p 类与实例="story">Once upon a time there were three little sisters; and their names were
    # # <a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
    # # <a 类与实例="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
    # # <a 类与实例="sister" href="http://example.com/tillie" id="link3">Tillie</a>;
    # # and they lived at the bottom of a well.</p>
    #
    # print('.next_siblings .prev_siblings 属性 获取前后迭代节点 '.center(100, "-"))
    # for sibling in Beautifulsoup_PO.soup.a.next_siblings:
    #     print(repr(sibling))
    # # ',\n'
    # # <a 类与实例="sister" href="http://example.com/lacie" id="link2">Lacie</a>
    # # ' and\n'
    # # <a 类与实例="sister" href="http://example.com/tillie" id="link3">Tillie</a>
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
    # # <p 类与实例="story">Once upon a time there were three little sisters; and their names were
    # # <a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
    # # <a 类与实例="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
    # # <a 类与实例="sister" href="http://example.com/tillie" id="link3">Tillie</a>;and they lived at the bottom of a well.</p>
    # # <p 类与实例="story">...</p>
    # # </body></html>
    #
    #
    # print('.next_elements .previous_elements 属性 获取所有迭代节点 '.center(100, "-"))
    # for ele in Beautifulsoup_PO.soup.a.next_elements:
    #     print(repr(ele))
    # # ' Elsie '
    # # ',\n'
    # # <a 类与实例="sister" href="http://example.com/lacie" id="link2">Lacie</a>
    # # 'Lacie'
    # # ' and\n'
    # # <a 类与实例="sister" href="http://example.com/tillie" id="link3">Tillie</a>
    # # 'Tillie'
    # # ';and they lived at the bottom of a well.'
    # # '\n'
    # # <p 类与实例="story">...</p>
    # # '...'
    # # '\n'
    #
    #
    #
    # print('find_all () 方法搜索当前 tag 的所有 tag 子节点之传标签名'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.find_all('video'))  # [<b>The Dormouse's story</b>]
    # print(Beautifulsoup_PO.soup.find_all('b'))  # [<b>The Dormouse's story</b>]
    # print(Beautifulsoup_PO.soup.find_all('a'))  # [<a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a 类与实例="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a 类与实例="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
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
    # # <p 类与实例="story">Once upon a time there were three little sisters; and their names were
    # # <a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
    # # <a 类与实例="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
    # # <a 类与实例="sister" href="http://example.com/tillie" id="link3">Tillie</a>;and they lived at the bottom of a well.</p>
    # # <p 类与实例="story">...</p>
    # # </body>]
    # # b
    # # [<b>The Dormouse's story</b>]
    #
    # print('find_all () 方法搜索当前 tag 的所有 tag 子节点之传列表参数'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.find_all(["a", "b"])) # [<b>The Dormouse's story</b>, <a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a 类与实例="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a 类与实例="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
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
    #     return tag.has_attr('类与实例') and not tag.has_attr('id')
    #
    # print(Beautifulsoup_PO.soup.find_all(hasClassButNoId))
    # # [<p 类与实例="story">Once upon a time there were three little sisters; and their names were
    # # <a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>,
    # # <a 类与实例="sister" href="http://example.com/lacie" id="link2">Lacie</a> and
    # # <a 类与实例="sister" href="http://example.com/tillie" id="link3">Tillie</a>;and they lived at the bottom of a well.</p>, <p 类与实例="story">...</p>]
    #
    #
    #
    # print('find_all () 方法搜索当前 tag 的所有 tag 子节点之传方法keyword参数，'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.find_all(id='link2'))  # [<a 类与实例="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
    # print(Beautifulsoup_PO.soup.find_all(href=re.compile("elsie")))  # [<a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
    # print(Beautifulsoup_PO.soup.find_all(href=re.compile("elsie"), id='link1'))  # [<a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
    # print(Beautifulsoup_PO.soup.find_all('a', class_='sister'))  # [<a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a 类与实例="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a 类与实例="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
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
    # print(Beautifulsoup_PO.soup.find_all("a",limit=2))  # [<a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a 类与实例="sister" href="http://example.com/lacie" id="link2">Lacie</a>]
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
    # print(Beautifulsoup_PO.soup.select('a'))  # [<a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a 类与实例="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a 类与实例="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
    #
    #
    # print('.select CSS选择器,通过类名查找'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.select('.sister'))  # [<a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a 类与实例="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a 类与实例="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
    #
    # print('.select CSS选择器,通过id查找'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.select('#link1'))  # [<a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
    #
    # print('.select CSS选择器,通过组合查找,查找p标签中id等于link1的内容'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.select('p #link1'))  # [<a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
    #
    # print('.select CSS选择器,通过组合查找,直接子标签查找'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.select("head > title"))  # [<title>The Dormouse's story</title>]
    #
    #
    # print('.select CSS选择器,标签和属性查找'.center(100, "-"))
    # print(Beautifulsoup_PO.soup.select('a[类与实例="sister"]'))  #[<a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>, <a 类与实例="sister" href="http://example.com/lacie" id="link2">Lacie</a>, <a 类与实例="sister" href="http://example.com/tillie" id="link3">Tillie</a>]
    # print(Beautifulsoup_PO.soup.select('p a[href="http://example.com/elsie"]'))  #[<a 类与实例="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>]
    #
    #
    # print('.select CSS选择器,get_text () 方法来获取它的内容'.center(100, "-"))
    # soup = BeautifulSoup(html, 'lxml')
    # print(type(Beautifulsoup_PO.soup.select('title')))  #<类与实例 'bs4.element.ResultSet'>
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

    # bsop.find('div', {'类与实例': 'img'}).find("p").findAll("img")[0].attrs['alt']
