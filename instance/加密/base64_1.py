# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2023-4-17
# Description: # base64
# https://blog.csdn.net/weixin_44799217/article/details/125949538
# *****************************************************************

import base64,re

def decode_image(src, filename='test'):
    """
    解码图片
    :param src: 图片编码
        eg:
            src="data:image/gif;base64,R0lGODlhMwAxAIAAAAAAAP///
                yH5BAAAAAAALAAAAAAzADEAAAK8jI+pBr0PowytzotTtbm/DTqQ6C3hGX
                ElcraA9jIr66ozVpM3nseUvYP1UEHF0FUUHkNJxhLZfEJNvol06tzwrgd
                LbXsFZYmSMPnHLB+zNJFbq15+SOf50+6rG7lKOjwV1ibGdhHYRVYVJ9Wn
                k2HWtLdIWMSH9lfyODZoZTb4xdnpxQSEF9oyOWIqp6gaI9pI1Qo7BijbF
                ZkoaAtEeiiLeKn72xM7vMZofJy8zJys2UxsCT3kO229LH1tXAAAOw=="

    :return: str 保存到本地的文件名
    """
    # 1、信息提取
    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        data = result.groupdict().get("data")
    else:
        raise Exception("Do not parse!")

    # 2、base64解码
    img = base64.urlsafe_b64decode(data)

    # 3、二进制文件保存
    filename = "{}.{}".format(filename, ext)
    with open(filename, "wb") as f:
        f.write(img)

    return filename

def encode_image(filename):
    """
    编码图片
    :param filename: str 本地图片文件名
    :return: str 编码后的字符串
        eg:
        src="data:image/gif;base64,R0lGODlhMwAxAIAAAAAAAP///
            yH5BAAAAAAALAAAAAAzADEAAAK8jI+pBr0PowytzotTtbm/DTqQ6C3hGX
            ElcraA9jIr66ozVpM3nseUvYP1UEHF0FUUHkNJxhLZfEJNvol06tzwrgd
            LbXsFZYmSMPnHLB+zNJFbq15+SOf50+6rG7lKOjwV1ibGdhHYRVYVJ9Wn
            k2HWtLdIWMSH9lfyODZoZTb4xdnpxQSEF9oyOWIqp6gaI9pI1Qo7BijbF
            ZkoaAtEeiiLeKn72xM7vMZofJy8zJys2UxsCT3kO229LH1tXAAAOw=="

    """
    # 1、文件读取
    ext = filename.split(".")[-1]

    with open(filename, "rb") as f:
        img = f.read()

    # 2、base64编码
    data = base64.b64encode(img).decode()

    # 3、图片编码字符串拼接
    src = "data:image/{ext};base64,{data}".format(ext=ext, data=data)
    return src




# 解码（保存到文件）
url = '''data:image/gif;base64,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'''
decode_image(url, "123")
# decode_image(url)

# 编码（转换成base64）
print(encode_image("123.gif"))