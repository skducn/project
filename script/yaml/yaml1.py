# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2024-6-6
# Description: yaml
# 不是标记语言(所以它强调的是数据本身，而不是以标记为重点。),对用户极其友好,数据序列化标准,跨语言,所有编程语言都支持,跨平台,所有平台都支持,Windows、linux、Mac,格式简单,比json小姐姐穿得更少
# yaml文件读取效率非常高
# yaml文件相当适合存放测试数据
# ruamel.yaml模块对yaml文件的操作进一步简化
# yaml在自动化测试和测试开发中都有广泛应用

# pyyaml,应用最广泛,封装的api不够简单,不支持YAML 1.2最新版
# ruamel.yaml,是pyyaml的衍生版,封装的api简单,支持YAML 1.2最新版
# pip install ruamel.yaml
# ********************************************************************************************************************

from ruamel.yaml import YAML


# todo 将yaml格式的数据转化为python中的数据类型

# 第一步: 创建YAML对象
yaml = YAML(typ='safe')
# typ: 选择解析yaml的方式
#  'rt'/None -> RoundTripLoader/RoundTripDumper(默认)
#  'safe'    -> SafeLoader/SafeDumper,
#  'unsafe'  -> normal/unsafe Loader/Dumper
#  'base'    -> baseloader

# 第二步: 读取yaml格式的文件
with open('user_info.yaml', encoding='utf-8') as file:
    data = yaml.load(file)  # 为列表类型

print(data)  # {'user': ['可优', 'keyou', '小可可', '小优优'], 'lovers': ['柠檬小姐姐', '橘子小姐姐']}



# todo 将Python中的字典或者列表转化为yaml格式的数据

# 第一步: 创建YAML对象
# yaml = YAML(typ='safe')
yaml = YAML()

# 第二步: 将Python中的字典类型数据转化为yaml格式的数据
src_data = {'user': {'name': '可优', 'age': 17, 'money': None, 'gender': True},
            'lovers': ['柠檬小姐姐', '橘子小姐姐', '小可可']
            }

with open('new_user_info.yaml', mode='w', encoding='utf-8') as file:
    yaml.dump(src_data, file)



