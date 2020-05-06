# coding: utf-8
# ***************************************************************
# Author     : John
# Date       : 2016-7-29
# Description: ymal学习，
# PyYAML的官方APi文档 http://pyyaml.org/wiki/PyYAMLDocumentation
# ruamel.yaml的API文档[https://yaml.readthedocs.io/en/latest/overview.html]
# python中读写yaml存在两个包，自带的PyYAML包和ruamel.yaml包，ruamel.yaml包在PyYAML包上进行了一些改进，下面分别介绍如何使用这两个包
# pip3 install PyYAML
# pip3 install ruamel.yaml
# Yaml语法检查， http://www.yamllint.com/
# ***************************************************************

from ruamel.yaml import YAML
import sys, os
yaml = YAML()

class YamlPO():

    # 1，读取键的值
    def readYaml(self, varYamlFile, varKey):
        # 读取 yaml 中键的值
        with open(varYamlFile, "r", encoding="utf-8") as docs:
            code = yaml.load(docs)
        return (code[varKey])

    # 2，编辑键的值
    def editYaml(self, varYamlFile, varKey, varValue):
        # 编辑 yaml 键值后保存
        with open(varYamlFile, "r", encoding="utf-8") as docs:
            code = yaml.load(docs)
            code[varKey] = varValue
        with open(varYamlFile, "w+", encoding="utf-8") as f:
            yaml.dump(code, f)

    # 3，打开yaml写入键值（覆盖）
    def writeYaml(self, varYamlFile, varDict):
        # 重写 yaml （删除原先的内容）
        with open(varYamlFile, "w+", encoding="utf-8") as f:
            yaml.dump(varDict, f)

    # yaml.dump(code, sys.stdout)


if __name__ == '__main__':

    Yaml_PO = YamlPO()

    # 将字典写入到yamlPO.yaml
    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '7.0',
        'deviceName': 'A5RNW18316011440',
        'appPackage': 'com.tencent.mm',
        'appActivity': '.ui.LauncherUI',
        'automationName': 'Uiautomator2',
        'unicodeKeyboard': [True, "hh"],
        'resetKeyboard': True,
        'noReset': True,
        'chromeOptions': {'androidProcess': 'com.tencent.mm:tools'}
    }


    print("3，打开yaml写入键值（覆盖）".center(100, "-"))
    Yaml_PO.writeYaml("YamlPO.yaml", desired_caps)

    print("1，读取键的值".center(100, "-"))
    print(Yaml_PO.readYaml("YamlPO.yaml", "deviceName"))  # A5RNW18316011440

    print("2，编辑键的值".center(100, "-"))
    Yaml_PO.editYaml("YamlPO.yaml", "deviceName", {'androidProcess': 'com.tencent.mm:tools'})
    print(Yaml_PO.readYaml("YamlPO.yaml", "deviceName"))  # ordereddict([('androidProcess', 'com.tencent.mm:tools')])

    Yaml_PO.editYaml("YamlPO.yaml", "deviceName", "A5RNW18316011449")
    print(Yaml_PO.readYaml("YamlPO.yaml", "deviceName"))  # # A5RNW18316011449

    



