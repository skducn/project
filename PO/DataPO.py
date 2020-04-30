# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2019-9-19
# Description: 数据对象层
# jsonpath官网 https://goessner.net/articles/JsonPath/
# 线上的一个json文档用于测试，https://www.lagou.com/lbs/getAllCitySearchLabels.json
# Description: md5(python2),hashlib(python3)
# MD5消息摘要算法（英语：MD5 Message-Digest Algorithm），一种被广泛使用的密码散列函数，
# 可以产生出一个128位（16字节）的散列值（hash value），用于确保信息传输完整一致。
# 什么是摘要算法呢？摘要算法又称哈希算法、散列算法。它通过一个函数，把任意长度的数据转换为一个长度固定的数据串（通常用16进制的字符串表示）
# # 如果要被加密的数据太长，可以分段update，结果是一样的，如下：
# m = hashlib.md5()
# m.update('12345'.encode('utf-8'))
# m.update('6'.encode('utf-8'))
# print(m.hexdigest())  # e10adc3949ba59abbe56e057f20f883e
# ***************************************************************
'''
1，随机生成中文用户名
2，随机生成手机号码

3.1，随机生成身份证号 （依赖于 getRandomIdcard.txt ）
3.2，判断是否是有效身份证
3.3，获取身份证的出生年月(只限大陆身份证)
3.4，获取身份证的年龄
3.5，获取身份证的性别

4，随机生成n个数字

5.1，随机生成一个有效IP
5.2，随机生成一个有效IP2
5.3，从当前IP地址开始连续生成N个IP

6，从列表中随机获取n个元素
7，解析json

8.1，用MD5加密内容
8.2，MD5分段加密

9，获取文档里某个单词出现的数量
'''

import random,json, jsonpath, hashlib,socket, struct, re,datetime
from datetime import date
from datetime import timedelta


