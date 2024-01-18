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
from pydub import AudioSegment


def mp3Transform(varSource, varTarget):
    # 音频互转 mp3转wav
    file = AudioSegment.from_mp3(file=varSource)
    file.export(varTarget, format="wav")
# mp3Transform("/Users/linghuchong/Downloads/spleeter1/1.mp3", "/Users/linghuchong/Downloads/spleeter1/1.wav")


def mp4Transform(varSource, varTarget):
    # 视频转音频, mp4转mp3\wav
    subprocess.call("ffmpeg -i " + varSource + " -ar 16000 -vn " + varTarget, shell=True)

# mp4Transform("/Users/linghuchong/Downloads/spleeter1/1.mp4", "/Users/linghuchong/Downloads/spleeter1/1.wav")
# mp4Transform("/Users/linghuchong/Downloads/spleeter1/1.mp4", "/Users/linghuchong/Downloads/spleeter1/1.mp3")


def video2audio(varSource, varTarget):
    # 视频转音频
    video = VideoFileClip(varSource)
    audio = video.audio
    audio.write_audiofile(varTarget)

# video2audio("/Users/linghuchong/Downloads/spleeter1/《不要让》Jangan Biarkan万尼瓦比奥拉.mp4", "/Users/linghuchong/Downloads/spleeter1/《不要让》Jangan Biarkan万尼瓦比奥拉.mp3")
