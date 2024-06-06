# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2024-6-6
# Description: yaml
# 不是标记语言,对用户极其友好,数据序列化标准,跨语言,所有编程语言都支持,跨平台,所有平台都支持,Windows、linux、Mac,格式简单,比json小姐姐穿得更少
# yaml文件读取效率非常高
# yaml文件相当适合存放测试数据
# ruamel.yaml模块对yaml文件的操作进一步简化
# yaml在自动化测试和测试开发中都有广泛应用

# pyyaml,应用最广泛,封装的api不够简单,不支持YAML 1.2最新版
# ruamel.yaml,是pyyaml的衍生版,封装的api简单,支持YAML 1.2最新版
# pip install ruamel.yaml
# ********************************************************************************************************************

from ruamel.yaml import YAML

# todo 将Python中的对象转化为yaml格式数据

# 第一步: 创建需要保存的User类
class User:

    def __init__(self, name, age, gender):
        self.name, self.age, self.gender = name, age, gender
        self.lovers = []

    def loved(self, user):
        self.lovers.append(user)


# 第二步: 创建YAML对象
yaml = YAML()

# 第三步: 注册用户类
yaml.register_class(User)

# 第四步: 保存用户对象
keyou = User("可优", 17, "油腻男")
lemon_little_girl = User("柠檬小姐姐", 16, "素颜小仙女")
orange_little_girl = User("橘子小姐姐", 18, "不会PS的靓妹")
keyou.loved(lemon_little_girl)
keyou.loved(orange_little_girl)

with open('lovers.yaml', mode='w', encoding='utf-8') as file:
    yaml.dump([keyou], file)

