# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-9-2
# Description: # mp3转wav
# 安装 pip3 install ffmpeg
# 在线转换 https://www.aconvert.com/cn/audio/mp4-to-wav/
#***************************************************************


import os, sys
from pydub import AudioSegment

varFile, x = os.path.splitext(os.path.split(sys.argv[1])[1])
MP3_File = AudioSegment.from_mp3(file=os.path.split(sys.argv[1])[1])
MP3_File.export(os.getcwd() + "\\" + str(varFile) + '.wav', format="wav")





