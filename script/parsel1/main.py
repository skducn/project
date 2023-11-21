# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-8-31
# Description:
# pip install parsel
# 官方网：https://parsel.readthedocs.io/en/latest/
# 相比于BeautifulSoup，xpath，parsel效率更高，使用更简单。
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

selector = Selector(html)  # 初始化Selector()对象

# get()：将css() 查询到的第一个结果转换为str类型
# getall()：将css() 查询到的结果转换为python的列表


# todo 1, xpath, 获取id为images下的所有a标签
items = selector.xpath('//div[@id="images"]/a')
texts = items.getall()
# print(texts)  # ['<a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg"></a>', '<a href="image2.html">Name: My image 2 <br><img src="image2_thumb.jpg"></a>']
texts = items.get()
# print(texts)  # <a href="image1.html">Name: My image 1 <br><img src="image1_thumb.jpg"></a>
result_text = [item.xpath('./text()').get() for item in items]  # ['Name: My image 1 ', 'Name: My image 2 ']
result_text2 = [item.xpath('./text()').getall() for item in items]  # [['Name: My image 1 '], ['Name: My image 2 ']]
result_href = [item.xpath('./@href').get() for item in items]  # ['image1.html', 'image2.html']


# todo 2, css, 获取id为images下的所有a标签
items = selector.css('#images > a')
result_text = [item.css('::text').get() for item in items]  # ['Name: My image 1 ', 'Name: My image 2 ']
result_href = [item.css('::attr(href)').get() for item in items]  # ['image1.html', 'image2.html']
# print(result_text)
# print(result_href)


# todo 获取图书的信息
with open('./demo.html', 'r', encoding='utf-8') as f:
    html = f.read()
selector = Selector(html)  # 初始化Selector()对象

shop_items = selector.css('.product-list li')
for shop in shop_items:
    shop_name = shop.xpath('.//div[@类与实例="p-name"]/text()').get()  # 商品名称
    shop_href = 'http:' + shop.xpath('./a/@href').get()  # 商品详细链接
    price = shop.xpath('.//div[@类与实例="p-price"]/text()').get()  # 商品价格
    shop_price = shop.xpath('.//div[@类与实例="p-price"]/text()').re('\d+\D\d+')[0]  # 商品价格

    print(shop_name)
    print(shop_href)
    print(price)
    print(shop_price)
    print('\n')


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

