# coding: utf-8
# ***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: ymal
# 两种方式读写yaml：

# 1，python自带的 PyYAML，安装：pip3 install PyYAML
# PyYAML的官方APi文档 http://pyyaml.org/wiki/PyYAMLDocumentation

# 2，ruamel.yaml包，它在PyYAML上进行了一些改进，安装 pip3 install ruamel.yaml
# ruamel.yaml的API文档[https://yaml.readthedocs.io/en/latest/overview.html]

# Yaml语法检查， http://www.yamllint.com/


# ***************************************************************

"""
1 将字典保存到yaml文件中（覆盖）
2 读取yaml文件中的值
3 编辑yaml文件中的值并保存
"""

from ruamel.yaml import YAML
yaml = YAML()


class YamlPO:

    # 1，将字典保存到yaml文件中（覆盖）
    def dict2yaml(self, varYamlFile, varDict):
        # 重写 yaml （删除原先的内容）
        with open(varYamlFile, "w+", encoding="utf-8") as f:
            yaml.dump(varDict, f)

    # 2，读取yaml文件中的值
    def getValue(self, varYamlFile, varKey):
        # 读取 yaml 中键的值
        with open(varYamlFile, "r", encoding="utf-8") as docs:
            code = yaml.load(docs)
        return code[varKey]

    # 3，编辑yaml文件中的值并保存
    def setSave(self, varYamlFile, varKey, varValue):
        with open(varYamlFile, "r", encoding="utf-8") as docs:
            code = yaml.load(docs)
            code[varKey] = varValue
        with open(varYamlFile, "w+", encoding="utf-8") as f:
            yaml.dump(code, f)


if __name__ == "__main__":

    Yaml_PO = YamlPO()

    desired_caps = {
        "platformName": "Android",
        "platformVersion": "7.0",
        "deviceName": "A5RNW18316011440",
        "appPackage": "com.tencent.mm",
        "appActivity": ".ui.LauncherUI",
        "automationName": "Uiautomator2",
        "unicodeKeyboard": [True, "hh"],
        "resetKeyboard": True,
        "noReset": True,
        "chromeOptions": {"androidProcess": "com.tencent.mm:tools"},
    }


    # print("1，将字典保存到文件（覆盖）".center(100, "-"))
    # Yaml_PO.dict2yaml("./data/data.yaml", desired_caps)

    # print("2，获取yaml文件中的值".center(100, "-"))
    # print(Yaml_PO.getValue("./data/data.yaml", "automationName"))  # A5RNW18316011440
    #
    # print(" 3，编辑yaml文件中的值并保存".center(100, "-"))
    # Yaml_PO.setSave("./data/data.yaml", "automationName", {"x": "123", "b": 444, "c": 555, "a": 111, "test": "jinhao"})
    #
    # print(Yaml_PO.getValue("./data/data.yaml", "automationName")) # {'x': '123', 'b': 444, 'c': 555, 'a': 111, 'test': 'jinhao'}
    # print(Yaml_PO.getValue("./data/data.yaml", "automationName")['c'])  # 555

