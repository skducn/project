# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2018/4/20 14:47
# Description: pytesser0.0.1.zip
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Pytesser：依赖于PIL ，Tesseract 了解pytesser及基本使用
# pytesser中并未提供安装脚本，只需把相应py文件拷贝到自己的工程中即可


from pytesser import *
im = Image.open('D:\\51\\Python\\09project\\dkzy\\test.jpg')


def saveAsBmp(fname):
    pos1 = fname.rfind('.')
    fname1 = fname[0:pos1]
    fname1 = fname1 + '_2.bmp'
    im = Image.open(fname)
    new_im = Image.new("RGB", im.size)
    new_im.paste(im)
    new_im.save(fname1)
    return fname1


def RGB2BlackWhite(filename):
        im = Image.open(filename)
        print "image info,", im.format, im.mode, im.size
        (w, h) = im.size
        R = 0
        G = 0
        B = 0

        for x in xrange(w):
            for y in xrange(h):
                pos = (x, y)
                rgb = im.getpixel(pos)
                (r, g, b) = rgb
                R = R + r
                G = G + g
                B = B + b

        rate1 = R * 1000 / (R + G + B)
        rate2 = G * 1000 / (R + G + B)
        rate3 = B * 1000 / (R + G + B)

        print "rate:", rate1, rate2, rate3

        for x in xrange(w):
            for y in xrange(h):
                pos = (x, y)
                rgb = im.getpixel(pos)
                (r, g, b) = rgb
                n = r * rate1 / 1000 + g * rate2 / 1000 + b * rate3 / 1000
                # print "n:",n
                if n >= 60:
                    im.putpixel(pos, (255, 255, 255))
                else:
                    im.putpixel(pos, (0, 0, 0))

        im.save("blackwhite.bmp")

# imgry = im.convert('L')
# # 去噪,G = 50,N = 4,Z = 4
# self.clearNoise(imgry, 50, 0, 4)
# # imgry.save(capScrnPic)

filename = saveAsBmp('D:\\51\\Python\\09project\\dkzy\\test.jpg')
RGB2BlackWhite('D:\\51\\Python\\09project\\dkzy\\test.jpg')
imgry = im.convert('L')

text = image_to_string(im)
print text

