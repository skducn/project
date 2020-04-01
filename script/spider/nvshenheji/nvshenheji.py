# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2019-1-24
# Description   : python3 爬取 https://www.nvshenheji.com/ 上图片
# *****************************************************************
# 功能：
# 1、某个板块下所有页、所有相册    nvshenheji('国产美女','all')
# 2、某个板块下某页的所有相册  nvshenheji('国产美女','2_all')
# 3、某个板块下某页的某个相册  nvshenheji('国产美女','2_4')
# 4、某个板块下某个更新日期之后相册  nvshenheji('国产美女','2019-1-1')
# 4、遍历所有板块下某个更新日期之后相册  nvshenheji('all','2019-1-1')
# 5、遍历首页某相册  xiangceTop100('all')

import os,requests,sys
from bs4 import BeautifulSoup
from time import sleep
import datetime

import random
UserAgent_List = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

baseURL = "https://www.nvshenheji.com"

# 遍历板块生成字典
def getModule(moduleName):

    '''
    遍历板块字典
    :param moduleName: 国产美女
    :return: '国产美女','Guochan'
    '''

    html = requests.get(baseURL)
    html.encoding = 'gb2312'
    bsop = BeautifulSoup(html.text, 'html.parser')

    # 获取第一行板块字典，如 网站首页
    d_moduleNames = {}
    l_moduleNames = bsop.findAll('div', {'class': 'lm1'})
    for l in l_moduleNames[1:]:
        x = str(l).replace("</a></div>",'').split('href="/')[1]
        keys = x.split(">")[1]
        values = x.split("/")[0]
        d_moduleNames[keys] = values

    # 获取第二行板块字典，如 模范学院 （忽略 秀人旗下）
    l_moduleNames = bsop.findAll('div', {'class': 'qttt'})
    for l in l_moduleNames[1:]:
        x = str(l).replace("</a></div>", '').split('href="/')[1]
        keys = x.split(">")[1]
        values = x.split('"')[0].replace("/","")
        d_moduleNames[keys] = values

    # 获取第三行板块字典，如 美腿宝贝 （忽略 丝袜系列、秀人视频、推女郎、嗲囡囡、御女郎）
    l_moduleNames = bsop.findAll('div', {'class': 'qttt1'})
    for l in l_moduleNames[1:]:
        if "href=" in str(l) and "_shipin" not in str(l):
            x = str(l).replace("</a></div>", '').replace('<font color="ff0000">', '').replace('</font>', '').split('href="/')[1]
            keys = x.split(">")[1]
            values = x.split('"')[0].replace("/", "")
            d_moduleNames[keys] = values

    # 追加 top100
    d_moduleNames['top100'] = 'top.html'
    if moduleName == '' or moduleName == 'all':
        return d_moduleNames
    # print(d_moduleNames)
    else:
        return moduleName,d_moduleNames[moduleName]

# 遍历top100
def xiangceTop100(xiangceNo):

    '''
    遍历top100
    :param param: all , 2, 2-5
    :return:
    '''

    # 相册数
    xiangceCount = 0
    moduleURL = 'https://nvshenheji.com'
    html = requests.get(moduleURL + '/top.html')
    html.encoding = 'gb2312'
    bsop = BeautifulSoup(html.text, 'html.parser')
    xiangceCount = 0
    l_xiangcePages = bsop.findAll('div', {'class': 'dan'})
    # for l in l_xiangcePages:
    #     xiangceCount = xiangceCount + 1
    # print(xiangceCount)

    if xiangceNo == 'all':
        for l in l_xiangcePages:
            xiangceCount = xiangceCount + 1
            xiangceURL = str(l).split('href="')[1].split('"')[0]
            xiangceTitle = str(l).split('title="')[1].split('"')[0]
            xiangceURL = moduleURL + xiangceURL
            print("top" + str(xiangceCount) + "：(" + xiangceTitle + ")")
            downloadPIC(xiangceURL)
            print("\n")

    elif ',' in xiangceNo:
        # xiangceTop100('4,7')
        xiangceNo1 = str(xiangceNo).split(',')
        list1 = []
        for i in range(len(xiangceNo1)):
            list1.append(xiangceNo1[i])
        # print(list1) # ['4', '7']
        for l in l_xiangcePages:
            xiangceCount = xiangceCount + 1
            if str(xiangceCount) in list1:
                xiangceURL = str(l).split('href="')[1].split('"')[0]
                xiangceTitle = str(l).split('title="')[1].split('"')[0]
                xiangceURL = moduleURL + xiangceURL
                print("top" + str(xiangceCount) + "：(" + xiangceTitle + ")")
                downloadPIC(xiangceURL)
                print("\n")
    elif '-' in xiangceNo:
        # xiangceTop100('4-6')
        xiangceNo2 = str(xiangceNo).split("-")
        list2 = []
        for i in range(int(xiangceNo2[0]), int(xiangceNo2[1]) + 1):
            list2.append(i)
        # print(list2)  # ['4', '5', '6']
        for l in l_xiangcePages:
            xiangceCount = xiangceCount + 1
            if str(xiangceCount) in list2:
                xiangceURL = str(l).split('href="')[1].split('"')[0]
                xiangceTitle = str(l).split('title="')[1].split('"')[0]
                xiangceURL = moduleURL + xiangceURL
                print("top" + str(xiangceCount) + "：(" + xiangceTitle + ")")
                downloadPIC(xiangceURL)
                print("\n")
    else:
        for l in l_xiangcePages:
            xiangceCount = xiangceCount + 1
            try:
                xiangceNo = int(xiangceNo)
                if xiangceCount == xiangceNo:
                    xiangceURL = str(l).split('href="')[1].split('"')[0]
                    xiangceTitle = str(l).split('title="')[1].split('"')[0]
                    xiangceURL = moduleURL + xiangceURL
                    print("top" + str(xiangceCount) + "：(" + xiangceTitle + ")")
                    downloadPIC(xiangceURL)
                    break
            except ValueError as err:
                print("error:参数必须是数字，" + str(err))
                break

