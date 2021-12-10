# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2021-12-10
# Description: 系统对象
# ***************************************************************

'''
1，关闭进程
'''

import psutil, os, sys
from time import sleep


class SysPO():

    def killPid(self, varApplication):
        '''
        1，关闭进程
        :param varApplication:
        :return:
                os.system 输出如果出现乱码，需将 File->Settings->Editor->File Encodings 中 Global Encoding 设置成 GBK
        '''

        pids = psutil.pids()
        for pid in pids:
            try:
                p = psutil.Process(pid)
                # print('pid=%s,pname=%s' % (pid, p.name()))
                if p.name() == varApplication:
                    cmd = 'taskkill /F /IM ' + varApplication
                    os.system(cmd)
                    sleep(2)
            except:
                print("errorrrrrrrrrr, call " + sys._getframe().f_code.co_name + "() from " + str(sys._getframe(1).f_lineno) + " row, error from " + str(sys._getframe(0).f_lineno) + " row")


if __name__ == '__main__':

    Sys_PO = SysPO()

    print("1，关闭进程".center(100, "-"))
    Sys_PO.killPid('EXCEL.EXE')
    Sys_PO.killPid('360Newsld.exe')
