# -*- coding: utf-8 -*-
# *********************************************************************
# Author        : John
# Date          : 2021-9-7
# Description   : 音频与文字互转
# 安装 pip3 install ffmpeg
# 在线转换 https://www.aconvert.com/cn/audio/mp4-to-wav/

# *********************************************************************

'''
1.1 mp3转wav
1.2 mp4转wav
1.3 中文转拼音（不带声调）
'''

import os, subprocess
from pydub import AudioSegment
from pydub.utils import make_chunks
import pyttsx3
from os.path import join, dirname
import json
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class AudioPO():

    def __init__(self):
        pass

    # 1.1 mp3转wav
    def mp32wav(self, mp3Path, wavPath):
        MP3_File = AudioSegment.from_mp3(file=mp3Path)
        MP3_File.export(wavPath, format="wav")

    # 1.2 mp4转wav
    def mp42wav(self, mp4Path, wavPath):
        subprocess.call("ffmpeg -i " + mp4Path + " -ar 16000 -vn " + wavPath, shell=True)


    # 2 将音频文件进行平均分割
    def divideAudio(self, varSourcePath, varTargetPath, varTargetName, milliseconds):
        # milliseconds  = 50000 表示切割的50毫秒数
        audio = AudioSegment.from_file(varSourcePath, "wav")
        chunks = make_chunks(audio, milliseconds)
        for i, chunk in enumerate(chunks):
            chunk_name = varTargetName + "_{0}.wav".format(i)
            print(chunk_name)
            chunk.export(varTargetPath + chunk_name, format="wav")


    # 3 pyttsx3文字转语音
    def text2mp3(self, varText, varMp3Path):
        tts = pyttsx3.init()
        tts.setProperty('voice', tts.getProperty('voice')[1])
        tts.save_to_file(varText, varMp3Path)
        tts.runAndWait()


    # 4 speech2Text音频转文字
    def speech2Text(self, varPath, varFile):
        # 需要翻墙 live 每月 500 分钟
        # Speech to Text-lv api密钥和url https://cloud.ibm.com/services/speech-to-text/crn%3Av1%3Abluemix%3Apublic%3Aspeech-to-text%3Aau-syd%3Aa%2Fc729c976a03b4b979c7b0225698d2f5c%3A6e18be11-8598-4401-98c3-7622f12d73b6%3A%3A?paneId=manage
        # API参考 https://cloud.ibm.com/apidocs/speech-to-text?code=python
        authenticator = IAMAuthenticator('Ui7RPYwxGu-BDzKT10rGxMweFAECVJHg97z7WJ41RmoG')
        speech_to_text = SpeechToTextV1(
            authenticator=authenticator
        )
        speech_to_text.set_service_url(
            'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/6e18be11-8598-4401-98c3-7622f12d73b6/')
        with open(join(dirname(__file__), varPath, varFile), 'rb') as audio_file:
        # with open(join(dirname(__file__), 'd:/voice/', 'ku7gn-f8adk.wav'), 'rb') as audio_file:
            speech_recognition_results = speech_to_text.recognize(
                audio=audio_file,
                content_type='audio/wav',
                model='zh-CN_BroadbandModel'
                # word_alternatives_threshold=0.9,
                # keywords=['colorado', 'tornado', 'tornadoes'],
                # keywords_threshold=0.5
            ).get_result()
        # print(speech_recognition_results)  # 字典
        result = ""
        all = len(speech_recognition_results['results'])
        for i in range(all):
            text = (speech_recognition_results['results'][i]['alternatives'][0]['transcript']).replace(" ", "")
            result = result + text
        # print(result)
        return result

if __name__ == "__main__":

    Audio_PO = AudioPO()

    # print("1.1 mp3转wav".center(100, "-"))
    # print(Audio_PO.mp32wav('D:\\600\\test1.mp3', 'd:\\600\\test1.wav'))

    # print("1.2 mp4转wav".center(100, "-"))
    # Audio_PO.mp42wav("D:\\1\\123.mp4", "D:\\1\\test2.wav")


    # print("2 将音频文件进行平均分割".center(100, "-"))
    # Audio_PO.divideAudio("d:\\600\\bulues0.wav", "d:\\600\\", "haha", 5000)   # 将bulues0.wav文件平均分割若干个5s文件，并另存于d:\\voice\\test\\


    # print("3 pyttsx3文字转语音".center(100, "-"))
    # Audio_PO.text2mp3("我想测试一下这个系统？不知道明天天气如何", "D:\\600\\text2VoicePyttsx3.mp3")


    print("4 speech2Text音频转文字".center(100, "-"))
    print(Audio_PO.speech2Text('d:/1/', 'test2.wav'))


