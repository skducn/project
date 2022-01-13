#!/usr/bin/env python
# coding: utf-8

# In[1]:


# pi3 install jupyter
# pip3 install numpy 
# pip3 install pandas
# 启动 jupyter 
# 在工作目录下启动 jupyte notebook

# numpy 数学库，用于数组计算（一维、二维、多维），对list进行部分封装。提供了非常便利的科学运算功能
# 官网：https://numpy.org/doc/stable/reference/

# pandas 侧重于数据处理，清洗
# pandas用户指南，https://pandas.pydata.org/docs/user_guide/index.html
# Shift + 回车  //执行
# all + 回车

import numpy as np
import pandas as pd 


# In[4]:


# a = np.array()   # 报错，选中 array() 按 shift + tab ,显示函数array参数信息，便于定位或修改。
a = np.array([1,2,3,4])
a


# In[18]:


np.array([[1,2],[3,4],[5,6]])


# In[9]:


b = np.array([[[1,2],[3,4],[5,6]]])
b.ndim  # 查看数据维度


# In[24]:


b.dtype


# In[25]:


np.arange(10)


# In[26]:


np.linspace(0,2,11)


# In[28]:


np.random.randn(6,4)


# In[31]:


### pandas 简介
# - 是一个专注于数据处理的一个库
# - 可以帮助数据分析、数据挖掘、算法工程师的人员其高耸的姐姐数据预处理的问题
# Pandas模块的数据结构主要有两种：1.Series 2.DataFrame
###


# In[10]:


# Series 是一维数组，基于Numpy的ndarray 结构
# Series([data, index, dtype, name, copy, …])	
obj = pd.Series([1,2,3,4,5,np.nan])
obj


# In[37]:


obj[0]


# In[38]:


obj.index


# In[25]:


# 通过索引号获取元素，这里2个中括号中的是索引号
obj[[0,2,4]]  


# In[32]:


d = {'a':10,'b':20,'c':30,'d':40,'e':50}
d = pd.Series(d)
d


# In[22]:


d.values


# In[34]:


# 通过key获取值
d["a"]


# In[35]:


# 通过索引号获取值
d[2]


# In[39]:


# 显示列表的索引号与类型
d.index


# In[54]:


index = ['Bob', 'Steve', 'Jeff', 'Ryan', 'Jeff', 'Ryan'] 
a = pd.Series([4, 7, -5, 3, 7, np.nan],index = index)
# obj.value_counts()
a


# In[55]:


a.value_counts()


# In[68]:


a1 = a.value_counts()
a1[-5.0]


# In[73]:


a1.index


# In[74]:


a.sort_values()


# In[77]:


a.sort_values(ascending=False)


# In[80]:


a.rank(method='first')


# In[ ]:





# In[81]:


obj2 = pd.Series({"姓名":"张三","年龄":"12"})
obj2


# In[40]:


obj2["姓名"]


# In[43]:


obj2[["姓名","年龄"]]


# In[45]:


obj3 = pd.Series(["夏雨荷","山东",19],index=["姓名","地址","年龄"])
obj3


# In[56]:


# pandas结合这Numpy来进行数学运算
number1 = pd.Series([4,8,16,32])
np.log2(number1)  # 对数运算
a = np.log2(number1)  # 对数运算
type(a)


# In[55]:


# dataFrame
df1 = pd.DataFrame([["张无忌",24,"男"],["谢逊",54,"男"],["周芷若",16,"女"]])
df1


# In[58]:


# 使用字典进行构造
data = {
    "人物":["张三丰","张无忌","张翠山"],
    "风景":["武当山","桃花岛","冰火岛"]
}
df2 = pd.DataFrame(data)
df2


# In[59]:


df2["人物"]


# In[60]:


df2["人物"][1]


# In[61]:


np_data = [["张无忌",24,"男"],["谢逊",54,"男"],["周芷若",16,"女"]]
df3 = pd.DataFrame(np_data)
df3


# In[21]:


# 读取csv文件
pd.read_csv("data.csv")


# In[23]:


# 将第一行标题作为数据
pd.read_csv("data.csv", header=None)


# In[77]:


# 指定c这列作为索引
pd.read_csv("data.csv",index_col='c')


# In[78]:


a = pd.read_csv("data.csv",index_col='c')
type(a)


# In[79]:


pd.read_csv("data.csv", header=None)[0][0]


# In[85]:


# 行列数
csv = pd.read_csv("data.csv")
csv.shape


# In[86]:


# 每一列的数据类型
csv.dtypes 


# In[87]:


# 显示b列的数据及类型
csv.b


# In[89]:


# 数据统计性描述
csv.describe()


# In[91]:


dates = pd.date_range("20201127",periods=6)
dates


# In[93]:


# 随机生成6行4列的随机数，索引号显示dates的日期，列名显示ABCD
df = pd.DataFrame(np.random.rand(6,4),index=dates,columns=list("ABCD"))
df


# In[94]:


# 转置，行列切换（与93对比一下）
df.T


# In[95]:


# 显示区间里的记录
df["2020-11-27":"2020-11-29"]


# In[96]:


# 对列进行筛选
df.loc["2020-11-27":"2020-11-29",["A","B"]]


# In[97]:


# at对行列值的选择
df.at[dates[0],"A"]


# In[100]:


df.at[dates[1],"B"]


# In[101]:


# 显示头部N条记录
df.head(2)


# In[102]:


# 显示尾部N条记录
df.tail(3)


# In[24]:


# pandas 重新索引
obj = pd.Series([4.5,9.4,-2.3],index=["a","b","c"])
obj


