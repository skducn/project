# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-9-2
# Description: mp4转mp3
# 安装 pip3 install ffmpeg
# 在线转换 https://www.aconvert.com/cn/audio/mp4-to-wav/
# 注意源文件名不能有空格，否则报错
#***************************************************************


from pydub import AudioSegment
import os, sys, subprocess
# varFile, x = os.path.splitext(os.path.split(sys.argv[1])[1])
# print(os.getcwd() + "\\" + str(varFile) + '.mp3')

varSource = "/Users/linghuchong/Downloads/letsgo4.mp4"
varTarget = "/Users/linghuchong/Downloads/letsgo4.mp3"
# subprocess.call("ffmpeg -i " + os.path.split(sys.argv[1])[1] + " -ar 16000 -vn " + os.getcwd() + "\\" + str(varFile) + '.mp3', shell=True)
subprocess.call("ffmpeg -i " + varSource + " -ar 16000 -vn " + varTarget, shell=True)