# 遍历相册
def xiangce(t_module, param):

    '''
    遍历相册
    :param t_module[0]: 模范学院
    :param t_module[1]: MFStar/
    :param param: all , 2_all , 2_4
    :return:
    '''

    # 总页数
    totalPages = 0
    moduleURL = 'https://www.nvshenheji.com/' + t_module[1]
    html = requests.get(moduleURL)
    html.encoding = 'gb2312'
    bsop = BeautifulSoup(html.text, 'html.parser')
    l_xiangcePages = bsop.findAll('div', {'class': 'page'})
    for l in l_xiangcePages:
        totalPages = str(l).split('this.value&lt;=')[1].split("&")[0]
    # print(totalPages)

    # 每页相册数
    xiangceCount = 0
    l_xiangcePages = bsop.findAll('div', {'class': 'biank1'})
    for l in l_xiangcePages:
        xiangceCount = xiangceCount + 1
    # print(xiangceCount)


    # 遍历定位
    if param == 'all':
        # 遍历所有页、所有相册
        page = 'all'
    elif "_" not in param:
        print("错误，参数不正确！")
    else:
        page = param.split("_")[0]
        xiangceNo = param.split("_")[1]
        if xiangceNo == 'all':
            # 遍历某页的所有相册，nvshenheji('国产美女','2_all')
            if page != '1':
                moduleURL = moduleURL + '/index' + str(page) + '.html'
                # print(moduleURL)  # https://www.nvshenheji.com/MFStar/index2.html
            html = requests.get(moduleURL)
            html.encoding = 'gb2312'
            bsop = BeautifulSoup(html.text, 'html.parser')
            l_xiangcePages = bsop.findAll('div', {'class': 'biank1'})
            # 模范学院共9页，第2页20个相册
            print(t_module[0] + "共" + str(totalPages) +"页，第" + str(page) + "页" + str(xiangceCount) + "个册")
            i = 0
            for l in l_xiangcePages:
                i = i + 1
                xiangceURL = str(l).split('href="')[1].split('"')[0]  # /MFStar/lengbuding_98b18730.html
                xiangceURL = 'https://www.nvshenheji.com' + xiangceURL
                print("*"*50 + "\n")
                print('相册' + str(i) + '：' + xiangceURL)
                downloadPIC(xiangceURL)
        else:
            # 某页的某个相册，nvshenheji('国产美女','2_5')
            if page != '1':
                moduleURL = moduleURL + '/index' + str(page) + '.html'
                # print(moduleURL)  # https://www.nvshenheji.com/MFStar/index2.html
            html = requests.get(moduleURL)
            html.encoding = 'gb2312'
            bsop = BeautifulSoup(html.text, 'html.parser')
            l_xiangcePages = bsop.findAll('div', {'class': 'biank1'})
            print(t_module[0] + "共" + str(totalPages) +"页，第" + str(page) + "页" + str(xiangceCount) + "个册")
            i = 0
            for l in l_xiangcePages:
                i = i + 1
                if i == int(xiangceNo):
                    xiangceURL = str(l).split('href="')[1].split('"')[0]  # /MFStar/lengbuding_98b18730.html
                    xiangceURL = 'https://www.nvshenheji.com' + xiangceURL
                    print('相册' + str(i) + '：' + xiangceURL)
                    downloadPIC(xiangceURL)

