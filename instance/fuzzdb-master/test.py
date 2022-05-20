# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2019-12-23
# Description   : FUZZDB 安全测试用例数据库
# 参考：http://www.51testing.com/html/68/n-6657668.html
# *********************************************************************
import requests
from threading import Thread
import sys
import getopt

# 程序用法
def usage():
    print("用法：")
    print("     -w:网址 (http://wensite.com/FUZZ)")
    print("     -t:线程数")
    print("     -f:字典文件")
    print("例子：bruteforcer.py -w http://zmister.com/FUZZ -t 5 -f commom.txt")


class request_performer(Thread):
    def __init__(self,word,url):
        Thread.__init__(self)
        try:
            self.word = word.split("\n")[0]
            self.urly = url.replace('FUZZ',self.word)
            self.url = self.urly
        except Exception as e:
            print(e)
    def run(self):
        try:
            r = requests.get(self.url)
            print(self.url,"-",str(r.status_code))
            # i[0] = i[0] -1
        except Exception as e:
            print(e)


def launcher_thread(names,th,url):
    global i
    i = []
    resultlist = []
    i.append(0)
    while len(names):
        try:
            if i[0] < th:
                n = names.pop(0)
                i[0] = i[0]+1
                thread = request_performer(n,url)
                thread.start()
        except KeyboardInterrupt:
            print("用户停止了程序运行。完成探测")
            sys.exit()
    return True


def start(argv):
    if len(sys.argv) < 5:
        usage()
        sys.exit()
    try:
        opts,args = getopt.getopt(sys.argv[1:],"w:t:f:")
    except getopt.GetoptError:
        print("错误的参数")
        sys.exit()
    for opt,arg in opts:
        if opt == '-w':
            url = arg
        elif opt == '-f':
            dicts = arg
        elif opt == '-t':
            threads = int(arg)
    try:
        f = open(dicts,'r')
        words = f.readlines()
    except Exception as e:
        print("打开文件错误：",dicts,"\n")
        print(e)
        sys.exit()
    launcher_thread(words,threads,url)

if __name__ == '__main__':
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print("用户停止了程序运行。完成探测")



