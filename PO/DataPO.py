# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2019-9-19
# Description: 数据对象层
# todo:用MD5加密内容
# md5(python2),hashlib(python3)
# MD5消息摘要算法（英语：MD5 Message-Digest Algorithm），一种被广泛使用的密码散列函数，
# 可以产生出一个128位（16字节）的散列值（hash value），用于确保信息传输完整一致。
# 什么是摘要算法呢？摘要算法又称哈希算法、散列算法。它通过一个函数，把任意长度的数据转换为一个长度固定的数据串（通常用16进制的字符串表示）
# # 如果要被加密的数据太长，可以分段update，结果是一样的，如下：
# m = hashlib.md5()
# m.update('12345'.encode('utf-8'))
# m.update('6'.encode('utf-8'))
# print(m.hexdigest())  # e10adc3949ba59abbe56e057f20f883e

# todo: 二维码生成和识别
# 参考：https://www.bilibili.com/read/cv7761473/
# pip install myqr
# pip install pyzbr
# pip install pil 报错请切换 pip install pillow
# ***************************************************************

"""
1.1，随机获取中文用户名 getChineseName()
1.2，随机获取手机号码 getPhone()
1.3，随机获取n位数 getFigures(n)
1.4，随机获取n个整数 getIntList()
1.5，随机获取列表中元素 getElement(list,n)
1.6，随机获取国内高匿ip代理  getProxies()
1.7.1，随机获取用户代理1 getUserAgent()
1.7.2，随机获取用户代理2(访问fake地址) getUserAgent2()
1.7.3，随机获取用户代理3(解析fake地址另存为json，本地访问json文件) getUserAgent3()
1.8 随机获取一个日期 getDate()

2.1，生成身份证号 getIdCard()
2.1.1，获取身份证出生年月 getBirthday(varIdcard)
2.1.2，获取身份证年龄 getAge(varIdcard)
2.1.3，获取身份证性别 getSex(varIdcard)
2.1.4, 获取身份证校验码 getCheckCode(varIdcard)
2.1.5，判断身份证有效性 isIdCard(varIdcard)
2.3.1，生成IP  getIp()
2.3.2，生成IP2  getIP2()
2.3.3，获取连续n个IP  getSeriesIp(ip,n)
2.4.1，生成MD5加密值 getMd5()
2.4.2，生成MD5分段加密值 getMd5Segment()
2.5，生成uuid  getUUID()
2.6，生成二维码 getQR()
2.6.1，获取二维码的地址  getAddressByQR()

3.1，获取字符串中数字的位置(索引) getNumnberIndex()
3.2，获取字符串中字符重复的次数 getRepeatCount()
3.3，获取文档里单词数量  getWordQty(pathfile,word)

"""

import sys, random, json, jsonpath, hashlib, socket, struct, re, uuid, requests, datetime, os
import random
from datetime import date
from datetime import timedelta
from bs4 import BeautifulSoup
import pandas as pd
# from MyQR import myqr

# from pyzbar.pyzbar import decode
from PIL import Image
from time import sleep

# from fake_useragent import UserAgent

# 如报错 fake_useragent.errors.FakeUserAgentError: Maximum amount of retries reached，则更新 pip3.9 install -U fake-useragent
# location = 'D:/51/python/project/PO/fake_useragent_0.1.11.json'
# print(location)
# ua = UserAgent(path=location)