# 下载图片
def downloadPIC(xiangceURL):

    '''
    下载图片
    :param xiangceURL: https://www.nvshenheji.com/MFStar/lengbuding_98b18730.html
    :return:
    '''

    html = requests.get(xiangceURL)
    html.encoding = 'gb2312'
    bsop = BeautifulSoup(html.text, 'html.parser')

    # 获取图片标题，用于目录名
    imgFolder = bsop.find('div', {'class': 'img'}).find("p").findAll("img")[0].attrs['alt']
    print('下载：' + imgFolder) # [MFStar模范学院]Vol.149_靓丽美女冷不丁私房全裸秀白嫩胴体撩人姿势火辣诱惑写真51P
    proDir = os.path.split(os.path.realpath(__file__))[0]
    resultPath = os.path.join(proDir, imgFolder)
    if not os.path.exists(resultPath):
         os.mkdir(resultPath)

    # 获取总页数
    pages = bsop.find('div', {'class': 'page'}).findAll("a")
    # print(len(pages[:-1]))  # 17

    # 遍历所有页
    for j in range(1,len(pages[:-1])):
        print("第" + str(j) + "页")
        pageURL = str(xiangceURL).split('.html')[0] + '_' + str(j) + '.html'
        html = requests.get(pageURL)
        html.encoding = 'gb2312'
        bsop = BeautifulSoup(html.text, 'html.parser')

        # 下载图片
        imgs = bsop.find('div', {'class': 'img'}).find("p")
        for l in imgs:
            x = str(l).split(".jpg")
            for i in range(len(x)-1):
                imgURL = 'https://img.nvshenheji.com/' + str(x[i]).split('src="')[1] + ".jpg"
                print(imgURL)
                imgName = imgURL.split('/')[-1]  # 图片名字
                headers = {'User-Agent': random.choice(UserAgent_List),
                           'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                           'Accept-Encoding': 'gzip',
                           }
                img_html = requests.get(imgURL, headers=headers)
                with open(resultPath + '\\' + imgName, 'wb') as f:
                    f.write(img_html.content)
                    f.close()

