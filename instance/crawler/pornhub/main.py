# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2023-3-14
# Description: pornhub 获取页面视频地址
# 默认路径：/Users/linghuchong/Downloads/eMule/pornhub
#***************************************************************

from PornhubPO import *
Pornhub_PO = PornhubPO()

# 检查网页mhtml视频链接
# Pornhub_PO.checkLink("html.txt","Rtwlingo666")
# Pornhub_PO.checkLink("./page/Rtwlingo666_1.mht")

if platform.system() == "Darwin":
    ...
    # 专辑页面下载
    # Pornhub_PO.downloadAlbum("html.txt", "Rtwlingo666")  # 参数1是是html文件，参数2是目录名
    # Pornhub_PO.downloadAlbum("yinyleon","")  # 参数2为空时默认路径 /Users/linghuchong/Downloads/eMule/pornhub
    #
    # 文本批量下载
    # Pornhub_PO.downloadTxt('pornhub.txt')  # 参数1是是html文件，参数2是目录名
    # file格式 ： 目录，视频连接，如：
    # crystal-lust1，https://cn.pornhub.com/view_video.php?viewkey=ph5fbf2ae68c09
    # crystal-lust，https://cn.pornhub.com/view_video.php?viewkey=ph5fbf2ae68c09
    # crystal-lust3，https://cn.pornhub.com/view_video.php?viewkey=ph5fbf2ae68c09


    # 单个下载
    Pornhub_PO.downloadOne('https://cn.pornhub.com/view_video.php?viewkey=ph62e90ea0555ec', "Rtwlingo666")  # 参数2是目录名
    # Pornhub_PO.downloadOne('https://cn.pornhub.com/view_video.php?viewkey=63de9d08b9892')  # 参数2为空时默认路径 /Users/linghuchong/Downloads/eMule/pornhub




# if platform.system() == "Windows":
#     folder = Pornhub_PO.run("yinyleon", "d:/11/44")






