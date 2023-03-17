# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-3-14
# Description: pornhub 获取页面视频地址
# 默认路径：/Users/linghuchong/Downloads/eMule/pornhub
# platform.system() == "Darwin"
#***************************************************************

from PornhubPO import *
Pornhub_PO = PornhubPO()

# 1，初始化更新文件列表
# Pornhub_PO.setFileList('000.txt')

# 2，获取html页面中的视频链接，并保存到 2videoUrl
# Pornhub_PO.html2url("1html", '2phFolderUrl', '2folderUrl')

# 3，下载
# # 3.1.1 单个下载（存在则忽略）
# Pornhub_PO.downloadOne("HelloElly", "https://cn.pornhub.com/view_video.php?viewkey=ph6301df6674703")
# Pornhub_PO.downloadOne("/", "https://cn.pornhub.com/view_video.php?viewkey=ph633a3fbc372ee")  # 下载到当前 /Users/linghuchong/Downloads/eMule/pornhub
# # 3.1.2 单个下载（强制下载）
# Pornhub_PO.downloadOneOver("/", "https://cn.pornhub.com/view_video.php?viewkey=ph633a3fbc372ee")  # 下载到当前 /Users/linghuchong/Downloads/eMule/pornhub

# 3.2 批量下载
Pornhub_PO.downloadMore('2folderUrl')











# if platform.system() == "Windows":
#     folder = Pornhub_PO.run("yinyleon", "d:/11/44")






