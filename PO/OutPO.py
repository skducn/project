# -*- coding: utf-8 -*-
# *******************************************************************************************************************************
# Author     : John
# Date       : 2022-5-6
# Description: 输出对象
# from PO.OutPO import *
# Out_PO = OutPO()
# Out_PO.outRedError(str(sys._getframe(1).f_lineno), sys._getframe(1).f_code.co_name, sys._getframe().f_code.co_filename, sys._getframe(0).f_code.co_name)

# *******************************************************************************************************************************

from PO.ColorPO import *
Color_PO = ColorPO()


class OutPO():

    def __init__(self):
        pass

    def outRedError(self, errLine, func1, file, func2):

        Color_PO.consoleColor("31", "31", "[Error] , line " + str(errLine) + " (" + func1 + "()) jump to (" + file + " -> " + func2 + "())", "")


if __name__ == '__main__':

    Out_PO = OutPO()

