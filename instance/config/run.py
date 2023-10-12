# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2023-10-12
# Description   : 配置功能，readConfig
# *****************************************************************

from ConfigparserPO import *
Configparser_PO = ConfigparserPO()

projectName = Configparser_PO.DB("host")
reportName = Configparser_PO.DB("port")

print(projectName)