class DataPO:
    def getChineseName(self):

        """1.1，随机获取中文用户名"""

        a1 = [
            "赵",
            "钱",
            "孙",
            "李",
            "周",
            "吴",
            "郑",
            "王",
            "冯",
            "陈",
            "褚",
            "卫",
            "蒋",
            "沈",
            "韩",
            "杨",
            "朱",
            "秦",
            "尤",
            "许",
            "何",
            "吕",
            "施",
            "张",
        ]
        a2 = ["玉", "明", "龙", "芳", "军", "玲", "一", "美", "恋", "世", "亮", "佳"]
        a3 = [
            "栋",
            "玲",
            "",
            "国",
            "",
            "浩",
            "秋",
            "涛",
            "",
            "杰",
            "",
            "华",
            "伟",
            "荣",
            "兴",
            "柏",
            "",
            "桦",
        ]
        return random.choice(a1) + random.choice(a2) + random.choice(a3)
        # return unicode(name, "utf-8")

    def getPhone(self):

        """1.2，随机获取手机号码"""

        prelist = [
            "130",
            "131",
            "132",
            "133",
            "134",
            "135",
            "136",
            "137",
            "138",
            "139",
            "147",
            "150",
            "151",
            "152",
            "153",
            "155",
            "156",
            "157",
            "158",
            "159",
            "186",
            "187",
            "188",
            "199",
        ]
        return random.choice(prelist) + "".join(
            random.choice("0123456789") for i in range(8)
        )

    def getFigures(self, n):

        """1.3，随机获取n位数"""

        ret = []
        for i in range(n):
            while 1:
                number = random.randrange(0, 10)
                if number not in ret:
                    ret.append(str(number))
                    break
        x = "".join(ret)
        return x

    def getIntList(self, varEndInt, varNum):

        """1.4，随机获取n个整数"""

        return random.sample(range(1, varEndInt), varNum)

    def getElement(self, l_Content, varNum):

        """1.5，随机获取列表中元素"""

        # 如：getElement(['411', '1023', '0906', '0225'],'2')
        return random.sample(l_Content, varNum)



    def getUserAgent2(self, varVersionUrl="https://fake-useragent.herokuapp.com/browsers/0.1.11"):

        """1.7.2，随机获取用户代理2(访问fake地址)"""

        my_user_agent = requests.get(varVersionUrl)
        agent_json = json.loads(my_user_agent.text)
        # print(agent_json)
        l_browsers = agent_json["browsers"]
        # print(l_browsers)
        i = random.randint(0, len(l_browsers))
        browsers_name = ""
        if i == 0:
            browsers_name = "chrome"
        elif i == 1:
            browsers_name = "opera"
        elif i == 2:
            browsers_name = "firefox"
        elif i == 3:
            browsers_name = "internetexplorer"
        elif i == 4:
            browsers_name = "safari"
        final_browser = l_browsers[browsers_name][
            random.randint(0, len(l_browsers[browsers_name]) - 1)
        ]
        return final_browser

    def getUserAgent3(
        self,
        jsonFile,
        varVersionUrl="https://fake-useragent.herokuapp.com/browsers/0.1.11",
    ):

        """1.7.3，随机获取用户代理3(解析fake地址另存为json，本地访问json文件)"""

        if varVersionUrl == "None":
            pass
        else:
            my_user_agent = requests.get(varVersionUrl)
            with open(jsonFile, "w") as f:
                json.dump(my_user_agent.text, f)
                # json.dump(my_user_agent.text, f, ensure_ascii=False)  # 将翻译成中文。

        # 获取最佳读取速度
        with open(jsonFile, "r") as f:
            browsers_json = json.load(f)
            browsers_json = json.loads(browsers_json)
            l_browsers = browsers_json["browsers"]
            i = random.randint(0, len(l_browsers))
            browsers_name = ""
            if i == 0:
                browsers_name = "chrome"
            elif i == 1:
                browsers_name = "opera"
            elif i == 2:
                browsers_name = "firefox"
            elif i == 3:
                browsers_name = "internetexplorer"
            elif i == 4:
                browsers_name = "safari"
            final_browser = l_browsers[browsers_name][
                random.randint(0, len(l_browsers[browsers_name]) - 1)
            ]
            return final_browser


    def getDate(self):

        # 1.8 随机获取一个日期

        # 设置起始日期和结束日期（包含）
        start_date = date(2019, 1, 1)
        end_date = date.today()

        # 计算日期范围内的天数
        delta = end_date - start_date + timedelta(days=1)
        total_days = delta.days

        # 生成随机索引值
        index = random.randint(0, total_days - 1)

        # 根据索引值计算随机日期
        random_date = start_date + timedelta(days=index)

        return random_date



    def getIdCard(self, areaCode="310101", start="1950-01-01"):

        """
        2.1 生成身份证号
        areaCode 是区域码，可通过国家统计局获取所有地区的区域码，国家统计局 http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/index.html
        默认北京西城区 110102， 上海黄浦区310101
        start 表示只生成start之后的出生日期
        """

        end = str(date.today())
        days = (
            datetime.datetime.strptime(end, "%Y-%m-%d")
            - datetime.datetime.strptime(start, "%Y-%m-%d")
        ).days + 1
        birth_days = datetime.datetime.strftime(
            datetime.datetime.strptime(start, "%Y-%m-%d")
            + datetime.timedelta(random.randint(0, days)),
            "%Y%m%d",
        )
        areaCode += str(birth_days)
        # 顺序码(2位数)
        areaCode += str(random.randint(10, 99))
        # 性别码(1位数)，sex = 0女性，sex = 1男性
        areaCode += str(random.randrange(random.randint(0, 1), 10, step=2))
        # 校验码(1位数)
        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * int(areaCode[i])
        check_digit = (12 - (check_sum % 11)) % 11
        if check_digit < 10:
            check_digit
        else:
            check_digit = "X"
        return areaCode + str(check_digit)

    def getBirthday(self, varIdcard):

        """2.1.1，获取身份证的出生年月"""

        # 先判断身份证是否有效
        if Data_PO.isIdCard(varIdcard) == True:
            yearMonthDay = (varIdcard[6:10], varIdcard[10:12], varIdcard[12:14])
            return yearMonthDay
        else:
            return None

    def getAge(self, varIdcard):

        """2.1.2，获取身份证的年龄"""

        # 先判断身份证是否有效
        if Data_PO.isIdCard(varIdcard) == True:
            Date = varIdcard[6:10] + "." + varIdcard[10:12] + "." + varIdcard[12:14]
            Date = Date.split(".")
            BirthDate = datetime.date(int(Date[0]), int(Date[1]), int(Date[2]))
            Today = datetime.date.today()
            if Today.month > BirthDate.month:
                NextYear = datetime.date(Today.year + 1, BirthDate.month, BirthDate.day)
            elif Today.month < BirthDate.month:
                NextYear = datetime.date(
                    Today.year,
                    Today.month + (BirthDate.month - Today.month),
                    BirthDate.day,
                )
            elif Today.month == BirthDate.month:
                if Today.day > BirthDate.day:
                    NextYear = datetime.date(
                        Today.year + 1, BirthDate.month, BirthDate.day
                    )
                elif Today.day < BirthDate.day:
                    NextYear = datetime.date(
                        Today.year,
                        BirthDate.month,
                        Today.day + (BirthDate.day - Today.day),
                    )
                elif Today.day == BirthDate.day:
                    NextYear = 0
            Age = Today.year - BirthDate.year
            if NextYear == 0:  # if today is the birthday
                return "%d" % (Age)
                # return '%d, days until %d: %d' % (Age, Age+1, 0)
            else:
                DaysLeft = NextYear - Today
                return "%d" % (Age)
                # return '%d, days until %d: %d' % (Age, Age+1, DaysLeft.days)
        else:
            return None

    def getSex(self, varIdcard):

        """2.1.3，获取身份证的性别"""

        # 先判断身份证是否有效
        if self.isIdCard(varIdcard) == True:
            if (int(varIdcard[16:17]) % 2) == 0:
                # print("{0} 是偶数".format(IdCard[16:17]))
                return "女"
            else:
                # print("{0} 是奇数".format(IdCard[16:17]))
                return "男"
        else:
            return None

    def getCheckCode(self, areaCode):

        """2.1.4，获取身份证校验码"""

        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * int(areaCode[i])
        check_digit = (12 - (check_sum % 11)) % 11
        return check_digit if check_digit < 10 else "X"

    def isIdCard(self, varIdcard):

        """2.1.5 判断身份证有效性"""
        # errors = ['验证通过!', '身份证号码位数不对!', '身份证号码出生日期超出范围或含有非法字符!', '身份证号码校验错误!', '身份证地区非法!']

        errors = [True, False, False, False, False]
        area = {
            "11": "北京",
            "12": "天津",
            "13": "河北",
            "14": "山西",
            "15": "内蒙古",
            "21": "辽宁",
            "22": "吉林",
            "23": "黑龙江",
            "31": "上海",
            "32": "江苏",
            "33": "浙江",
            "34": "安徽",
            "35": "福建",
            "36": "江西",
            "37": "山东",
            "41": "河南",
            "42": "湖北",
            "43": "湖南",
            "44": "广东",
            "45": "广西",
            "46": "海南",
            "50": "重庆",
            "51": "四川",
            "52": "贵州",
            "53": "云南",
            "54": "西藏",
            "61": "陕西",
            "62": "甘肃",
            "63": "青海",
            "64": "宁夏",
            "65": "新疆",
            "71": "台湾",
            "81": "香港",
            "82": "澳门",
            "91": "国外",
        }
        id_card = str(varIdcard)
        id_card = id_card.strip()  # 删除前后空格
        id_card_list = list(id_card)

        # 地区校验
        if not area[id_card[0:2]]:
            return errors[4]

        # 15位身份号码检测
        if len(id_card) == 15:
            if (int(id_card[6:8]) + 1900) % 4 == 0 or (
                (int(id_card[6:8]) + 1900) % 100 == 0
                and (int(id_card[6:8]) + 1900) % 4 == 0
            ):
                e_reg = re.compile(
                    "[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|"
                    "[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$"
                )  # //测试出生日期的合法性
            else:
                e_reg = re.compile(
                    "[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|"
                    "[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$"
                )  # //测试出生日期的合法性
            if re.match(e_reg, id_card):
                return errors[0]
            else:
                return errors[2]

        # 18位身份号码检测
        elif len(id_card) == 18:
            # 出生日期的合法性检查
            if int(id_card[6:10]) % 4 == 0 or (
                int(id_card[6:10]) % 100 == 0 and int(id_card[6:10]) % 4 == 0
            ):
                e_reg = re.compile(
                    "[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)"
                    "(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$"
                )  # //闰年出生日期的合法性正则表达式
            else:
                e_reg = re.compile(
                    "[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)"
                    "(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$"
                )  # //平年出生日期的合法性正则表达式
            # //测试出生日期的合法性
            if re.match(e_reg, id_card):
                # //计算校验位
                S = (
                    (int(id_card_list[0]) + int(id_card_list[10])) * 7
                    + (int(id_card_list[1]) + int(id_card_list[11])) * 9
                    + (int(id_card_list[2]) + int(id_card_list[12])) * 10
                    + (int(id_card_list[3]) + int(id_card_list[13])) * 5
                    + (int(id_card_list[4]) + int(id_card_list[14])) * 8
                    + (int(id_card_list[5]) + int(id_card_list[15])) * 4
                    + (int(id_card_list[6]) + int(id_card_list[16])) * 2
                    + int(id_card_list[7]) * 1
                    + int(id_card_list[8]) * 6
                    + int(id_card_list[9]) * 3
                )
                Y = S % 11
                M = "F"
                JYM = "10X98765432"
                M = JYM[Y]  # 判断校验位
                # print(S)
                # print(Y)
                # print(M)
                if M == id_card_list[17]:  # 检测ID的校验位
                    return errors[0]
                else:
                    return errors[3]
            else:
                return errors[2]
        else:
            return errors[1]

    def getIp(self, varPartIP):

        """2.3.1，生成IP"""

        varIP = socket.inet_ntoa(struct.pack(">I", random.randint(1, 0xFFFFFFFF)))
        list1 = varPartIP.split(".")[:]
        if varPartIP == "":
            return varIP
        elif varPartIP.count(".") == 3:

            if "?" not in varPartIP:
                return varPartIP

            # 11.?.?.?
            if list1[1] == "?" and list1[2] == "?" and list1[3] == "?":
                return (
                    varPartIP.split(".")[0]
                    + "."
                    + varIP.split(".")[1]
                    + "."
                    + varIP.split(".")[2]
                    + "."
                    + varIP.split(".")[3]
                )

            # ?.11.?.?
            if list1[0] == "?" and list1[1] == "?" and list1[3] == "?":
                return (
                    varIP.split(".")[0]
                    + "."
                    + varIP.split(".")[1]
                    + "."
                    + varPartIP.split(".")[2]
                    + "."
                    + varIP.split(".")[3]
                )

            # ?.?.11.?
            if list1[0] == "?" and list1[2] == "?" and list1[3] == "?":
                return (
                    varIP.split(".")[0]
                    + "."
                    + varPartIP.split(".")[1]
                    + "."
                    + varIP.split(".")[2]
                    + "."
                    + varIP.split(".")[3]
                )

            # ?.?.?.11
            if list1[0] == "?" and list1[1] == "?" and list1[2] == "?":
                return (
                    varIP.split(".")[0]
                    + "."
                    + varIP.split(".")[1]
                    + "."
                    + varIP.split(".")[2]
                    + "."
                    + varPartIP.split(".")[3]
                )

            # 11.12.?.?
            if list1[2] == "?" and list1[3] == "?":
                return (
                    varPartIP.split(".")[0]
                    + "."
                    + varPartIP.split(".")[1]
                    + "."
                    + varIP.split(".")[2]
                    + "."
                    + varIP.split(".")[3]
                )

            # ?.11.22.?
            if list1[0] == "?" and list1[3] == "?":
                return (
                    varIP.split(".")[0]
                    + "."
                    + varPartIP.split(".")[1]
                    + "."
                    + varPartIP.split(".")[2]
                    + "."
                    + varIP.split(".")[3]
                )

            # ?.?.11.12
            if list1[0] == "?" and list1[1] == "?":
                return (
                    varIP.split(".")[0]
                    + "."
                    + varIP.split(".")[1]
                    + "."
                    + varPartIP.split(".")[2]
                    + "."
                    + varPartIP.split(".")[3]
                )

            # ?.11.11.11
            if list1[0] == "?":
                return (
                    varIP.split(".")[0]
                    + "."
                    + varPartIP.split(".")[1]
                    + "."
                    + varPartIP.split(".")[2]
                    + "."
                    + varPartIP.split(".")[3]
                )

            # 11.?.11.11
            if list1[1] == "?":
                return (
                    varPartIP.split(".")[0]
                    + "."
                    + varIP.split(".")[1]
                    + "."
                    + varPartIP.split(".")[2]
                    + "."
                    + varPartIP.split(".")[3]
                )

            # 11.11.?.11
            if list1[2] == "?":
                return (
                    varPartIP.split(".")[0]
                    + "."
                    + varPartIP.split(".")[1]
                    + "."
                    + varIP.split(".")[2]
                    + "."
                    + varPartIP.split(".")[3]
                )

            # 11.11.11.?
            if list1[3] == "?":
                return (
                    varPartIP.split(".")[0]
                    + "."
                    + varPartIP.split(".")[1]
                    + "."
                    + varPartIP.split(".")[2]
                    + "."
                    + varIP.split(".")[3]
                )
        else:
            print(
                "[ERROR], "
                + sys._getframe(1).f_code.co_name
                + ", line "
                + str(sys._getframe(1).f_lineno)
                + ", in "
                + sys._getframe(0).f_code.co_name
                + ", SourceFile '"
                + sys._getframe().f_code.co_filename
                + "'"
            )

    def getIp2(self):

        """2.3.2，生成IP2"""

        return socket.inet_ntoa(struct.pack(">I", random.randint(1, 0xFFFFFFFF)))

    def getSeriesIp(self, varFirstIP, varNum):

        """2.3.3，获取连续n个IP"""

        # 如 getSeriesIP('101.23.228.253', 5)
        starts = varFirstIP.split(".")
        A = int(starts[0])
        B = int(starts[1])
        C = int(starts[2])
        D = int(starts[3])
        l_ip = []
        for A in range(A, 256):
            for B in range(B, 256):
                for C in range(C, 256):
                    for D in range(D, 256):
                        ip = "%d.%d.%d.%d" % (A, B, C, D)
                        if varNum > 1:
                            varNum -= 1
                            l_ip.append(ip)
                        elif varNum == 1:  # 解决最后多一行回车问题
                            varNum -= 1
                            l_ip.append(ip)
                        else:
                            return l_ip
                    D = 0
                C = 0
            B = 0

    def getMd5(self, varText):

        """2.4.1，生成MD5加密值"""
        # 分析：加密输出是16进制的md5值，这里传入的字符串前加个b将其转为二进制，或者声明为utf-8, 否则回报错误TypeError: Unicode-objects must be encoded before hashing

        m = hashlib.md5(
            varText.encode(encoding="utf-8")
        )  # 等同于 m = hashlib.md5(b'123456')
        return m.hexdigest()

    def getMd5Segment(self, *varText):

        """2.4.2，生成MD5分段加密值"""
        # 一般用在数据太长时，进行分段加密。

        m = hashlib.md5()
        for i in range(len(varText)):
            m.update(varText[i].encode("utf-8"))
        return m.hexdigest()

    def getUUID(self, varMode, varName="jinhao"):

        """2.5，生成uuid
        # UUID是128位的全局唯一标识符，通常由32字节的字符串表示。
        """

        if varMode == "uuid1":
            # 从主机ID，序列号和当前时间生成UUID
            return uuid.uuid1().hex
        elif varMode == "md5":
            # 把一个UUID和name经过MD5生成UUID
            return uuid.uuid3(uuid.uuid1(), varName).hex
        elif varMode == "random":
            # 生成一个随机UUID
            return uuid.uuid4().hex
        elif varMode == "sh1":
            # 把一个UUID和name经过sha1生成UUID
            return uuid.uuid5(uuid.uuid1(), varName).hex

    def getQR(self, varURL, varSavePic):

        """2.6，生成二维码"""

        # from MyQR import myqr
        # 扫描二维码，直接访问words网址
        myqr.run(words=varURL, colorized=False, save_name=varSavePic)

    def getAddressByQR(self, varTwoDimensionCodePic):

        """2.6.1，获取二维码的地址"""

        # from pyzbar.pyzbar import decode
        # from PIL import Image
        img = Image.open(varTwoDimensionCodePic)
        bar = decode(img)[0]
        result = bar.data.decode()
        print(result)

    def getNumnberIndex(self, path=""):

        """3.1，获取字符串中数字的位置(索引)"""
        # print(getNumnberIndex("abc1test2ok"))  # [['1', 3], ['2', 8]]  第一个数字在位置3，第二个数字在位置8

        kv = []
        nums = []
        beforeDatas = re.findall("\d", path)
        for num in beforeDatas:
            indexV = []
            times = path.count(num)
            if times > 1:
                if num not in nums:
                    indexs = re.finditer(num, path)
                    for index in indexs:
                        iV = []
                        i = index.span()[0]
                        iV.append(num)
                        iV.append(i)
                        kv.append(iV)
                nums.append(num)
            else:
                index = path.find(num)
                indexV.append(num)
                indexV.append(index)
                kv.append(indexV)
        # 根据数字位置排序
        indexSort = []
        resultIndex = []
        for vi in kv:
            indexSort.append(vi[1])
        indexSort.sort()
        for i in indexSort:
            for v in kv:
                if i == v[1]:
                    resultIndex.append(v)
        return resultIndex

    def getRepeatCount(self, varStr, varChar):

        """3.2，获取字符串中字符重复的次数"""

        return varStr.count(varChar)

    def getWordQty(self, pathfile, word):

        """3.3，获取文档里单词数量"""

        # print(Data_PO.getWordQty(r"D:\51\python\project\instance\zyjk\BI\web\log\bi_20200430.log", "INFO"))
        f = open(pathfile, encoding="utf-8")
        ms = f.read().split()
        count = {}
        for m in ms:
            if m in count:
                count[m] += 1
            else:
                count[m] = 1
        for m in count:
            if m == word:
                return count[m]


