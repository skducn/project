# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2022-10-14
# Description: 听喜马拉雅实例
# 听喜马拉雅 https://www.ximalaya.com/
# 在线乱码翻译 http://www.mytju.com/classCode/tools/messyCodeRecover.asp

# 获取index，专辑音频总数，页数 https://www.ximalaya.com/revision/album/getTracksList?albumId=13738175&pageNum=1
# 获取src，https://www.ximalaya.com/revision/play/album?albumId=13738175&pageNum=1
#******************************************************************************************************************


from XimalayaPO import *
ximalaya_PO = XimalayaPO()



# 1，获取专辑列表（序号，音频名，trackId，音频文稿，音频链接）
# ximalaya_PO.getAlbumList("43576130")  # 超级演说家刘媛媛说高效学习法
# ximalaya_PO.getAlbumList("13738175")  # 刘媛媛的晚安电台
# 听喜马拉雅 => 刘媛媛的晚安电台(https://www.ximalaya.com/gerenchengzhang/13738175) => 25页 741个音频
# [2, '“毕业之后，你一定要先留在大城市”', 75421060, 'https://fdfs.xmcdn.com/storages/7b9c-audiofreehighqps/EC/0A/GKwRIaIF9rgXAAAqGAEip-yT.txt', 'http://aod.cos.tx.xmcdn.com/group40/M09/0F/74/wKgJT1qgm-qRjOzPADNCOplZaao353.m4a']
# [1, '“你一定一定一定一定要好好学习”', 75273623, 'https://fdfs.xmcdn.com/storages/4344-audiofreehighqps/AA/1D/CKwRIRwFWV7_AAAuFwDzqHEe.txt', 'http://aod.cos.tx.xmcdn.com/group42/M08/36/0B/wKgJ9FqfoUmwBlrRADLUKlMm8xo039.m4a']


# 2，下载711音频
# ximalaya_PO.getOneAudio("13738175", 711, "d:\\500")  # [711, '为什么我说，好想生个女儿', 'http://aod.cos.tx.xmcdn.com/storages/7f58-audiofreehighqps/67/8E/GKwRIJEGy335ACW0WQGRRn14.m4a', 'd:\\500\\刘媛媛的晚安电台']


# 3，下载多个音频
# ximalaya_PO.getMoreAudio("13738175", "d:\\500")   # 下载所有音频
# ximalaya_PO.getMoreAudio("13738175", "d:\\500", "before", 3)  # 下载3之前的音频
# ximalaya_PO.getMoreAudio("13738175", "d:\\500", "after", 700)  # 下载700之后的音频
# ximalaya_PO.getMoreAudio("13738175", "d:\\500", "", keyword="孩子")   # 下载标题中带“孩子”关键字的音频


# 4，获取音频的文稿（文稿由ASR技术生成）
# 通过专辑id获取每个音频的trackId再取音频的文本
# 如专辑 https://www.ximalaya.com/revision/album/getTracksList?albumId=13738175&pageNum=1 中的某个trackId是 575798239
# 专辑id，albumId=13738175， 音频trackId: 575798239
ximalaya_PO.getTapescriptASR("572912514")  #  trackId = 575798239


