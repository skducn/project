# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2018-5-21
# Description: 颜色对象
# python for mac 输出带颜色的文字方法 https://www.cnblogs.com/yinjia/p/5559702.html
# *******************************************************************************************************************************


class ColorPO:
    def __init__(self):
        pass

    def consoleColor(self, varBackColor, varForeColor, *args):
        # 控制台输出各种颜色字体，多个参数颜色间隔开。
        print(
            "\033[" + varBackColor + ";" + varForeColor + "m" + str(args[0]) + "",
            "\033[0m" + str(args[1]),
        )


if __name__ == "__main__":

    Color_PO = ColorPO()

    Color_PO.consoleColor("31", "36", "[OK], ", "123123123123")
    Color_PO.consoleColor("31", "31", "[ERROR], ", "123123123123")
    Color_PO.consoleColor("31", "33", "[WARNING], ", "123123123123")

    print("\033[1;31;41m", "[1], 红底红字", "\033[0m")
    print("\033[1;31;42m", "[2], 草绿底红字", "\033[0m")
    print("\033[1;31;43m", "[3], 黄底红字", "\033[0m")
    print("\033[1;31;44m", "[4], 蓝底红字", "\033[0m")
    print("\033[1;31;45m", "[5], 紫底红字", "\033[0m")
    print("\033[1;31;46m", "[6], 军绿底红字", "\033[0m")
    print("\033[1;31;47m", "[7], 灰底红字", "\033[0m")
    print("`````````````````````````````````````````````")
    print("\033[1;31;39m", "[8], 黑底白灰字", "\033[0m")
    print("\033[1;31;38m", "[9], 黑底红字", "\033[0m")
    print("\033[1;31;37m", "[10], 黑底碳灰字", "\033[0m")
    print("\033[1;31;36m", "[11], 黑底墨绿字", "\033[0m")
    print("\033[1;31;35m", "[12], 黑底紫字", "\033[0m")
    print("\033[1;31;34m", "[13], 黑底蓝字", "\033[0m")
    print("\033[1;31;33m", "[14], 黑底黄字", "\033[0m")
    print("\033[1;31;32m", "[15], 黑底黄绿字", "\033[0m")
    print("\033[1;31;30m", "[16], 黑底白字", "\033[0m")
    print("`````````````````````````````````````````````")
    print("\033[1;30;40m", "[17], 白底白字", "\033[0m")
    print("\033[1;31;40m", "[18], 白底红字", "\033[0m")
    print("\033[1;32;40m", "[19], 白底黄绿字", "\033[0m")
    print("\033[1;33;40m", "[20], 白底黄字", "\033[0m")
    print("\033[1;34;40m", "[21], 白底蓝字", "\033[0m")
    print("\033[1;35;40m", "[22], 白底紫字", "\033[0m")
    print("\033[1;36;40m", "[23], 白底绿字", "\033[0m")
    print("\033[1;37;40m", "[24], 白底墨灰字", "\033[0m")
    print("\033[1;38;40m", "[25], 白底白灰字", "\033[0m")
    print("`````````````````````````````````````````````")
    print("\033[1;30;41m", "[26], 红底白字", "\033[0m")
    print("\033[1;31;41m", "[27], 红底红字", "\033[0m")
    print("\033[1;32;41m", "[28], 红底黄绿字", "\033[0m")
    print("\033[1;33;41m", "[29], 红底黄字", "\033[0m")
    print("\033[1;34;41m", "[30], 红底蓝字", "\033[0m")
    print("\033[1;35;41m", "[31], 红底紫字", "\033[0m")
    print("\033[1;36;41m", "[32], 红底绿字", "\033[0m")
    print("\033[1;37;41m", "[33], 红底墨灰字", "\033[0m")
    print("\033[1;38;41m", "[34], 红底白灰字", "\033[0m")
    print("`````````````````````````````````````````````")
    print("\033[1;30;42m", "[35], 绿底白字", "\033[0m")
    print("\033[1;31;42m", "[36], 绿底红字", "\033[0m")
    print("\033[1;32;42m", "[37], 绿底黄绿字", "\033[0m")
    print("\033[1;33;42m", "[38], 绿底黄字", "\033[0m")
    print("\033[1;34;42m", "[39], 绿底蓝字", "\033[0m")
    print("\033[1;35;42m", "[40], 绿底紫字", "\033[0m")
    print("\033[1;36;42m", "[41], 绿底绿字", "\033[0m")
    print("\033[1;37;42m", "[42], 绿底墨灰字", "\033[0m")
    print("\033[1;38;42m", "[43], 绿底白灰字", "\033[0m")
    print("`````````````````````````````````````````````")
    print("\033[1;30;43m", "[44], 黄底白字", "\033[0m")
    print("\033[1;31;43m", "[45], 黄底红字", "\033[0m")
    print("\033[1;32;43m", "[46], 黄底黄绿字", "\033[0m")
    print("\033[1;33;43m", "[47], 黄底黄字", "\033[0m")
    print("\033[1;34;43m", "[48], 黄底蓝字", "\033[0m")
    print("\033[1;35;43m", "[49], 黄底紫字", "\033[0m")
    print("\033[1;36;43m", "[50], 黄底绿字", "\033[0m")
    print("\033[1;37;43m", "[51], 黄底墨灰字", "\033[0m")
    print("\033[1;38;43m", "[52], 黄底白灰字", "\033[0m")
