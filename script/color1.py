# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2018-5-21
# Description: cmd 中输出内容颜色
# *******************************************************************************************************************************
# 字体颜色定义 ,关键在于颜色编码，由2位十六进制组成，分别取0~f，前一位指的是背景色，后一位指的是字体色

import ctypes, sys

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# Windows CMD命令行 字体颜色定义 text colors
# 由于该函数的限制，只有这16种，可以前景色与背景色组合。也可以几种颜色通过或运算组合。
FOREGROUND_BLACK = 0x00  # black.
FOREGROUND_DARKBLUE = 0x01  # dark blue.
FOREGROUND_DARKGREEN = 0x02  # dark green.
FOREGROUND_DARKSKYBLUE = 0x03  # dark skyblue.
FOREGROUND_DARKRED = 0x04  # dark red.
FOREGROUND_DARKPINK = 0x05  # dark pink.
FOREGROUND_DARKYELLOW = 0x06  # dark yellow.
FOREGROUND_DARKWHITE = 0x07  # dark white.
FOREGROUND_DARKGRAY = 0x08  # dark gray.
FOREGROUND_BLUE = 0x09  # blue.
FOREGROUND_GREEN = 0x0a  # green.
FOREGROUND_SKYBLUE = 0x0b  # skyblue.
FOREGROUND_RED = 0x0c  # red.
FOREGROUND_PINK = 0x0d  # pink.
FOREGROUND_YELLOW = 0x0e  # yellow.
FOREGROUND_WHITE = 0x0f  # white.

# Windows CMD命令行 背景颜色定义 background colors
BACKGROUND_BLUE = 0x10  # dark blue.
BACKGROUND_GREEN = 0x20  # dark green.
BACKGROUND_DARKSKYBLUE = 0x30  # dark skyblue.
BACKGROUND_DARKRED = 0x40  # dark red.
BACKGROUND_DARKPINK = 0x50  # dark pink.
BACKGROUND_DARKYELLOW = 0x60  # dark yellow.
BACKGROUND_DARKWHITE = 0x70  # dark white.
BACKGROUND_DARKGRAY = 0x80  # dark gray.
BACKGROUND_BLUE = 0x90  # blue.
BACKGROUND_GREEN = 0xa0  # green.
BACKGROUND_SKYBLUE = 0xb0  # skyblue.
BACKGROUND_RED = 0xc0  # red.
BACKGROUND_PINK = 0xd0  # pink.
BACKGROUND_YELLOW = 0xe0  # yellow.
BACKGROUND_WHITE = 0xf0  # white.

# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool

# reset white
def resetColor():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

# 暗蓝色
# dark blue
def printDarkBlue(mess):
    set_cmd_text_color(FOREGROUND_DARKBLUE)
    sys.stdout.write(mess)
    resetColor()

# 暗绿色
# dark green
def printDarkGreen(mess):
    set_cmd_text_color(FOREGROUND_DARKGREEN)
    sys.stdout.write(mess)
    resetColor()

# 暗天蓝色
# dark sky blue
def printDarkSkyBlue(mess):
    set_cmd_text_color(FOREGROUND_DARKSKYBLUE)
    sys.stdout.write(mess)
    resetColor()

# 暗红色
# dark red
def printDarkRed(mess):
    set_cmd_text_color(FOREGROUND_DARKRED)
    sys.stdout.write(mess)
    resetColor()

# 暗粉红色
# dark pink
def printDarkPink(mess):
    set_cmd_text_color(FOREGROUND_DARKPINK)
    sys.stdout.write(mess)
    resetColor()

# 暗黄色
# dark yellow
def printDarkYellow(mess):
    set_cmd_text_color(FOREGROUND_DARKYELLOW)
    sys.stdout.write(mess)
    resetColor()

# 暗白色
# dark white
def printDarkWhite(mess):
    set_cmd_text_color(FOREGROUND_DARKWHITE)
    sys.stdout.write(mess)
    resetColor()

# 暗灰色
# dark gray
def printDarkGray(mess):
    set_cmd_text_color(FOREGROUND_DARKGRAY)
    sys.stdout.write(mess)
    resetColor()

# 蓝色
# blue
def printBlue(mess):
    set_cmd_text_color(FOREGROUND_BLUE)
    sys.stdout.write(mess)
    resetColor()

# 绿色
# green
def printGreen(mess):
    set_cmd_text_color(FOREGROUND_GREEN)
    sys.stdout.write(mess)
    resetColor()

# 天蓝色
# sky blue
def printSkyBlue(mess):
    set_cmd_text_color(FOREGROUND_SKYBLUE)
    sys.stdout.write(mess)
    resetColor()

# 红色
# red
def printRed(mess):
    set_cmd_text_color(FOREGROUND_RED)
    sys.stdout.write(mess)
    resetColor()

# 粉红色
# pink
def printPink(mess):
    set_cmd_text_color(FOREGROUND_PINK)
    sys.stdout.write(mess)
    resetColor()

# 黄色
# yellow
def printYellow(mess):
    set_cmd_text_color(FOREGROUND_YELLOW)
    sys.stdout.write(mess)
    resetColor()

# 白色
# white
def printWhite(mess):
    set_cmd_text_color(FOREGROUND_WHITE)
    sys.stdout.write(mess)
    resetColor()

