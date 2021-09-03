# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-9-2
# Description: pyttsx3 文字转语音
#***************************************************************


# engine = pyttsx3.init()
# voices = engine.getProperty("voices")
# for item in voices:
#     print(item.id,item.languages)

import pyttsx3
tts = pyttsx3.init()
tts.setProperty('voice', tts.getProperty('voice')[1])
tts.save_to_file("我想测试一下这个系统？不知道明天天气如何", "./text2VoicePyttsx3.mp3")
tts.runAndWait()