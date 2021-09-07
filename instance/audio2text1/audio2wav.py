# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-9-2
# Description: mp4转wav , mp3转wav
# 安装 pip3 install ffmpeg
# 在线转换 https://www.aconvert.com/cn/audio/mp4-to-wav/
#***************************************************************


from pydub import AudioSegment
import os, subprocess

# mp3转wav
def mp32wav(mp3Path, wavPath):
    MP3_File = AudioSegment.from_mp3(file=mp3Path)
    MP3_File.export(wavPath, format="wav")
mp32wav('D:\\600\\test1.mp3','d:\\600\\17.wav')


# mp4转wav
def mp42wav(mp4Path, wavPath):
    subprocess.call("ffmpeg -i " + mp4Path + " -ar 16000 -vn " + wavPath, shell=True)
# mp42wav("D:\\600\\test.mp4", "D:\\600\\test.wav")




