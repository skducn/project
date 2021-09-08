# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-9-2
# Description: pydub 音频文件分割
#******************************************************************************************************************

from pydub import AudioSegment
from pydub.utils import make_chunks

# 将音频文件进行平均分割
def divideAudio(varSourcePath, varTargetPath, varTargetName, milliseconds):
    # milliseconds  = 50000 表示切割的50毫秒数
    audio = AudioSegment.from_file(varSourcePath, "wav")
    chunks = make_chunks(audio, milliseconds)
    for i, chunk in enumerate(chunks):
        chunk_name = varTargetName + "_{0}.wav".format(i)
        print(chunk_name)
        chunk.export(varTargetPath + chunk_name, format="wav")


# 将bulues0.wav文件平均分割若干个5s文件，并另存于d:\\voice\\test\\
# divideAudio("d:\\voice\\test\\bulues0.wav", "d:\\voice\\test\\", "test", 5000)

x = 3.1015926
print("{:+.2f}".format(x))
print("{:,}".format(10000000))