# 相册更新日期
def xiangceUpdate(moduleName, timeParam):

    '''
    遍历相册
    :param moduleName: all 、 国产美女
    :param timeParam: 2019-1-1  遍历1.1以后的相册
    :return:
    '''

    timeParam = datetime.datetime.strptime(str(timeParam), "%Y-%m-%d")

    if moduleName != 'all':
        print(moduleName)
        t_module = getModule(moduleName)
        moduleURL = baseURL + '/' + t_module[1]
        # 总页数
        totalPages = 0
        html = requests.get(moduleURL)
        html.encoding = 'gb2312'
        bsop = BeautifulSoup(html.text, 'html.parser')
        l_xiangcePages = bsop.findAll('div', {'class': 'page'})
        for l in l_xiangcePages:
            totalPages = str(l).split('this.value&lt;=')[1].split("&")[0]
        # print(totalPages)

        for i in range(int(totalPages)):
            if i == 0 :
                html = requests.get(moduleURL)
            else:
                html = requests.get(moduleURL + '/index' + str(i+1) + '.html')
            html.encoding = 'gb2312'
            bsop = BeautifulSoup(html.text, 'html.parser')

            print("第" + str(i + 1) + "页")
            # 检查每页相册数是否满足更新日期条件，获得符合要求的相册数量。
            xiangceCount = 0
            l_xiangceNos = bsop.findAll('div', {'class': 'biank1'})
            l_update = []
            l_xiangceURL = []
            l_xiangceTitle = []
            for l in l_xiangceNos:
                xiangceCount = xiangceCount + 1
                updateTime = str(l).split('更新:')[1].split("日<")[0]
                updateTime = updateTime.replace('年','-').replace('月','-')
                updateTime = datetime.datetime.strptime(updateTime, "%Y-%m-%d")
                if updateTime >= timeParam:
                    l_update.append(updateTime)
                    xiangceURL = str(l).split('href="')[1].split('"')[0]  # /MFStar/lengbuding_98b18730.html
                    xiangceTitle = str(l).split('title="')[1].split('"')[0]  # [MyGirl美媛馆]Vol.341_女神SOLO-尹菲日本旅拍户外红
                    xiangceURL = baseURL + xiangceURL
                    l_xiangceURL.append(xiangceURL)
                    l_xiangceTitle.append(xiangceTitle)
            # 遍历相册
            if len(l_update) == xiangceCount:
                for j in range(len(l_update)):
                    print('相册' + str(j+1) + '：' + l_xiangceTitle[j])
                    downloadPIC(l_xiangceURL[j])
            else:
                for j in range(len(l_update)):
                    print('相册' + str(j+1) + '：' + l_xiangceTitle[j])
                    downloadPIC(l_xiangceURL[j])
                break
    else:
        '遍历所有板块'
        d_all = getModule('all')
        for moduleName,moduleURL in d_all.items():
            moduleURL = baseURL + '/' + d_all[moduleName]
            # 总页数
            totalPages = 0
            html = requests.get(moduleURL)
            html.encoding = 'gb2312'
            bsop = BeautifulSoup(html.text, 'html.parser')
            l_xiangcePages = bsop.findAll('div', {'class': 'page'})
            for l in l_xiangcePages:
                totalPages = str(l).split('this.value&lt;=')[1].split("&")[0]
            # print(totalPages)

            for i in range(int(totalPages)):
                if i == 0:
                    html = requests.get(moduleURL)
                else:
                    html = requests.get(moduleURL + '/index' + str(i + 1) + '.html')
                html.encoding = 'gb2312'
                bsop = BeautifulSoup(html.text, 'html.parser')
                # 检查每页相册数是否满足更新日期条件，获得符合要求的相册数量。
                xiangceCount = 0
                l_xiangceNos = bsop.findAll('div', {'class': 'biank1'})
                l_update = []
                l_xiangceURL = []
                l_xiangceTitle = []
                for l in l_xiangceNos:
                    xiangceCount = xiangceCount + 1
                    updateTime = str(l).split('更新:')[1].split("日<")[0]
                    updateTime = updateTime.replace('年', '-').replace('月', '-')
                    updateTime = datetime.datetime.strptime(updateTime, "%Y-%m-%d")
                    if updateTime >= timeParam:
                        l_update.append(updateTime)
                        xiangceURL = str(l).split('href="')[1].split('"')[0]  # /MFStar/lengbuding_98b18730.html
                        xiangceTitle = str(l).split('title="')[1].split('"')[0]  # [MyGirl美媛馆]Vol.341_女神SOLO-尹菲日本旅拍户外红
                        xiangceURL = baseURL + xiangceURL
                        l_xiangceURL.append(xiangceURL)
                        l_xiangceTitle.append(xiangceTitle)

                if len(l_update) > 0 :
                    print(moduleName, "- 第" + str(i + 1) + "页")


                # 遍历相册
                if len(l_update) == xiangceCount:

                    for j in range(len(l_update)):
                        print('相册' + str(j + 1) + '：' + l_xiangceTitle[j])
                        downloadPIC(l_xiangceURL[j])
                else:

                    for j in range(len(l_update)):
                        print('相册' + str(j + 1) + '：' + l_xiangceTitle[j])
                        downloadPIC(l_xiangceURL[j])
                    break

# 主程序
def nvshenheji(moduleName, param):

    '''
    下载图片
    :param moduleName:
    :param param:
    # 参数1：板块名字
    # 参数2：all 表示所有板块中所有相册的图片（费时间）
    #       _ 前面是指定页数，
    #       _ 后面是数字，表示指定相册，后面是all表示所有的相册
    # 如 3_5 表示下载第3页第五个相册
    # 如 4_all 表示下载第4页所有相册
    e.g.:
    # nvshenheji('性感美女','178_4') # 下载 性感车模 板块中第3页中第4个相册图片
    # nvshenheji('性感车模','3_all') # 下载 性感车模 板块中第3页中所有相册图片
    # nvshenheji('性感车模','all') # 下载 性感车模 板块中所有的相册图片(谨慎)


    :return:
    '''

    t_module = getModule(moduleName)
    xiangce(t_module, param)
    # 打开目录
    os.startfile(str('E:\\51\\Python\\09project\\common\\spider\\nvshenheji'))

# *****************************************************************

# print(getModule('假面女皇'))
# print(getModule('all'))
# x = getModule('all')
# print(len(x))


# 1、某个板块下所有页、所有相册
# nvshenheji('假面女皇', '1_all')

# 2、某个板块下某页的所有相册
# nvshenheji('Rosi口罩', '1_all')

# 3、某个板块下某页的某个相册
# nvshenheji('国产美女','2_4')

# 4、某个板块下某个更新日期之后相册
# xiangceUpdate('魅妍社','2019-01-30')
# xiangceUpdate('all','2019-02-01')

# 下载某个URL
downloadPIC('https://www.nvshenheji.com/Rosimm/heisimeinv_59cb44b8.html')
#
#

# top100: https://nvshenheji.com/top.html
# 下载top100所有相册
# xiangceTop100('all')
# 下载top100第2个相册
# xiangceTop100('2')
# 下载top100第1、4、100 三个相册
# xiangceTop100('1,4,100')
# 下载top100第2、3、4、5 四个相册
# xiangceTop100('2-5')










