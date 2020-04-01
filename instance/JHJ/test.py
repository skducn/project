# coding: utf-8
# http://www.jb51.net/article/48001.htm

import os,shutil

# 获取当前文档路径
print os.getcwd()

# 获取文档路径下所有目录和文件, 并将内容放在列表中
print os.listdir(os.getcwd())

# 判断目录是否存在
print os.path.exists("/Users/linghuchong/Downloads/51/ForWin/Python/02_code/screenshot")


# 判断文件是否存在
print os.path.exists("/Users/linghuchong/Downloads/51/ForWin/Python/02_code/screenshot/test.py")


