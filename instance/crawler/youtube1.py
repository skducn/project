# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2021-7-1
# Description: 爬取 youtube(未测试通过)
#***************************************************************


#
# import re
# import urllib.request
# def getHtml(url):
#
#     page = urllib.request.urlopen(url)
#
#     html = page.read()
#
#     return html
#
# def getUrl(html):
#
#     reg = r"(?<=a\shref=\"/watch).+?(?=\")"
#
#     urlre = re.compile(reg)
#
#     urllist = re.findall(urlre,html.decode('utf-8'))
#
#     format = "https://www.youtube.com/watch%s\n"
#
#     f = open("F:\output.txt", 'a')
#
#     for url in urllist:
#
#         result = (format % url)
#
#         f.write(result)
#
#         f.close()
#
#         pages = 10
#
#     for i in range(1,pages):
#
#         html = getHtml("https://www.youtube.com/results?search_query=lion+king&lclk=short&filters=short&page=%s" % i)
#
#         print (getUrl(html))
#
#         i += 1
#
# getUrl('https://www.youtube.com/v/j7KYm08ZFm4?rel=0&version=3&autohide=1')
#

# from pytube import YouTube
# yt = YouTube('https://www.youtube.com/watch?v=92h4F7h2Xik')
# yt.g
# yt = yt.get('mp4', '720p')
# yt.download('./')


# from __future__ import unicode_literals
# import youtube_dl
# import urllib
# import shutil
# ydl_opts = {}
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     ydl.download(['https://www.youtube.com/watch?v=92h4F7h2Xik'])
#     # ydl.download(['https://www.youtube.com/watch?v=x9kSOBtVQUc&t=32s'])
#
# #
#
# import youtube_dl
#
# """
# format information
#
# 249          webm       audio only tiny   50k , opus @ 50k (48000Hz), 3.35MiB
# 250          webm       audio only tiny   60k , opus @ 70k (48000Hz), 4.04MiB
# 251          webm       audio only tiny  110k , opus @160k (48000Hz), 7.43MiB
# 140          m4a        audio only tiny  130k , m4a_dash container, mp4a.40.2@128k (44100Hz), 9.58MiB
# 394          mp4        256x144    144p   79k , av01.0.00M.08, 30fps, video only, 4.66MiB
# 278          webm       256x144    144p   96k , webm container, vp9, 30fps, video only, 6.26MiB
# 160          mp4        256x144    144p  100k , avc1.4d400c, 30fps, video only, 3.54MiB
# 395          mp4        426x240    240p  166k , av01.0.00M.08, 30fps, video only, 8.27MiB
# 133          mp4        426x240    240p  190k , avc1.4d4015, 30fps, video only, 6.72MiB
# 242          webm       426x240    240p  218k , vp9, 30fps, video only, 8.21MiB
# 396          mp4        640x360    360p  346k , av01.0.01M.08, 30fps, video only, 15.95MiB
# 134          mp4        640x360    360p  380k , avc1.4d401e, 30fps, video only, 12.03MiB
# 243          webm       640x360    360p  395k , vp9, 30fps, video only, 13.98MiB
# 135          mp4        854x480    480p  527k , avc1.4d401f, 30fps, video only, 17.80MiB
# 244          webm       854x480    480p  598k , vp9, 30fps, video only, 20.22MiB
# 397          mp4        854x480    480p  604k , av01.0.04M.08, 30fps, video only, 28.32MiB
# 136          mp4        1280x720   720p  861k , avc1.4d401f, 30fps, video only, 25.54MiB
# 247          webm       1280x720   720p  971k , vp9, 30fps, video only, 34.36MiB
# 398          mp4        1280x720   720p 1192k , av01.0.05M.08, 30fps, video only, 55.90MiB
# 399          mp4        1920x1080  1080p 2153k , av01.0.08M.08, 30fps, video only, 99.15MiB
# 248          webm       1920x1080  1080p 2666k , vp9, 30fps, video only, 110.46MiB
# 137          mp4        1920x1080  1080p 2675k , avc1.640028, 30fps, video only, 91.89MiB
# 18           mp4        640x360    360p  431k , avc1.42001E, 30fps, mp4a.40.2@ 96k (44100Hz), 31.93MiB
# 22           mp4        1280x720   720p  474k , avc1.64001F, 30fps, mp4a.40.2@192k (44100Hz) (best)
# """
#
#
# class DataDownload:
#     def GetVideo(self, line, f='134'):
#         name = line.split('=')[1]
#         # save address
#         # videoSavePath = 'youtube_data/video/' + name
#         videoSavePath = './' + name
#         # format setting
#         ydl_opts = {
#             'format': f,  # save as 360p mp4
#             'outtmpl': videoSavePath + ".%(ext)s"
#         }
#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([line])
#
#     def GetAudio(self, line, f='140'):
#         name = line.split('=')[1]
#         # save address
#         # audioSavePath = 'youtube_data/audio/' + name
#         audioSavePath = './' + name
#         # format setting
#         ydl_opts = {
#             'format': f,  # save as m4a
#             'outtmpl': audioSavePath + ".%(ext)s"
#         }
#         with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([line])
#
#     def GetBoth(self, line):
#         self.GetAudio(line)
#         self.GetVideo(line)
#
#
# if __name__ == "__main__":
#     A = DataDownload()
#     A.GetBoth('https://www.youtube.com/watch?v=92h4F7h2Xik')
#
