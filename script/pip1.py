# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2022-12-20
# Description: pip 国内镜像
# ********************************************************************************************************************

# 问题1：安装包时提示 time out 超时情况？# raise ReadTimeoutError(self._pool, None, 'Read timed out.')
# # ReadTimeoutError: HTTPSConnectionPool(host='files.pythonhosted.org', port=443): Read timed out.
# 方法1：延长 timeout 时间
# pip --default-timeout=100 install Package    //将Package替换你所需要的库就行


# 方法2：将pip源更换到国内镜像
# 用pip管理工具安装库文件时，默认使用国外的源文件，因此在国内的下载速度会比较慢，可能只有50KB/s。幸好，国内的一些顶级科研机构已经给我们准备好了各种镜像，下载速度可达2MB/s。
# 其中，比较常用的国内镜像包括：
#
# （1）阿里云 http://mirrors.aliyun.com/pypi/simple/
# （2）豆瓣http://pypi.douban.com/simple/
# （3）清华大学 https://pypi.tuna.tsinghua.edu.cn/simple/
# （4）中国科学技术大学 http://pypi.mirrors.ustc.edu.cn/simple/
#
# pip install --index-url https://pypi.douban.com/simple scipy  //从豆瓣源安装scipy库
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple –upgrade tensorflow-gpu   //使用清华大学的源
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pandas   //从清华镜像安装pandas库。