class DataPO():

    # 1，随机生成中文用户名
    def getRandomName(self):
        # 随机生成中文用户名
        a1 = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许', '何', '吕', '施', '张']
        a2 = ['玉', '明', '龙', '芳', '军', '玲', '一', '美', '恋', '世', '亮', '佳']
        a3 = ['栋', '玲', '', '国', '', '浩', '秋', '涛', '', '杰', '', '华', '伟', '荣', '兴', '柏', '', '桦']
        return random.choice(a1) + random.choice(a2) + random.choice(a3)
        # return unicode(name, "utf-8")

    # 2，随机生成手机号码
    def getRandomPhone(self):
        # 随机生成手机号码
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153", "155", "156", "157", "158", "159", "186", "187", "188","199"]
        return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))

    # 3.1，随机生成身份证号
    def getRandomIdcard(self):
        # 随机生成身份证号
        # 如 Data_PO.rdIdcard()
        global codelist
        codelist = []
        if not codelist:
            with open("getRandomIdcard.txt") as file:
                data = file.read()
                districtlist = data.split('\n')
            for node in districtlist:
                # print node
                if node[10:11] != ' ':
                    state = node[10:].strip()
                if node[10:11] == ' ' and node[12:13] != ' ':
                    city = node[12:].strip()
                if node[10:11] == ' ' and node[12:13] == ' ':
                    district = node[14:].strip()
                    code = node[0:6]
                    codelist.append({"state": state, "city": city, "district": district, "code": code})
        id = codelist[random.randint(0, len(codelist))]['code']  # 地区项
        id = id + str(random.randint(1930, 2013))  # 年份项
        da = date.today() + timedelta(days=random.randint(1, 366))  # 月份和日期项
        id = id + da.strftime('%m%d')
        id = id + str(random.randint(100, 300))  # ，顺序号简单处理
        i = 0
        count = 0
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
        # checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3','10': '2'}  # 校验码映射
        checkcode = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']  # mod11,对应校验码字符值
        for i in range(0, len(id)):
            count = count + int(id[i]) * weight[i]
        id = id + checkcode[count % 11]  # 算出校验码
        return id

    # 3.2，判断是否是有效身份证
    def isIdcard(self, id_card):
        # 判断是否是有效身份证
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

    # 3.3，获取身份证的出生年月(只限大陆身份证)
    def getBirthday(self, varIdcard):
        # 获取身份证的出生年月(只限大陆身份证)
        # 先判断身份证是否有效，再获取身份证的出生年月(只限大陆身份证)
        # 如 getBirthday(getRandomIdcard())
        try:
            if Data_PO.isIdcard(varIdcard) == True:
                yearMonthDay = (varIdcard[6:10], varIdcard[10:12], varIdcard[12:14])
                return yearMonthDay
            return None
        except:
            return None

    # 3.4，获取身份证的年龄
    def getAge(self, varIdcard):
        # 获取身份证的年龄
        # 先判断身份证是否有效，再获取身份证的年龄(只限大陆身份证)
        # 如 getAge('310101198004110014')
        try:
            if Data_PO.isIdcard(varIdcard) == True:
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
            return None
        except:
            # return u'errorrrrrrrrrr, 错误的身份证号码！'
            return None

    # 3.5，获取身份证的性别
    def getSex(self, varIdcard):
        # 获取身份证的性别
        # 先判断身份证是否有效，再获取身份证的性别(只限大陆身份证)
        # 如：getSex("310101198004110014")
        try:
            if Data_PO.isIdcard(varIdcard) == True:
                if (int(varIdcard[16:17]) % 2) == 0:
                    # print("{0} 是偶数".format(IdCard[16:17]))
                    return u"女"
                else:
                    # print("{0} 是奇数".format(IdCard[16:17]))
                    return u"男"
            return None
        except:
            # return u'errorrrrrrrrrr, 错误的身份证号码！'
            return


    # 4，随机生成n个数字
    def getRandomNum(self, n):
        # 随机生成n个数字
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
            return None

    # 5.1，随机生成一个有效IP
    def getRandomIp(self, varPartIP):
        # 随机生成一个有效IP
        # print(Data_PO.getRandomIp(""))
        # print(Data_PO.getRandomIp("111.222.333.444"))
        # print(Data_PO.getRandomIp("999.?.?.?"))
        # print(Data_PO.getRandomIp("?.999.?.?"))
        # print(Data_PO.getRandomIp("?.?.999.?"))
        # print(Data_PO.getRandomIp("?.?.?.999"))
        # print(Data_PO.getRandomIp("999.888.?.?"))
        # print(Data_PO.getRandomIp("?.999.888.?"))
        # print(Data_PO.getRandomIp("?.?.999.888"))
        # print(Data_PO.getRandomIp("?.777.888.999"))
        # print(Data_PO.getRandomIp("777.?.555.666"))
        # print(Data_PO.getRandomIp("111.222.?.444"))
        # print(Data_PO.getRandomIp("111.222.333.?"))
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
            return None

    # 5.2，随机生成一个有效IP2
    def getRandomIp2(self):
        # 随机生成一个有效IP2
        return (socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))

    # 5.3，从当前IP地址开始连续生成N个IP
    def getSeriesIp(self, varFirstIP, varNum):
        # 从当前IP地址开始连续生成N个IP
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


    # 6，从列表中随机获取某个元素
    def getRandomContent(self, l_Content, varNum):
        # 从列表中随机获取n个元素
        # 如：rdContent(['411', '1023', '0906', '0225'],'2')
        try:
            return random.sample(l_Content, varNum)
        except:
            return None


    # 7，解析json
    def getJsonPath(self, varJson, varKey):
        # 解析json
        # 如：{"status":200,"msg":"success","token":"e351b73b1c6145ceab2a02d7bc8395e7"}' 获取 token的值
        # print(Net_PO.getJsonPath('{"status":200,"msg":"success","token":"e351b73b1c6145ceab2a02d7bc8395e7"}', '$.token'))
        try:
            return jsonpath.jsonpath(json.loads(varJson), expr=varKey)
        except:
            return None

    # 8.1，MD5整段加密
    def md5(self, varContent):
        # MD5字符串加密
        # 分析：加密输出是16进制的md5值，这里传入的字符串前加个b将其转为二进制，或者声明为utf-8, 否则回报错误TypeError: Unicode-objects must be encoded before hashing
        try:
            m = hashlib.md5(varContent.encode(encoding='utf-8'))  # 等同于 m = hashlib.md5(b'123456')
            return m.hexdigest()
        except:
            return None

    # 8.2，MD5分段加密
    def md5Segment(self, *varContent):
        # MD5分段加密
        # 主要用在数据太长时，可分段加密，结果一样。
        try:
            m = hashlib.md5()
            for i in range(len(varContent)):
                m.update(varContent[i].encode('utf-8'))
            return m.hexdigest()
        except:
            return None

    # 9，获取文档里某个单词出现的数量
    def getNumByText(self, varPathFile, varWord):
        # print(Data_PO.getNumByText(r"D:\51\python\project\instance\zyjk\BI\web\log\bi_20200430.log", "INFO"))
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
            return None