# 白底黑字
# white bkground and black text
def printWhiteBlack(mess):
    set_cmd_text_color(FOREGROUND_BLACK | BACKGROUND_WHITE)
    sys.stdout.write(mess)
    resetColor()

# 白底黑字
# white bkground and black text
def printWhiteBlack_2(mess):
    set_cmd_text_color(0xf0)
    sys.stdout.write(mess)
    resetColor()

# 黄底蓝字
# white bkground and black text
def printYellowRed(mess):
    set_cmd_text_color(BACKGROUND_YELLOW | FOREGROUND_RED)
    sys.stdout.write(mess)
    resetColor()

if __name__ == '__main__':

    print('\033[1;31;41m', '[1], 红底红字', '\033[0m')
    print('\033[1;31;42m', '[2], 草绿底红字', '\033[0m')
    print('\033[1;31;43m', '[3], 黄底红字', '\033[0m')
    print('\033[1;31;44m', '[4], 蓝底红字', '\033[0m')
    print('\033[1;31;45m', '[5], 紫底红字', '\033[0m')
    print('\033[1;31;46m', '[6], 军绿底红字', '\033[0m')
    print('\033[1;31;47m', '[7], 灰底红字', '\033[0m')
    print("`````````````````````````````````````````````")
    print('\033[1;31;39m', '[8], 黑底白灰字', '\033[0m')
    print('\033[1;31;38m', '[9], 黑底红字', '\033[0m')
    print('\033[1;31;37m', '[10], 黑底碳灰字', '\033[0m')
    print('\033[1;31;36m', '[11], 黑底墨绿字', '\033[0m')
    print('\033[1;31;35m', '[12], 黑底紫字', '\033[0m')
    print('\033[1;31;34m', '[13], 黑底蓝字', '\033[0m')
    print('\033[1;31;33m', '[14], 黑底黄字', '\033[0m')
    print('\033[1;31;32m', '[15], 黑底黄绿字', '\033[0m')
    print('\033[1;31;30m', '[16], 黑底白字', '\033[0m')
    print("`````````````````````````````````````````````")
    print('\033[1;30;40m', '[17], 白底白字', '\033[0m')
    print('\033[1;31;40m', '[18], 白底红字', '\033[0m')
    print('\033[1;32;40m', '[19], 白底黄绿字', '\033[0m')
    print('\033[1;33;40m', '[20], 白底黄字', '\033[0m')
    print('\033[1;34;40m', '[21], 白底蓝字', '\033[0m')
    print('\033[1;35;40m', '[22], 白底紫字', '\033[0m')
    print('\033[1;36;40m', '[23], 白底绿字', '\033[0m')
    print('\033[1;37;40m', '[24], 白底墨灰字', '\033[0m')
    print('\033[1;38;40m', '[25], 白底白灰字', '\033[0m')
    print("`````````````````````````````````````````````")
    print('\033[1;30;41m', '[26], 红底白字', '\033[0m')
    print('\033[1;31;41m', '[27], 红底红字', '\033[0m')
    print('\033[1;32;41m', '[28], 红底黄绿字', '\033[0m')
    print('\033[1;33;41m', '[29], 红底黄字', '\033[0m')
    print('\033[1;34;41m', '[30], 红底蓝字', '\033[0m')
    print('\033[1;35;41m', '[31], 红底紫字', '\033[0m')
    print('\033[1;36;41m', '[32], 红底绿字', '\033[0m')
    print('\033[1;37;41m', '[33], 红底墨灰字', '\033[0m')
    print('\033[1;38;41m', '[34], 红底白灰字', '\033[0m')
    print("`````````````````````````````````````````````")
    print('\033[1;30;42m', '[35], 绿底白字', '\033[0m')
    print('\033[1;31;42m', '[36], 绿底红字', '\033[0m')
    print('\033[1;32;42m', '[37], 绿底黄绿字', '\033[0m')
    print('\033[1;33;42m', '[38], 绿底黄字', '\033[0m')
    print('\033[1;34;42m', '[39], 绿底蓝字', '\033[0m')
    print('\033[1;35;42m', '[40], 绿底紫字', '\033[0m')
    print('\033[1;36;42m', '[41], 绿底绿字', '\033[0m')
    print('\033[1;37;42m', '[42], 绿底墨灰字', '\033[0m')
    print('\033[1;38;42m', '[43], 绿底白灰字', '\033[0m')
    print("`````````````````````````````````````````````")
    print('\033[1;30;43m', '[44], 黄底白字', '\033[0m')
    print('\033[1;31;43m', '[45], 黄底红字', '\033[0m')
    print('\033[1;32;43m', '[46], 黄底黄绿字', '\033[0m')
    print('\033[1;33;43m', '[47], 黄底黄字', '\033[0m')
    print('\033[1;34;43m', '[48], 黄底蓝字', '\033[0m')
    print('\033[1;35;43m', '[49], 黄底紫字', '\033[0m')
    print('\033[1;36;43m', '[50], 黄底绿字', '\033[0m')
    print('\033[1;37;43m', '[51], 黄底墨灰字', '\033[0m')
    print('\033[1;38;43m', '[52], 黄底白灰字', '\033[0m')



