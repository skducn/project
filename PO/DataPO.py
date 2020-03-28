# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2019-9-19
# Description: 数据对象层()
# 1,随机生成中文用户名、手机号、身份证、随机N个数、IP地址、从列表中随机获取n的元素，
# 2,从身份证中获取年月日、年龄、性别，获取连续IP地址，从json中返回指定值
# 3，MD5加密内容
# 注意："DataPO.txt" 用于生成身份证号码,不能删除。
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
import random,json, jsonpath,hashlib
from datetime import date
from datetime import timedelta
import socket, random, struct, uuid
from random import choice

class DataPO():

    def rdName(self):
        ''' 随机生成中文用户名 '''
        # 如 Data_PO.rdName()
        a1 = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许', '何', '吕', '施', '张']
        a2 = ['玉', '明', '龙', '芳', '军', '玲', '一', '美', '恋', '世', '亮', '佳']
        a3 = ['栋', '玲', '', '国', '', '浩', '秋', '涛', '', '杰', '', '华', '伟', '荣', '兴', '柏', '', '桦']
        name = random.choice(a1) + random.choice(a2) + random.choice(a3)
        return name
        # return unicode(name, "utf-8")

    def rdPhone(self):
        '''随机生成手机号码'''
        # 如 Data_PO.rdPhone()
        prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "153", "155", "156", "157", "158", "159", "186", "187", "188","199"]
        return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))
    def rdIdcard(self):
        '''随机生成身份证号'''
        # 如 Data_PO.rdIdcard()
        global codelist
        codelist = []
        if not codelist:
            with open("DataPO.txt") as file:
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
    def rdNum(self, n):
        '''随机生成n个数字'''
        # 如 Data_PO.rdNum(8)
        ret = []
        for i in range(n):
            while 1:
                number = random.randrange(0, 10)
                if number not in ret:
                    ret.append(str(number))
                    break
        x = "".join(ret)
        return x
    def rdIP(self, varPartIP):
        '''自动生成一个有效IP'''
        # print(Data_PO.rdIP(""))
        # print(Data_PO.rdIP("111.222.333.444"))
        # print(Data_PO.rdIP("999.?.?.?"))
        # print(Data_PO.rdIP("?.999.?.?"))
        # print(Data_PO.rdIP("?.?.999.?"))
        # print(Data_PO.rdIP("?.?.?.999"))
        # print(Data_PO.rdIP("999.888.?.?"))
        # print(Data_PO.rdIP("?.999.888.?"))
        # print(Data_PO.rdIP("?.?.999.888"))
        # print(Data_PO.rdIP("?.777.888.999"))
        # print(Data_PO.rdIP("777.?.555.666"))
        # print(Data_PO.rdIP("111.222.?.444"))
        # print(Data_PO.rdIP("111.222.333.?"))
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
            print(u'errorrrrr - IP地址格式有误!')
            return u'error'
    def rdIP2(self):
        '''自动生成一个有效IP'''
        return (socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))

    def rdContent(self,l_Content, varNum):
        # 从列表中随机获取n个元素
        # 如：rdContent(['411', '1023', '0906', '0225'],'2')
        return random.sample(l_Content, varNum)

    def getBirthday(self, idcard):
        ''' 输入身份证(只限大陆身份证)，返回年月日 '''
        # 如 getBirthday("310101198004110014")
        yearMonthDay = (idcard[6:10], idcard[10:12], idcard[12:14])
        return yearMonthDay
    def getAge(self, idcard):
        import datetime
        '''输入身份证，返回年龄'''
        # 如 getAge('310101198004110014')
        try:
            Date = idcard[6:10] + "." + idcard[10:12] + "." + idcard[12:14]
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
        except:
            return u'errorrrrrrrrrr, 错误的身份证号码！'
    def getSex(self, idcard):
        ''' 输入身份证，返回性别（男或女）'''
        # 如：getSex("310101198004110014")
        try:
            if (int(idcard[16:17]) % 2) == 0:
                # print("{0} 是偶数".format(IdCard[16:17]))
                return u"女"
            else:
                return u"男"
                # print("{0} 是奇数".format(IdCard[16:17]))
        except:
            return u'errorrrrrrrrrr, 错误的身份证号码！'

    def getSeriesIP(self, varFirstIP, varNum):
        ''' 从当前IP地址开始连续生成N个IP '''
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

    def getJsonPath(self, varJson, varKey):
        # 解析json
        # 如：{"status":200,"msg":"success","token":"e351b73b1c6145ceab2a02d7bc8395e7"}' 获取 token的值
        # print(Net_PO.getJsonPath('{"status":200,"msg":"success","token":"e351b73b1c6145ceab2a02d7bc8395e7"}', '$.token'))
        return jsonpath.jsonpath(json.loads(varJson), expr=varKey)

    def md5(self, varContent):
        # 用MD5加密内容，结果是16进制的md5值
        # 分析：这里传入的字符串前加以个b将其转为二进制，或者声明为utf-8, 否则回报错误TypeError: Unicode-objects must be encoded before hashing
        m = hashlib.md5(varContent.encode(encoding='utf-8'))  # 等同于 m = hashlib.md5(b'123456')
        return m.hexdigest()

    def md5_update(self, *varContent):
        # 用 update 方法进行加密的好处是当数据太长时，可以分段加密，结果一样。
        m = hashlib.md5()
        for i in range(len(varContent)):
            m.update(varContent[i].encode('utf-8'))
        return m.hexdigest()

if __name__ == '__main__':
    Data_PO = DataPO()
    # print(Data_PO.rdName())
    # print(Data_PO.rdPhone())
    # print(Data_PO.rdIdcard())
    # print(Data_PO.rdNum(4))
    # print(Data_PO.rdIP(""))
    # print(Data_PO.rdIP2())

    print(Data_PO.getJsonPath('{"status":200,"msg":"success","token":"e351b73b1c6145ceab2a02d7bc8395e7"}', '$.token'))
    # print(Data_PO.rdContent(['411', '1023', '0906', '0225'], 2))
    #
    # yearMonthDay = Data_PO.getBirthday("310101198004110014")
    # print(yearMonthDay[0] + "-" + yearMonthDay[1] + "-" + yearMonthDay[2])
    # print(Data_PO.getAge("310101198004110014"))
    # print(Data_PO.getSex("310101198004110014"))
    # x = Data_PO.getSeriesIP('101.23.228.12', 4)
    # print(x)
    #
    # print(Data_PO.md5('123456'))
    # print(Data_PO.md5_update('123', '45', "6"))