if __name__ == '__main__':

    Data_PO = DataPO()

    print("1，随机生成中文用户名".center(100, "-"))
    print(Data_PO.getRandomName())  # 陈恋柏

    print("2，随机生成有效手机号码".center(100, "-"))
    print(Data_PO.getRandomPhone())  # 14790178656

    print("3.1，随机生成身份证号".center(100, "-"))
    print(Data_PO.getRandomIdcard())   # 441427196909022802   // 随机生成身份证号

    print("3.2，判断是否是有效身份证".center(100, "-"))
    print(Data_PO.isIdcard(Data_PO.getRandomIdcard()))
    print(Data_PO.isIdcard("31012547854125"))

    print("3.3，获取身份证的出生年月(只限大陆身份证)".center(100, "-"))
    print(Data_PO.getBirthday(Data_PO.getRandomIdcard()))  # ('1965', '04', '16')
    print(Data_PO.getBirthday("31ceshi141212"))  # None  //错误的身份证则返回None

    print("3.4，获取身份证的年龄".center(100, "-"))
    print(Data_PO.getAge("310101198004110014"))  # 40

    print("3.5，获取身份证的性别".center(100, "-"))
    print(Data_PO.getSex("310101198004110014"))  # 男

    print("4，随机生成n个数字".center(100, "-"))
    print(Data_PO.getRandomNum(4))  # 6408  //随机生成4个数字

    print("5.1，随机生成一个有效IP".center(100, "-"))
    print(Data_PO.getRandomIp(""))  # 116.210.48.8  //随机生成一个IP地址
    print("5.2，随机生成一个有效IP2".center(100, "-"))
    print(Data_PO.getRandomIp2())  # 36.93.19.190  //随机生成一个IP地址2
    print("5.3，从当前IP地址开始连续生成N个IP".center(100, "-"))
    print(Data_PO.getSeriesIp('101.23.228.254', 4))   # ['101.23.228.254', '101.23.228.255', '101.23.229.0', '101.23.229.1']

    print("6，从列表中随机获取某个元素".center(100, "-"))
    print(Data_PO.getRandomContent(['411', '1023', '0906', '0225'], 2))  # ['1023', '0906']

    print("7，解析json".center(100, "-"))
    print(Data_PO.getJsonPath('{"status":200,"msg":"success","token":"e351b73b1c6145ceab2a02d7bc8395e7"}', '$.token'))  # ['e351b73b1c6145ceab2a02d7bc8395e7']

    print("8.1，MD5整段加密".center(100, "-"))
    print(Data_PO.md5('123456'))  # e10adc3949ba59abbe56e057f20f883e
    print("8.2，MD5分段加密".center(100, "-"))
    print(Data_PO.md5Segment('123', '45', "6"))  # e10adc3949ba59abbe56e057f20f883e

    print("9，获取文档里某个单词出现的数量".center(100, "-"))
    # print(Data_PO.getNumByText(r"D:\51\python\project\instance\zyjk\BI\web\log\bi_20200430.log", "INFO"))
    # print(Data_PO.getNumByText(r"D:\51\python\project\instance\zyjk\BI\web\log\bi_20200430.log", "ERROR"))