# In[107]:


# NaN表示空，表示某个索引不存在，缺省值NaN
obj_1 = obj.reindex(["a","b","c","d","e"])
obj_1


# In[25]:


# 对缺省值设置默认值，如0
obj_1 = obj.reindex(["a","b","c","d","e"], fill_value=0)
obj_1


# In[39]:


# 旅游网站数据清洗实战
df = pd.read_csv("icd.csv",index_col=0)   # 去掉索引
df.head()


# In[28]:


df.shape


# In[126]:


df.info()


# In[136]:


df.describe()


# In[140]:


# 把所有的列列出来
# 注意部分列名前后有多余的空格
df.columns


# In[141]:


df.columns.values


# In[29]:


col = df.columns.values
col[0].strip()


# In[30]:


# 批量清除列名前后空格
df.columns = [x.strip() for x in col]
df.columns.values


# In[40]:


# 统计重复值，true表示重复
df.duplicated()


# In[41]:


# 统计重复值的数量
df.duplicated().sum()


# In[42]:


# 显示重复的记录
df[df.duplicated()]


# In[50]:


# 删除重复数据（上次记录数量 Length: 23088, dtype: bool） - 重复28条， 应该是 23060
# df.drop_duplicates()  # 显示重复待删除的记录
df.drop_duplicates(inplace=True)  # 执行删除操作（不显示记录）


# In[61]:


df.duplicated().sum()


# In[62]:


df.shape


# In[63]:


# 删除重复记录后，index则变成不连续
df.index


# In[59]:


# 重新让index连续
df.index=range(df.shape[0])


# In[64]:


df.index


# In[155]:


# 处理异常值
# 旅游网站数据清洗实战
# df = pd.read_csv("tr.csv",index_col=0)   # 去掉索引
df = pd.read_csv("tr.csv")  
df


# In[156]:


df.describe().T


# In[157]:


df["价格"].std()


# In[158]:


df["价格"].sum()/df["价格"].count()


# In[159]:


df["价格"]-df["价格"].mean()


# In[160]:


# 数据减去平均数除以标准差的值称为“标准分数（standard score）”
sta = (df["价格"]-df["价格"].mean())/df["价格"].std()
sta


# In[161]:


# 数据清洗规则，对价格翻一翻的记录做清洗。
# df[sta.abs()]
df[sta.abs()>2]


# In[163]:


# 还有一种情况是节省>价格也是不正常的，需要清洗
df[df.节省>df.价格]


# In[164]:


# 将两种异常数据进行拼接一下，便于一起处理
pd.concat([df[sta.abs()>2],df[df.节省>df.价格]])


# In[165]:


# 获取4条记录的索引号
del_index = pd.concat([df[sta.abs()>2],df[df.节省>df.价格]]).index
del_index


# In[168]:


# 删除记录
# 删除表中的某一行或者某一列更明智的方法是使用drop，它不改变原有的df中的数据，而是可选择性的返回另一个dataframe来存放删除后的数据。
# df.drop(del_index)  # 显示删除后记录（未删除）
df.drop(del_index, inplace=True)  # 执行删除


# In[169]:


df.shape


# In[170]:


df


# # 查看缺失值
# -df.isnull() 查看缺失值
# -df.notnull() 查看不为空
# -df.dropnd() Fillna填充缺失数据
# -df.fillna()

# In[171]:


df.isnull()


# In[172]:


df.isnull().sum()


# In[173]:


df.notnull()


# In[174]:


df.notnull().sum()


# In[175]:


df[df.价格.isnull()]


# In[352]:


# 修改缺失值
df = pd.read_csv("tr.csv")  
df


# In[353]:


df[df.出发地.isnull()]


# In[354]:


df.loc[df.出发地.isnull(),"路线名"]


# In[355]:


[str(x).split("-")[0] for x in df.loc[df.出发地.isnull(),"路线名"]]


# In[356]:


df.loc[df.出发地.isnull(),"出发地"] = [str(x).split("-")[0] for x in df.loc[df.出发地.isnull(),"路线名"]]


# In[357]:


df


# In[358]:


str(df.loc[df.目的地.isnull(),"路线名"].values)


# In[359]:


# 通过正则表达式获取目的地？
re.findall("-(.*)\d天","['江苏-四川4天3夜']") 
# x[0]
# re.findall("(.*)\d",x[0])[0]


# In[360]:


str(df.loc[df.目的地.isnull(),"路线名"].values).split("-")[1]


# In[361]:


tmp = Str_PO.indexNumber(str(df.loc[df.目的地.isnull(),"路线名"].values).split("-")[1])
tmp


# In[362]:


tmp[0][1]


# In[363]:


[str(x).split("-")[1] for x in df.loc[df.目的地.isnull(),"路线名"]][0][:tmp[0][1]]


# In[364]:


df.loc[df.目的地.isnull(),"目的地"] = [str(x).split("-")[1] for x in df.loc[df.目的地.isnull(),"路线名"]][0][:tmp[0][1]]


# In[365]:


df[df.目的地.isnull()]


# In[366]:


df


# In[367]:


df.describe().T


# In[368]:


round(df['价格'].mean(),0)


# In[369]:


# 将平均价格填充价格缺失值
df['价格'].fillna(round(df['价格'].mean(),0),inplace=True)


# In[370]:


df


# In[371]:


df["几天几夜"] = df.路线名.str.extract("(\d天\d夜)",expand=False)


# In[372]:


df["几天几夜"] 


# In[374]:


df


# In[375]:


df.to_csv("tr2.csv")


# In[ ]:




