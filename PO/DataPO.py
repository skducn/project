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
'''
1，随机生成中文用户名 getChineseName()
2，随机生成手机号码 getPhone()

3.1 随机生成身份证号 getIdCard()
3.2，判断是否是有效身份证 isIdCard()
3.3，获取身份证的出生年月(只限大陆身份证) getDateOfBirthById()
3.4，获取身份证的年龄 getAgeById()
3.5，获取身份证的性别 getSexById()
3.6 通过身份证号获取校验码 getCheckCodeById()

4，随机生成n个数字 getFigures()

5.1，随机生成一个有效IP  getIp()
5.2，随机生成一个有效IP2  getIP2()
5.3，从当前IP地址开始连续生成N个IP  getSeriesIp()

6，从列表中随机获取n个元素 getElement()

8.1，用MD5加密内容 md5()
8.2，MD5分段加密 md5Segment()

9，获取文档里某个单词出现的数量  getFQCY()
10，生成uuid  getUUID()

11.1, 生成二维码 getQR()
11.2 获取二维码的地址  getAddressByQR()

12，获取国内高匿ip代理  getIpAgent()

13.1 随机获取用户代理 getUserAgent()
13.2 获取用户代理 getUserAgent2()
13.3 将fake包用户代理信息写入文档  setFileByUserAgent()
13.4 从fake文件中获取用户代理 getUserAgentFromFile()

14 随机获取1-101之间的20个整数 getRandomInt()

15 优化round 四舍五入 newRound()

'''

import sys, random, json, jsonpath, hashlib, socket, struct, re, uuid, requests,datetime
import random
from datetime import date
from datetime import timedelta
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import pandas as pd
from MyQR import myqr
# from pyzbar.pyzbar import decode
from PIL import Image

class DataPO():


    def getChineseName(self):
        
        # 1，随机生成中文用户名
        
        a1 = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许', '何', '吕', '施', '张']
        a2 = ['玉', '明', '龙', '芳', '军', '玲', '一', '美', '恋', '世', '亮', '佳']
        a3 = ['栋', '玲', '', '国', '', '浩', '秋', '涛', '', '杰', '', '华', '伟', '荣', '兴', '柏', '', '桦']
        return random.choice(a1) + random.choice(a2) + random.choice(a3)
        # return unicode(name, "utf-8")

    def getPhone(self):

        # 2，随机生成手机号码

        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153", "155", "156", "157", "158", "159", "186", "187", "188","199"]
        return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))



    def getIdCard(self, areaCode = '110102', start="1950-01-01"):

        """
        3.1 随机生成身份证号
        areaCode 是区域码，可通过国家统计局获取所有地区的区域码，这里写死一个。
        start 是开始时间，即只生成start到现在的出生日期
        """

        end = str(date.today())
        days = (datetime.datetime.strptime(end, "%Y-%m-%d") - datetime.datetime.strptime(start, "%Y-%m-%d")).days + 1
        birth_days = datetime.datetime.strftime(
            datetime.datetime.strptime(start, "%Y-%m-%d") + datetime.timedelta(random.randint(0, days)), "%Y%m%d"
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

    def isIdCard(self, id_card):
        
        # 3.2 判断是否是有效身份证
        
        # errors = ['验证通过!', '身份证号码位数不对!', '身份证号码出生日期超出范围或含有非法字符!', '身份证号码校验错误!', '身份证地区非法!']
        errors = [True, False, False, False, False]
        area = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁", "22": "吉林", "23": "黑龙江",
                "31": "上海", "32": "江苏", "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", "37": "山东", "41": "河南",
                "42": "湖北",
                "43": "湖南", "44": "广东", "45": "广西", "46": "海南", "50": "重庆", "51": "四川", "52": "贵州", "53": "云南",
                "54": "西藏",
                "61": "陕西", "62": "甘肃", "63": "青海", "64": "宁夏", "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门",
                "91": "国外"}
        id_card = str(id_card)
        id_card = id_card.strip()  # 删除前后空格
        id_card_list = list(id_card)

        # 地区校验
        if not area[id_card[0:2]]:
            return(errors[4])

        # 15位身份号码检测
        if len(id_card) == 15:
            if ((int(id_card[6:8]) + 1900) % 4 == 0 or (
                    (int(id_card[6:8]) + 1900) % 100 == 0 and (int(id_card[6:8]) + 1900) % 4 == 0)):
                e_reg = re.compile(
                    '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|'
                    '[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$')  # //测试出生日期的合法性
            else:
                e_reg = re.compile(
                    '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|'
                    '[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$')  # //测试出生日期的合法性
            if re.match(e_reg, id_card):
                return(errors[0])
            else:
                return(errors[2])

        # 18位身份号码检测
        elif len(id_card) == 18:
            # 出生日期的合法性检查
            if int(id_card[6:10]) % 4 == 0 or (int(id_card[6:10]) % 100 == 0 and int(id_card[6:10]) % 4 == 0):
                e_reg = re.compile(
                    '[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)'
                    '(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')  # //闰年出生日期的合法性正则表达式
            else:
                e_reg = re.compile(
                    '[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)'
                    '(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')  # //平年出生日期的合法性正则表达式
            # //测试出生日期的合法性
            if re.match(e_reg, id_card):
                # //计算校验位
                S = (int(id_card_list[0]) + int(id_card_list[10])) * 7 + (int(id_card_list[1]) +
                                                                          int(id_card_list[11])) * 9 + (
                            int(id_card_list[2]) + int(id_card_list[12])) * 10 + (
                            int(id_card_list[3]) + int(id_card_list[13])) * 5 + (
                            int(id_card_list[4]) + int(id_card_list[14])) * 8 + (
                            int(id_card_list[5]) + int(id_card_list[15])) * 4 + (
                            int(id_card_list[6]) + int(id_card_list[16])) * 2 + int(id_card_list[7]) * 1 + int(
                    id_card_list[8]) * 6 + int(id_card_list[9]) * 3
                Y = S % 11
                M = "F"
                JYM = "10X98765432"
                M = JYM[Y]  # 判断校验位
                # print(S)
                # print(Y)
                # print(M)
                if M == id_card_list[17]:  # 检测ID的校验位
                    return(errors[0])
                else:
                    return(errors[3])
            else:
                return(errors[2])
        else:
            return(errors[1])

    def getDateOfBirthById(self, varIdcard):

        # 3.3 获取身份证的出生年月(只限大陆身份证)

        # 先判断身份证是否有效
        if Data_PO.isIdCard(varIdcard) == True:
            yearMonthDay = (varIdcard[6:10], varIdcard[10:12], varIdcard[12:14])
            return yearMonthDay
        else:
            return None

    def getAgeById(self, varIdcard):
        
        # 3.4 获取身份证的年龄

        # 先判断身份证是否有效
        if Data_PO.isIdCard(varIdcard) == True:
            Date = varIdcard[6:10] + "." + varIdcard[10:12] + "." + varIdcard[12:14]
            Date = Date.split('.')
            BirthDate = datetime.date(int(Date[0]), int(Date[1]), int(Date[2]))
            Today = datetime.date.today()
            if (Today.month > BirthDate.month):
                NextYear = datetime.date(Today.year + 1, BirthDate.month, BirthDate.day)
            elif (Today.month < BirthDate.month):
                NextYear = datetime.date(Today.year, Today.month + (BirthDate.month - Today.month), BirthDate.day)
            elif (Today.month == BirthDate.month):
                if (Today.day > BirthDate.day):
                    NextYear = datetime.date(Today.year + 1, BirthDate.month, BirthDate.day)
                elif (Today.day < BirthDate.day):
                    NextYear = datetime.date(Today.year, BirthDate.month, Today.day + (BirthDate.day - Today.day))
                elif (Today.day == BirthDate.day):
                    NextYear = 0
            Age = Today.year - BirthDate.year
            if NextYear == 0:  # if today is the birthday
                return '%d' % (Age)
                # return '%d, days until %d: %d' % (Age, Age+1, 0)
            else:
                DaysLeft = NextYear - Today
                return '%d' % (Age)
                # return '%d, days until %d: %d' % (Age, Age+1, DaysLeft.days)
        else:
            return None

    def getSexById(self, varIdcard):

        # 3.5 获取身份证的性别

        # 先判断身份证是否有效
        if Data_PO.isIdCard(varIdcard) == True:
            if (int(varIdcard[16:17]) % 2) == 0:
                # print("{0} 是偶数".format(IdCard[16:17]))
                return u"女"
            else:
                # print("{0} 是奇数".format(IdCard[16:17]))
                return u"男"
        else:
            return None

    def getCheckCodeById(self, areaCode):

        # 3.6 通过身份证号获取校验码

        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * int(areaCode[i])
        check_digit = (12 - (check_sum % 11)) % 11
        return check_digit if check_digit < 10 else 'X'



    def getFigures(self, n):

        # 4 随机生成N位数字
        # 如 Data_PO.rdNum(8)

        ret = []
        try:
            for i in range(n):
                while 1:
                    number = random.randrange(0, 10)
                    if number not in ret:
                        ret.append(str(number))
                        break
            x = "".join(ret)
            return x
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")



    def getIp(self, varPartIP):
        
        # 5.1 随机生成IP
        
        # print(Data_PO.getIp(""))
        # print(Data_PO.getIp("111.222.333.444"))
        # print(Data_PO.getIp("999.?.?.?"))
        # print(Data_PO.getIp("?.999.?.?"))
        # print(Data_PO.getIp("?.?.999.?"))
        # print(Data_PO.getIp("?.?.?.999"))
        # print(Data_PO.getIp("999.888.?.?"))
        # print(Data_PO.getIp("?.999.888.?"))
        # print(Data_PO.getIp("?.?.999.888"))
        # print(Data_PO.getIp("?.777.888.999"))
        # print(Data_PO.getIp("777.?.555.666"))
        # print(Data_PO.getIp("111.222.?.444"))
        # print(Data_PO.getIp("111.222.333.?"))
        varIP = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        list1 = varPartIP.split(".")[:]
        if varPartIP == "":
            return varIP
        elif varPartIP.count(".") == 3:

            if "?" not in varPartIP:
                return varPartIP

            # 11.?.?.?
            if list1[1] == "?" and list1[2] == "?" and list1[3] == "?":
                return varPartIP.split(".")[0] + "." + varIP.split(".")[1] + "." + varIP.split(".")[2] + "." + varIP.split(".")[3]

            # ?.11.?.?
            if list1[0] == "?" and list1[1] == "?" and list1[3] == "?":
                return varIP.split(".")[0] + "." + varIP.split(".")[1] + "." + varPartIP.split(".")[2] + "." + varIP.split(".")[3]

            # ?.?.11.?
            if list1[0] == "?" and list1[2] == "?" and list1[3] == "?":
                return varIP.split(".")[0] + "." + varPartIP.split(".")[1] + "." + varIP.split(".")[2] + "." + varIP.split(".")[3]

            # ?.?.?.11
            if list1[0] == "?" and list1[1] == "?" and list1[2] == "?":
                return varIP.split(".")[0] + "." + varIP.split(".")[1] + "." + varIP.split(".")[2] + "." + varPartIP.split(".")[3]

            # 11.12.?.?
            if list1[2] == "?" and list1[3] == "?" :
                return varPartIP.split(".")[0] + "." + varPartIP.split(".")[1] + "." + varIP.split(".")[2] + "." + varIP.split(".")[3]

            # ?.11.22.?
            if list1[0] == "?" and list1[3] == "?":
                return varIP.split(".")[0] + "." + varPartIP.split(".")[1] + "." + varPartIP.split(".")[2] + "." + varIP.split(".")[3]

            # ?.?.11.12
            if list1[0] == "?" and list1[1] == "?":
                return varIP.split(".")[0] + "." + varIP.split(".")[1] + "." + varPartIP.split(".")[2] + "." + varPartIP.split(".")[3]

            # ?.11.11.11
            if list1[0] == "?":
                return varIP.split(".")[0] + "." + varPartIP.split(".")[1] + "." + varPartIP.split(".")[2] + "." + varPartIP.split(".")[3]

            # 11.?.11.11
            if list1[1] == "?":
                return varPartIP.split(".")[0] + "." + varIP.split(".")[1] + "." + varPartIP.split(".")[2] + "." + varPartIP.split(".")[3]

            # 11.11.?.11
            if list1[2] == "?" :
                return varPartIP.split(".")[0] + "." + varPartIP.split(".")[1] + "." + varIP.split(".")[2] + "." + varPartIP.split(".")[3]

            # 11.11.11.?
            if list1[3] == "?" :
                return varPartIP.split(".")[0] + "." + varPartIP.split(".")[1] + "." + varPartIP.split(".")[2] + "." + varIP.split(".")[3]
        else:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")

    def getIp2(self):
        
        # 5.2 随机生成一个有效IP2
        
        return (socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))

    def getSeriesIp(self, varFirstIP, varNum):

        # 5.3 从当前IP地址开始连续生成N个IP

        # 如 getSeriesIP('101.23.228.253', 5)
        starts = varFirstIP.split('.')
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




    def getElement(self, l_Content, varNum):

        # 6，从列表中随机获取某个元素

        # 如：getElement(['411', '1023', '0906', '0225'],'2')
        try:
            return random.sample(l_Content, varNum)
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")




    def md5(self, varText):

        # 8.1 MD5加密字符串
        # 分析：加密输出是16进制的md5值，这里传入的字符串前加个b将其转为二进制，或者声明为utf-8, 否则回报错误TypeError: Unicode-objects must be encoded before hashing

            m = hashlib.md5(varText.encode(encoding='utf-8'))  # 等同于 m = hashlib.md5(b'123456')
            return m.hexdigest()

    def md5Segment(self, *varText):

        # 8.2 MD5分段加密字符串
        # 一般用在数据太长时，进行分段加密。

        m = hashlib.md5()
        for i in range(len(varText)):
            m.update(varText[i].encode('utf-8'))
        return m.hexdigest()





    def getFQCY(self, varPathFile, varWord):

        # 9 获取文档里某个单词出现的数量

        # print(Data_PO.getFQCY(r"D:\51\python\project\instance\zyjk\BI\web\log\bi_20200430.log", "INFO"))
        try:
            f = open(varPathFile, encoding="utf-8")
            ms = f.read().split()
            count = {}
            for m in ms:
                if m in count:
                    count[m] += 1
                else:
                    count[m] = 1
            for m in count:
                if m == varWord:
                    return (count[m])
        except:
            print("[ERROR], " +  sys._getframe(1).f_code.co_name + ", line " + str(sys._getframe(1).f_lineno) + ", in " + sys._getframe(0).f_code.co_name + ", SourceFile '" + sys._getframe().f_code.co_filename + "'")




    def getUUID(self, varMode, varName="jinhao"):

        # 10，生成uuid
        
        # UUID是128位的全局唯一标识符，通常由32字节的字符串表示。
        if varMode == "uuid1":
            # 从主机ID，序列号和当前时间生成UUID
            return uuid.uuid1().hex
        elif varMode == "md5":
            # 把一个UUID和name经过MD5生成UUID
            return (uuid.uuid3(uuid.uuid1(), varName).hex)
        elif varMode == "random":
            # 生成一个随机UUID
            return (uuid.uuid4().hex)
        elif varMode == "sh1":
            # 把一个UUID和name经过sha1生成UUID
            return (uuid.uuid5(uuid.uuid1(), varName).hex)




    def getQR(self, varURL, varSavePic):

        # 11.1 生成二维码

        # from MyQR import myqr
        # 扫描二维码，直接访问words网址
        myqr.run(words=varURL, colorized=False, save_name=varSavePic)



    def getAddressByQR(self, varTwoDimensionCodePic):

        # 11.2 获取二维码地址

        # from pyzbar.pyzbar import decode
        # from PIL import Image
        img = Image.open(varTwoDimensionCodePic)
        bar = decode(img)[0]
        result = bar.data.decode()
        print(result)





    def getIpAgent(self):

        # 12，获取国内高匿ip代理(ip代理池)

        # 爬取 https://www.kuaidaili.com/free/inha/1/ 的IP地址 ，然后进行随机获取
        baseURL = "https://www.kuaidaili.com/free"

        # 生成字典
        html = requests.get(baseURL)
        # html.encoding = 'gb2312'
        # html.encoding = 'utf-8'
        # html.encoding = 'gbk'
        bsop = BeautifulSoup(html.text.encode('gbk', 'ignore').decode('gbk'), 'html.parser')
        # bsop = BeautifulSoup(html.text, 'html.parser')


        # 获取 IP 列表
        l_ips = bsop.findAll('td', {'data-title': 'IP'})
        # print(l_ips)
        l_ip = []
        for l in l_ips:
            l_ip.append(str(l).replace('<td data-title="IP">', '').replace('</td>', ''))
        # print(l_ip)

        # 获取 PORT 列表
        l_ports = bsop.findAll('td', {'data-title': 'PORT'})
        l_port = []
        for l in l_ports:
            l_port.append(str(l).replace('<td data-title="PORT">', '').replace('</td>', ''))

        # 获取 类型 列表
        l_types = bsop.findAll('td', {'data-title': '类型'})
        l_type = []
        for l in l_types:
            l_type.append(str(l).replace('<td data-title="类型">', '').replace('</td>', ''))

        l_ipPort = []
        for i in range(len(l_ip)):
            l_ipPort.append(l_type[i] + "://" + l_ip[i] + ":" + l_port[i])

        # print(l_ipPort)
        return(l_ipPort[random.randint(0, len(l_ipPort)-1)])   # HTTP://223.243.255.4:65309




    def getUserAgent(self, varVersionUrl):

        # 13.1 随机获取用户代理(通过fake版本)

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
        final_browser = l_browsers[browsers_name][random.randint(0, len(l_browsers[browsers_name])-1)]
        return final_browser

    def getUserAgent2(self):

        # 13.4 随机获取用户代理2

        # 如报错，则更新 pip3 install -U fake-useragent
        # ua = UserAgent(use_cache_server=False)  # 禁用服务器缓存
        # ua = UserAgent(cache=False)  # 不缓存数据
        # ua = UserAgent(verify_ssl=False)  # 忽略ssl验证
        # print(ua.chrome)
        return (str(UserAgent().random))

    def setFileByUserAgent(self, varVersionUrl,toFile):

        # 13.3 将fake包用户代理信息写入文档

        my_user_agent = requests.get(varVersionUrl)
        with open(toFile, "w") as f:
            json.dump(my_user_agent.text, f)
            # json.dump(my_user_agent.text, f, ensure_ascii=False)  # 将翻译成中文。

    def getUserAgentFromFile(self, jsonFile):

        # 13.4 从fake文件中获取用户代理  （测试未通过）

        # 获取最佳读取速度
        with open(jsonFile,"r") as f:
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
            final_browser = l_browsers[browsers_name][random.randint(0, len(l_browsers[browsers_name]) - 1)]
            return final_browser



    # 14, 随机生成一批整数
    def getRandomInt(self, varEndInt, varNum):
        # random.sample()生成不相同的随机数
        return random.sample(range(1, varEndInt), varNum)


    # 15 优化round 四舍五入
    def newRound(self, varFloat):
        # 四舍五入取整， 原本遇偶数不进如：round(12.5) =12 , 遇期数进位如：round(13.5)=14 ，现优化为奇偶数都进位

        ff = int(varFloat)
        if ff % 2 == 0:
            return (round(varFloat + 1) - 1)
        else:
            return (round(varFloat))


if __name__ == '__main__':

    Data_PO = DataPO()

    # print("1 随机生成中文用户名".center(100, "-"))
    # print(Data_PO.getChineseName())  # 陈恋柏
    #
    # print("2 随机生成有效手机号码".center(100, "-"))
    # print(Data_PO.getPhone())  # 14790178656
    #
    # print("3.1 随机生成身份证号".center(100, "-"))
    # print(Data_PO.getIdCard())   # 441427196909022802   // 随机生成身份证号
    #
    # print("3.2 判断是否是有效身份证".center(100, "-"))
    # print(Data_PO.isIdCard(Data_PO.getIdCard()))
    #
    # print("3.3 获取身份证的出生年月".center(100, "-"))
    # print(Data_PO.getDateOfBirthById(Data_PO.getIdCard()))  # ('1965', '04', '16')
    # print(Data_PO.getDateOfBirthById("31ceshi141212"))  # None  //错误的身份证则返回None
    #
    # print("3.4 获取身份证的年龄".center(100, "-"))
    # print(Data_PO.getAgeById("310101198004110014"))  # 40
    #
    # print("3.5 获取身份证的性别".center(100, "-"))
    # print(Data_PO.getSexById("310101198004110014"))  # 男
    #
    # print("3.6 通过身份证号获取校验码".center(100, "-"))
    # print(Data_PO.getCheckCodeById("310101198004110014"))



    # print("4，随机生成N位数字".center(100, "-"))
    # print(Data_PO.getFigures(11))  # 6408
    #


    # print("5.1，随机生成IP".center(100, "-"))
    # print(Data_PO.getIp(""))  # 116.210.48.8  //随机生成一个IP地址
    # print("5.2，随机生成IP2".center(100, "-"))
    # print(Data_PO.getIp2())  # 36.93.19.190  //随机生成一个IP地址2

    # print("5.3，从当前IP地址开始连续生成N个IP".center(100, "-"))
    # print(Data_PO.getSeriesIp('101.23.228.254', 4))   # ['101.23.228.254', '101.23.228.255', '101.23.229.0', '101.23.229.1']
    #
    # print("6，从列表中随机获取某个元素".center(100, "-"))
    # print(Data_PO.getElement(['411', '1023', '0906', '0225'], 2))  # ['1023', '0906']
    #
    #
    # # print("8.1，MD5整段加密".center(100, "-"))
    # print(Data_PO.md5('123456'))  # e10adc3949ba59abbe56e057f20f883e
    # print("8.2，MD5分段加密".center(100, "-"))
    # print(Data_PO.md5Segment('123', '45', "6"))  # e10adc3949ba59abbe56e057f20f883e
    #
    # print("9，获取文档里某个单词出现的数量".center(100, "-"))
    # print(Data_PO.getFQCY(r"D:\51\python\project\instance\zyjk\BI\web\log\bi_20200430.log", "INFO"))
    # # print(Data_PO.getFQCY(r"D:\51\python\project\instance\zyjk\BI\web\log\bi_20200430.log", "ERROR"))
    #
    # print("10，生成uuid".center(100, "-"))
    # print(Data_PO.getUUID("uuid1"))
    # print(Data_PO.getUUID("md5"))
    # print(Data_PO.getUUID("random"))
    # print(Data_PO.getUUID("sh1"))



    # print("11.1 生成二维码".center(100, "-"))
    # Data_PO.getQR("https://www.baidu.com", "./data/baidu.jpg")

    # print("11.2 获取二维码地址".center(100, "-"))
    # Data_PO.getAddressByQR("./DataPO/baidu.jpg")



    # print("12 获取国内高匿ip代理(ip代理池)".center(100, "-"))
    # print(Data_PO.getIpAgent())
    #


    # print("13.1 随机获取用户代理".center(100, "-"))
    # print(Data_PO.getUserAgent("https://fake-useragent.herokuapp.com/browsers/0.1.11"))

    # print("13.2 获取用户代理2".center(100, "-"))
    # print(Data_PO.getUserAgent2())

    # print("13.3 将fake包用户代理信息写入文档".center(100, "-"))
    # Data_PO.setFileByUserAgent("https://fake-useragent.herokuapp.com/browsers/0.1.11", "userAgent.json")
    # # #
    # print("13.4 从fake文件中获取用户代理".center(100, "-"))
    # print(Data_PO.getUserAgentFromFile("userAgent.json"))



    # print("14 随机获取1-101之间的10个整数".center(100, "-"))
    # print(Data_PO.getRandomInt(101, 10))







