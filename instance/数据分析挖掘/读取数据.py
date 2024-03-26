# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2024-3-20
# Description: 读取数据
# https://pandas.pydata.org/docs/user_guide/io.html
# ********************************************************************************************************************

import pandas as pd

# print(pd.__version__)  # 1.5.3

# todo read_excel()
# # 读取excel文件（100多万数据量）
# df = pd.read_excel('test.xlsx', sheet_name='interface')
# print(df.head())
#
# # 另存为文件
# df.to_excel('test2.xlsx', sheet_name='interface')
# df.to_excel('test3.xlsx', sheet_name='interface', index=False)
#
# # 保存多个副本
# writer = pd.ExcelWriter('test4.xlsx')
# df.to_excel(writer, sheet_name='interface1')
# df.to_excel(writer, sheet_name='interface2')
# writer.close()   # close()方法会调用save()


# todo read_csv()
# 打开txt、csv文件(一般是以英文富豪逗号"，"为数据分隔符)
# df = pd.read_csv('sales_data1.csv')
# print(df.head())

# # 另存为文件，相当于mode='w', 默认模式
# df.to_csv('sales_data2.csv')

# # 追加模式另存为文件，默认带表头
# df.to_csv('sales_data1.csv', mode='a')

# # 不带表头追加模式另存为文件
# df.to_csv('sales_data2.csv', mode='a', header=None)

# 参数header，设置表头，索引从0开始
# header=None，表示不需要表头，第一行开始为数据
# header=0，表示表格第一行设为表头，第二行开始为数据
# header=1，表示表格第二行设为表头，第一行数据忽略，第三行开始为数据
# header=[0,1]，符合表头，表示表头为表格第一行和第二行，第三行开始为数据

# 参数names，重新设置表头名称，如 names=['a','b','c]
# 参数index_col，设置索引列，默认为None，索引从0开始，如 index_col='0' 或 index_col='手机号'，将某列设置为索引列。
# 参数usecols，设置读取的列，如 usecols=[0，2，4] 或 usecols=['手机号','姓名']，只读取这列数据。
# 参数chunksize，数据的分段读取
# 如将数据按照1000条分段读取
df = pd.read_csv('sales_data.csv', chunksize=1000)
print(df)  # <pandas.io.parsers.readers.TextFileReader object at 0x7fd87a210b80>
chunk = []
for c in df:
    print(c.shape)  # (1000, 24)、(1000, 24)、(823, 24)
    # 这里可以对1000行数据进行处理
    chunk.append(c)
# 合并分段读取的数据
df_all = pd.concat(chunk, axis=0)  # axis=1 表示纵向合并，axis=0 表示横向合并(每行)
print(df_all.shape)  # (2823, 24)

# 参数iterator，也是数据的分段读取
df = pd.read_csv('sales_data.csv', iterator=True)
print(df)  # <pandas.io.parsers.readers.TextFileReader object at 0x7fd7e4ef7a30>  迭代器
chunks = []
while True:
    try:
        reader = df.get_chunk(2000)
        print(reader.shape)  # # (2000, 24)、(823, 24)
        # 这里可以对2000行数据进行处理
        chunks.append(reader)
    except:
        break
df_all = pd.concat(chunks, axis=0)
print(df_all.shape)  # (2823, 24)







# from pandasai import PandasAI
#
# from pandasai.llm.openai import OpenAI
# llm = OpenAI()
# pandas_ai = PandasAI(llm, conversational=True, verbose=False)
# pandas_ai.clear_cache()
#
# df = pd.read_excel('test.xlsx', sheet_name='interface')
#
# result = pandas_ai(df, '我想知道每位代表的计划拜访人')
# print(result)