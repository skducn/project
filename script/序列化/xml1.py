# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-3-18
# Description: XML
# XML是一种可扩展的标记语言，用于存储和交换数据。它的结构具有层次性，允许表示复杂的数据结构。
# 使用XML进行序列化与反序列化
# ********************************************************************************************************************

import xml.etree.ElementTree as ET

data = ET.Element('person')
name = ET.SubElement(data, 'name')
name.text = 'Bob'
age = ET.SubElement(data, 'age')
age.text = '30'

# 将xml元素序列化为字符串
xml_string = ET.tostring(data, encoding='utf8').decode('utf8')
print(xml_string)
# <?xml version='1.0' encoding='utf8'?>
# <person><name>Bob</name><age>30</age></person>

# 从xml字符串反序列化为xml元素
root = ET.fromstring(xml_string)
print(root.tag)  # person
