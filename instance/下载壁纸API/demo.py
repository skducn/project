# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-2-8
# Description: 下载壁纸
# http://www.51testing.com/html/24/n-7794924.html
# *****************************************************************
# https://www.bing.com/th?id=OHR.AiringGrievances_EN-US3147113419_1920x1080.jpg&w=1920


import requests

# 下载壁纸数量
def get_wallpaper():
    for i in range(3):
        url = "https://bingw.jasonzeng.dev?resolutinotallow=UHD&index=%s" % str(i)
        print(url)
        res = requests.get(url)
        with open("D:\WALLPAPER/" + "%s.jpg" % str(i),"wb") as w:
            w.write(res.content)

if __name__ == "__main__":
    get_wallpaper()








