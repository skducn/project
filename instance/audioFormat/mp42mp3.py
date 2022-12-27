# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-9-2
# Description: mp4转mp3
# 安装 pip3 install ffmpeg
# 在线转换 https://www.aconvert.com/cn/audio/mp4-to-wav/
#***************************************************************


from moviepy.editor import *

varFile, x = os.path.splitext(os.path.split(sys.argv[1])[1])
video = VideoFileClip(os.path.split(sys.argv[1])[1])
audio = video.audio
audio.write_audiofile(os.getcwd() + "\\" + str(varFile) + '.mp3')






