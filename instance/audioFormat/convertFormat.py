# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-9-2
# Description: mp4转mp3
# 安装 pip3 install ffmpeg
# 在线转换 https://www.aconvert.com/cn/audio/mp4-to-wav/
#***************************************************************

import sys, os, subprocess
from moviepy.editor import *

def mp4_to_mp3(varMp4, varMp3):
    video = VideoFileClip(varMp4)
    audio = video.audio
    audio.write_audiofile(varMp3)
mp4_to_mp3("/Users/linghuchong/Downloads/spleeter1/《不要让》Jangan Biarkan万尼瓦比奥拉.mp4", "/Users/linghuchong/Downloads/spleeter1/《不要让》Jangan Biarkan万尼瓦比奥拉.mp3")


from pydub import AudioSegment
def mp3_to_wav(varMp3, varWav):
    MP3_File = AudioSegment.from_mp3(file=varMp3)
    MP3_File.export(varWav, format="wav")
# mp3_to_wav("/Users/linghuchong/Downloads/spleeter1/1.mp3", "/Users/linghuchong/Downloads/spleeter1/1.wav")


def mp4_to_wav(varMp4, varWav):
    subprocess.call("ffmpeg -i " + varMp4 + " -ar 16000 -vn " + varWav, shell=True)
# mp4_to_wav("/Users/linghuchong/Downloads/spleeter1/1.mp4", "/Users/linghuchong/Downloads/spleeter1/1.wav")

