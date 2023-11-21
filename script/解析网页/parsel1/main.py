# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-8-31
# Description: parsel 网页解析
# parsel 这个库可以解析 HTML 和XML，并支持使用 XPath 和 CSS 选择器对内容进行提取和修改，同时还融合了正则表达式的提取功能。parsel灵活且强大，同时也是 Python 最流行的爬虫框架 Scrapy的底层支持
# pip install parsel
# 官网：https://parsel.readthedocs.io/en/latest/
# 相比于BeautifulSoup，xpath，parsel 效率更高，使用更简单。
# get()：获取查询到的第一个结果（str类型）
# getall()：获取查询到的所有结果（list类型）
# https://blog.csdn.net/W_chuanqi/article/details/126003672
#***************************************************************

from parsel import Selector

html = '''
<html>
 <head>
  <base href='http://example.com/' />
  <title>Example website</title>
 </head>
 <body>
  <div id='images'>
   <a href='image1.html'>Name: My image 1 <br /><img src='image1_thumb.jpg' /></a>
   <a href='image2.html'>Name: My image 2 <br /><img src='image2_thumb.jpg' /></a>
  </div>
 </body>
</html>
'''

# 初始化Selector()对象
selector = Selector(html)

# todo 获取id为images下的a标签
items = selector.xpath('//div[@id="images"]/a')
texts = items.getall()
print(texts)  # ['<a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg"></a>', '<a href="image2.html">Name: My image 2 <br><img src="image2_thumb.jpg"></a>']
texts = items.get()
print(texts)  # <a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg"></a>

print([item.xpath('./text()').get() for item in items])  # ['Name: My image 1 ', 'Name: My image 2 ']
print([item.xpath('./text()').getall() for item in items])  # [['Name: My image 1 '], ['Name: My image 2 ']]
print([item.xpath('./@href').get() for item in items])  # ['image1.html', 'image2.html']


# todo 获取id为images下的a标签
items = selector.css('#images > a')
print([item.css('::text').get() for item in items])  # ['Name: My image 1 ', 'Name: My image 2 ']
print([item.css('::attr(href)').get() for item in items])  # ['image1.html', 'image2.html']


# todo 获取图书的信息
with open('demo.html', 'r', encoding='utf-8') as f:
    html = f.read()
selector = Selector(html)  # 初始化Selector()对象

shop_items = selector.css('.product-list li')
for shop in shop_items:
    shop_name = shop.xpath('.//div[@class="p-name"]/text()').get()  # 商品名称
    shop_href = 'http:' + shop.xpath('./a/@href').get()  # 商品详细链接
    price = shop.xpath('.//div[@class="p-price"]/text()').get()  # 商品价格
    shop_price = shop.xpath('.//div[@class="p-price"]/text()').re('\d+\D\d+')[0]  # 商品价格
    print(shop_name)
    print(shop_href)
    print(price)
    print(shop_price)

# 运行结果
# 创晟 泰国进口金枕头榴莲水果 1个2-2.5kg
# http://item.jd.com/16239208399.html
# ¥148.80
# 148.80
#
# 巴拜苏打泉 天然苏打水无气泡弱碱性水 非饮料 饮用水 420ml*12瓶/箱 整箱装
# http://item.jd.com/4838701.html
# ¥69.00
# 69.00
#
# 洁云 雅致生活抽纸 200抽软包面巾纸*8包（新老包装交替发货）
# http://item.jd.com/915074.html
# ¥19.90
# 19.90
#
# 康师傅 方便面 劲爽香辣牛肉面 12入桶装泡面【整箱装】
# http://item.jd.com/100002327718.html
# ¥37.00
# 37.00
#
# 宏辉果蔬 烟台红富士苹果 5kg 一级铂金果 单果190-240g 新鲜水果
# http://item.jd.com/6281974.html
# ¥119.90
# 119.90