if __name__ == "__main__":

    Data_PO = DataPO()

    # print("1.1，随机获取中文用户名".center(100, "-"))
    # print(Data_PO.getChineseName())  # 陈恋柏
    #
    # print("1.2，随机获取手机号码".center(100, "-"))
    # print(Data_PO.getPhone())  # 14790178656
    #
    # print("1.3，随机获取n位数".center(100, "-"))
    # print(Data_PO.getFigures(11))  # 47734406074
    #
    # print("1.4，随机获取n个整数".center(100, "-"))
    # print(Data_PO.getIntList(101, 10))
    #
    # print("1.5，随机获取列表中元素".center(100, "-"))
    # print(Data_PO.getElement(['411', '1023', '0906', '0225'], 2))  # ['1023', '0906']
    #
    # print("1.6，随机获取国内高匿ip代理".center(100, "-"))
    # print(Data_PO.getProxies())
    # print(Data_PO.getProxies())
    # print(Data_PO.getProxies())

    # print("1.7.1，随机获取用户代理1".center(100, "-"))
    # print(Data_PO.getUserAgent())

    # print("1.7.2，随机获取用户代理2(访问fake地址)".center(100, "-"))
    # print(Data_PO.getUserAgent2("https://fake-useragent.herokuapp.com/browsers/0.1.11"))
    #
    # print("1.7.3，随机获取用户代理3(解析fake地址另存为json，本地访问json文件) ".center(100, "-"))
    # print(Data_PO.getUserAgent3("userAgent.json", "None"))  # 不解析fake，直接访问json文件
    # print(Data_PO.getUserAgent3("userAgent.json"))  # 解析fake，生成并访问json
    # print(Data_PO.getUserAgent3("userAgent.json", "https://fake-useragent.herokuapp.com/browsers/0.1.11")) # 解析fake，生成并访问json

    # print("2.1，生成身份证号".center(100, "-"))
    # print(Data_PO.getIdCard())   # 441427196909022802
    #
    # print("2.1.1，获取身份证出生年月".center(100, "-"))
    # print(Data_PO.getBirthday(Data_PO.getIdCard()))  # ('1965', '04', '16')
    # print(Data_PO.getBirthday("31ceshi141212"))  # None
    #
    # print("2.1.2，获取身份证年龄".center(100, "-"))
    # print(Data_PO.getAge("310101198004110014"))  # 40
    #
    # print("2.1.3，获取身份证性别".center(100, "-"))
    # print(Data_PO.getSex("310101198004110014"))  # 男
    #
    # print("2.1.4,  获取身份证校验码".center(100, "-"))
    # print(Data_PO.getCheckCode("31010119570412128X"))
    #
    # print("2.1.5，判断身份证有效性".center(100, "-"))
    # print(Data_PO.isIdCard(Data_PO.getIdCard()))
    # print(Data_PO.isIdCard("310101200902089077"))
    #
    # print("2.3.1，生成IP".center(100, "-"))
    # print(Data_PO.getIp(""))  # 116.210.48.8
    #
    # print("2.3.2，生成IP2 ".center(100, "-"))
    # x = Data_PO.getIp2()
    # print(x)  # 36.93.19.190  //随机生成一个IP地址2
    #
    # print("2.3.3，获取连续n个IP".center(100, "-"))
    # print(Data_PO.getSeriesIp('101.23.228.254', 4))   # ['101.23.228.254', '101.23.228.255', '101.23.229.0', '101.23.229.1']
    # print(Data_PO.getSeriesIp(x, 7))   # ['101.23.228.254', '101.23.228.255', '101.23.229.0', '101.23.229.1']
    #
    # print("2.4.1，生成MD5加密值".center(100, "-"))
    # print(Data_PO.getMd5('123456'))  # e10adc3949ba59abbe56e057f20f883e
    #
    # print("2.4.2，生成MD5分段加密值".center(100, "-"))
    # print(Data_PO.getMd5Segment('123', '45', "6"))  # e10adc3949ba59abbe56e057f20f883e
    #
    # print("2.5，生成uuid ".center(100, "-"))
    # print(Data_PO.getUUID("uuid1"))
    print(Data_PO.getUUID("md5"))
    # print(Data_PO.getUUID("random"))
    # print(Data_PO.getUUID("sh1"))

    # print("2.6，生成二维码".center(100, "-"))
    # Data_PO.getQR("https://www.baidu.com", "./data/baidu.jpg")

    # print("2.6.1，获取二维码的地址".center(100, "-"))
    # Data_PO.getAddressByQR("./DataPO/baidu.jpg")

    # print("3.1，获取字符串中数字的位置(索引)".center(100, "-"))
    # print(Data_PO.getNumnberIndex("abc1test2ok"))  #[['1', 3], ['2', 8]]  第一个数字在位置3，第二个数字在位置8
    #
    # print("3.2，获取字符串中字符重复的次数".center(100, "-"))
    # print(Data_PO.getRepeatCount("123%s1232%s34%", "%s"))  # 2
    # print(Data_PO.getRepeatCount("123%123234%", "?"))  # 0
    #
    # print("3.3，获取文档里单词数量".center(100, "-"))
    # print(Data_PO.getWordQty(r"D:\51\python\project\instance\zyjk\BI\web\log\bi_20200430.log", "INFO"))

