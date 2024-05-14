# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2024-5-14
# Description: 多线程，并行处理文件,加速文件读取与操作。
# *****************************************************************

from concurrent.futures import ThreadPoolExecutor
def process_file(file):
    # 假设这是处理文件的函数
    f = open(file, "r")
    content = f.read()
    print(content)


files = ['file1.txt', 'file2.txt']

with ThreadPoolExecutor() as executor:
    executor.map(process_file, files)


# from datetime import datetime
# now = datetime.now()
# formatted = now.strftime("%Y-%m-%d %H:%M:%S")
# print(formatted)


list1 = [1, 5, 3]
list2 = [4, 5, 6]
print(list1)  # 等同于 [*list1]
print(*list1)  # 1 5 3
# print([*list1]) # [1, 5, 3]
combined = [*list1, *list2]
print(combined) # [1, 5, 3, 4, 5, 6]


my_dict = {'banana': 1, 'apple': 3, 'cherry': 2}
sorted_dict = dict(sorted(my_dict.items(), key=lambda x: x[0]))  # 对键排序
print(sorted_dict)
sorted_dict = dict(sorted(my_dict.items(), key=lambda x: x[1]))  # 对值排序
print(sorted_dict)

print(my_dict.items())




