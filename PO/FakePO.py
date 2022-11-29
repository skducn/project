# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2019-9-19
# Description: fake
# 关于大数据测试，你一定要试试python的fake库！ http://www.51testing.com/html/53/15150753-7793925.html
# 官网 https://faker.readthedocs.io/en/master/
# pip3.9 install faker

# 银行卡号查询 https://www.haoshudi.com/yinhangka/
# 身份证查询 https://www.haoshudi.com/shenfenzheng/
# 手机号码查询 https://www.shoujichahao.com/，https://www.haoshudi.com/
# ***************************************************************

'''
1 生成N个姓名 genName
2 生成N个身份证 genSsn
3 生成N个手机号   genPhone_numbe
4 生成N个Email genEmail
5 生成N个地址  genAddress
6 生成N个邮编  genPostcode
7 生成N个公司  genCompany
8 生成N个url  genUrl
9 生成N个ip  genIpv4
10 生成N个经度纬度  genLatitudeLongitude
11 生成N个text  genText

生成N个测试数据  genTest
'''

import sys,os
from faker import Faker
from faker.providers import internet
from PO.pandasPO import *


list1 = []
list3 = ['今天', '你好', '谢谢', '意愿']


class FakePO():

    def __init__(self):

        self.faker = Faker(locale='zh_CN')


    def genName(self, country, n=1):

        '''1 生成N个姓名 '''

        list1 = []
        faker = Faker(locale=country)
        if n == 1:
            return faker.name()
        elif n > 0:
            for i in range(n):
                list1.append(faker.name())
        else:
            return None
        return list1

    def genSsn(self, country, n=1):

        '''2 生成N个身份证 '''

        list1 = []
        faker = Faker(locale=country)
        if n == 1:
            return faker.ssn()
        elif n > 0:
            for i in range(n):
                list1.append(faker.ssn())
        else:
            return None
        return list1

    def genPhone_number(self, country, n=1):

        '''3 生成N个手机号 '''

        list1 = []
        faker = Faker(locale=country)
        if n == 1:
            return faker.phone_number()
        elif n > 0:
            for i in range(n):
                list1.append(faker.phone_number())
        else:
            return None
        return list1

    def genEmail(self, n=1):

        '''4 生成N个Email '''

        list1 = []
        if n == 1:
            return self.faker.email()
        elif n > 0:
            for i in range(n):
                list1.append(self.faker.email())
        else:
            return None
        return list1

    def genAddress(self, country, n=1):

        '''5 生成N个地址 '''

        list1 = []
        faker = Faker(locale=country)
        if n == 1:
            return faker.address()
        elif n > 0:
            for i in range(n):
                list1.append(faker.address())
        else:
            return None
        return list1

    def genPostcode(self, country, n=1):

        '''6 生成N个邮编 '''

        list1 = []
        faker = Faker(locale=country)
        if n == 1:
            return faker.postcode()
        elif n > 0 :
            for i in range(n):
                list1.append(faker.postcode())
        else:
            return None
        return list1

    def genCompany(self, country, n=1):

        '''7 生成N个公司 '''

        list1 = []
        faker = Faker(locale=country)
        if n == 1:
            return faker.company()
        elif n > 0:
            for i in range(n):
                list1.append(faker.company())
        else:
            return None
        return list1

    def genUrl(self, n=1):

        '''8 生成N个url '''

        list1 = []
        if n == 1:
            return self.faker.url()
        elif n > 0:
            for i in range(n):
                list1.append(self.faker.url())
        else:
            return None
        return list1

    def genIpv4(self, n=1):

        '''9 生成N个ip '''

        list1 = []
        if n == 1:
            return self.faker.ipv4(network=False)
        elif n > 0 :
            for i in range(n):
                list1.append(self.faker.ipv4(network=False))
        else:
            return None
        return list1

    def genLatitudeLongitude(self, n=1):

        '''10 生成N个经度纬度 '''

        dict1 = {}
        for i in range(n):
            longitude = str(self.faker.longitude())
            latitude = str(self.faker.latitude())
            dict1[longitude] = latitude
        return dict1

    def genText(self, country, n=1):

        '''11 生成N个text '''

        list1 = []
        faker = Faker(locale=country)
        if n == 1:
            return faker.text()
        elif n > 0 :
            for i in range(n):
                list1.append(faker.text())
        else:
            return None
        return list1



    def genTest(self, varList, n=1):

        ''' 生成N个测试数据 '''

        list1 = []
        list2 = []
        for k in range(n):
            for i in range(len(varList)):
                if varList[i] == "genName":
                    list1.append(self.faker.name())
                if varList[i] == "genSsn":
                    list1.append(self.faker.ssn())
                if varList[i] == "genPhone_number":
                    list1.append(self.faker.phone_number())
                if varList[i] == "genEmail":
                    list1.append(self.faker.email())
                if varList[i] == "genAddress":
                    list1.append(self.faker.address())
                if varList[i] == "genPostcode":
                    list1.append(self.faker.postcode())
                if varList[i] == "genCompany":
                    list1.append(self.faker.company())
                if varList[i] == "genUrl":
                    list1.append(self.faker.url())
                if varList[i] == "genIpv4":
                    list1.append(self.faker.ipv4(network=False))
                if varList[i] == "genLatitudeLongitude":
                    dict1 = {}
                    longitude = str(self.faker.longitude())
                    latitude = str(self.faker.latitude())
                    dict1[longitude] = latitude
                    list1.append(dict1)
                if varList[i] == "genText":
                    list1.append(self.faker.text())
            list2.append(list1)
            list1 = []
        return list2




if __name__ == '__main__':

    Fake_PO = FakePO()


    # print("1，生成N个姓名".center(100, "-"))
    # print(Fake_PO.genName("zh_CN", 5))  # ['曾勇', '程旭', '金云', '张桂芝', '潘凤兰']
    # print(Fake_PO.genName('ja_JP', 5))  # ['橋本 翔太', '山田 七夏', '山口 香織', '山口 陽一', '加藤 花子']
    # print(Fake_PO.genName('zh_TW', 5))  # ['陳瑋婷', '彭志偉', '李家豪', '楊淑華', '孫佩君']
    # print(Fake_PO.genName('ko_KR', 5))  # ['김병철', '김혜진', '엄영길', '이영자', '곽경숙']
    # print(Fake_PO.genName('it_IT', 5))    # ['Rembrandt Gargallo', 'Rosalia Foscari-Salvo', 'Cecilia Golino', 'Pierpaolo Zampa', 'Lando Scialpi']
    #
    # print("2，生成N个身份证".center(100, "-"))
    # print(Fake_PO.genSsn('Zh_CN', 5))  # ['220204193809145513', '441201195209216084', '620100194302246727', '640122193502253523', '370830198704231141']
    # print(Fake_PO.genSsn('ja_JP', 5))  # ['618-80-2847', '737-65-5495', '690-29-3731', '499-46-9797', '413-22-8831']
    # print(Fake_PO.genSsn('zh_TW', 5))  # ['W550839356', 'D852008578', 'P236143230', 'B097732523', 'E568438247']
    # print(Fake_PO.genSsn('ko_KR', 5))  # ['720413-2521511', '150313-2210406', '760625-1587887', '900226-2169116', '550604-2192097']
    # print(Fake_PO.genSsn('it_IT', 5))  # ['BCCLSU47T11E202R', 'VRGNCL47A48G184E', 'DLLSVN21B52B435B', 'BRTRMI99C27E349I', 'TRVTLL45M47D855M']
    #
    # print("3，生成N个手机号".center(100, "-"))
    # print(Fake_PO.genPhone_number('Zh_CN', 5))  # ['15319444539', '18607117489', '13389035662', '18704037366', '14578470103']
    # print(Fake_PO.genPhone_number('ja_JP', 5))  # ['090-1253-4485', '070-9307-1119', '37-5453-6768', '87-0312-3723', '080-3154-6896']
    # print(Fake_PO.genPhone_number('zh_TW', 5))  # ['0971-641114', '092 59296156', '06-22053548', '08-9388534', '0994-385306']
    # print(Fake_PO.genPhone_number('ko_KR', 5))  # ['055-400-2082', '061-992-5729', '043-532-2177', '063-690-2309', '031-484-4294']
    # print(Fake_PO.genPhone_number('it_IT', 5))  # ['0961775623', '+39 0709454682', '+39 0161087099', '3501400006', '+39 375743163']
    #
    # print("4，生成N个Email".center(100, "-"))
    # print(Fake_PO.genEmail(5))  # ['yanjun@example.net', 'fren@example.org', 'gang65@example.org', 'xzhang@example.net', 'qjia@example.net']
    #
    # print("5，生成N个地址".center(100, "-"))
    # print(Fake_PO.genAddress('zh_CN', 5))  # ['上海市杭州市长寿白路C座 570538', '山西省潜江县东丽巢湖街u座 213982', '黑龙江省海门县怀柔张路u座 159680', '云南省上海县金平郑路o座 699256', '香港特别行政区拉萨县朝阳张家港路K座 667767']
    # print(Fake_PO.genAddress('ja_JP', 5))  # ['徳島県川崎市高津区前弥六41丁目6番8号', '秋田県横浜市中区日光27丁目23番7号 六番町コート328', '兵庫県大田区鳥越3丁目10番18号', '静岡県新島村鍛冶ケ沢11丁目27番19号', '富山県台東区所野28丁目25番6号 平須賀シティ865']
    # print(Fake_PO.genAddress('zh_TW', 5))  # ['76220 八德縣仁愛巷9號5樓', '26059 苗栗市南路1號7樓', '32821 馬公縣永寧街77號3樓', '47049 屏東五福街292號7樓', '96189 頭份自由路3號2樓']
    # print(Fake_PO.genAddress('ko_KR', 5))  # ['전라북도 진천군 삼성로', '인천광역시 성동구 역삼213가', '경상남도 광명시 도산대가 (성호손박동)', '제주특별자치도 청주시 서원구 선릉길', '경상남도 용인시 기흥구 개포가 (지훈이동)']
    # print(Fake_PO.genAddress('it_IT', 5))  # ['Canale Asmundo, 91 Appartamento 42\n17045, Bormida (SV)', 'Piazza Mattia, 47 Appartamento 2\n83022, Baiano (AV)', 'Strada Pierpaolo, 921\n15050, Costa Vescovato (AL)', 'Viale Ughi, 19\n61023, Pietrarubbia (PU)', 'Stretto Niccolò, 1\n55047, Azzano (LU)']
    #
    # print("6，生成N个邮编".center(100, "-"))
    # print(Fake_PO.genPostcode('zh_CN', 5))  # ['921520', '747278', '556526', '438228', '523755']
    # print(Fake_PO.genPostcode('ja_JP', 5))  # ['825-4964', '091-6817', '783-7968', '643-8605', '100-8735']
    # print(Fake_PO.genPostcode('zh_TW', 5))  # ['80159', '775', '32933', '32890', '916']
    # print(Fake_PO.genPostcode('ko_KR', 5))  # ['97014', '43407', '69332', '51962', '90937']
    # print(Fake_PO.genPostcode('it_IT', 5))  # ['66051', '92021', '60123', '10154', '89014']
    #
    # print("7，生成N个公司".center(100, "-"))
    # print(Fake_PO.genCompany('zh_CN', 5))  # ['凌颖信息传媒有限公司', '太极传媒有限公司', '艾提科信网络有限公司', '网新恒天网络有限公司', '兰金电子科技有限公司']
    # print(Fake_PO.genCompany('ja_JP', 5))  # ['有限会社近藤保険', '加藤ガス株式会社', '中川銀行株式会社', '山本電気有限会社', '田中保険有限会社']
    # print(Fake_PO.genCompany('zh_TW', 5))  # ['台灣力電', '平太洋崇光百貨有限公司', '台灣台油資訊有限公司', '丹味企業', '麥當當股份有限公司']
    # print(Fake_PO.genCompany('ko_KR', 5))  # ['유한회사 장김김', '이최김', '주식회사 이', '이김한', '유한회사 권오강']
    # print(Fake_PO.genCompany('it_IT', 5))  # ['Satta, Zaccagnini e Mocenigo Group', 'Tuzzolino, Giunti e Filogamo e figli', 'Nibali, Govoni e Micca s.r.l.', 'Villarosa, Littizzetto e Canova SPA', 'Baggio, Sforza e Bonolis SPA']
    #
    # print("8，生成N个url".center(100, "-"))
    # print(Fake_PO.genUrl(5))  # ['http://fangjun.org/', 'http://www.55.cn/', 'http://www.shaodai.cn/', 'http://79.net/', 'https://www.min.net/']
    # print(Fake_PO.genUrl(1))
    #
    # print("9，生成N个ip地址".center(100, "-"))
    # print(Fake_PO.genIpv4(5))  # ['49.99.248.220', '87.134.87.25', '131.122.218.100', '209.168.88.132', '151.211.53.164']
    # print(Fake_PO.genIpv4(1))
    #
    #
    # print("10，生成N个经纬度".center(100, "-"))
    # print(Fake_PO.genLatitudeLongitude(5))  # {'-160.534852': '-60.329142', '162.865388': '-79.831936', '23.108037': '-47.045438', '-120.489596': '-16.8593375', '-75.771294': '-72.653309'}
    #
    #
    # print("11，生成N个文本".center(100, "-"))
    # print(Fake_PO.genText('zh_CN', 5))
    # print(Fake_PO.genText('ja_JP', 5))
    # print(Fake_PO.genText('zh_TW', 5))
    # print(Fake_PO.genText('ko_KR', 5))
    # print(Fake_PO.genText('it_IT', 5))


    print("12，生成10条测试数据".center(100, "-"))
    # print(Fake_PO.genTest(['genName', 'genSsn', 'genPhone_number', 'genEmail', 'genAddress', 'genPostcode', 'genCompany', 'genUrl', 'genIpv4', 'genLatitudeLongitude', 'genText'], 10))
    #  [['刘柳', '222404195311193544', '13797257259', 'moyong@example.com', '台湾省红霞市清城孙路o座 397441', '313071', '超艺网络有限公司', 'https://go.cn/', '100.42.251.31', {'-129.385847': '78.3048705'}, '处理城市国内登录今天回复能够就是.一点最新人员个人控制等级.不断手机作品大小.\n继续非常服务使用图片经验我的.业务网上很多有些.的话选择不会上海女人孩子新闻可以.\n影响记者回复今年日期她的.技术国际这个.质量进行电脑推荐今年一起.\n美国是否深圳合作.一个下载游戏.投资起来两个经营之间威望作为.\n问题建设电影类型所以任何.因为继续支持不过销售.\n一个根据同时下载.'], ['吴勇', '321183196006114279', '15374128269', 'mcai@example.org', '内蒙古自治区丽华县兴山重庆路v座 591650', '982386', '鸿睿思博网络有限公司', 'https://minyan.cn/', '129.84.30.208', {'-123.738326': '8.7047075'}, '商品作为发生注意电话.这是质量的是生产非常方面.工程方法教育一切经济.\n威望知道一直可能.进入得到电话下载关系.回复其他问题设备音乐一切汽车.\n问题开始谢谢一种威望怎么男人.登录制作一种文化行业什么当然.上海那个的人.而且行业状态只是增加帮助.\n比较需要用户发展这是美国.美国记者今年更多人民.开始希望直接.实现个人实现作者类别法律提高今天.\n继续电脑不同.部门使用组织.'], ['朱秀云', '140781200309123214', '13880431069', 'bsu@example.net', '上海市志强县平山香港路L座 611508', '625731', '银嘉科技有限公司', 'https://gangding.cn/', '189.114.120.247', {'-129.629573': '-85.7863665'}, '学生感觉发生网站这里提高.\n需要发生非常.单位上海商品选择市场今年注册.教育项目资料因为本站.\n包括密码地区责任查看世界.研究要求不断投资重要.建设当然推荐然后男人.这些汽车国家可以.\n企业部分是一处理这是这样各种.结果只有没有目前工程.要求精华推荐数据方式.\n安全上海国际所以需要.大小有些加入当前下载自己今天包括.今年免费城市这样.'], ['安楠', '52032520040830705X', '13483945655', 'xiulanwang@example.com', '湖北省银川县清河天津街p座 622498', '738804', '开发区世创信息有限公司', 'https://weiqin.cn/', '8.157.64.131', {'176.963852': '-3.9908155'}, '操作经营用户游戏很多可能来源帮助.组织文章图片详细.\n生产一点记者方面程序活动.也是说明其他行业.虽然报告这样结果全部.\n继续操作方式音乐重要由于如果.\n专业人员简介市场.学习能力责任一下能够.具有广告报告可是科技如何比较文化.不要全部注册内容.\n因为等级他的中心政府有限作品拥有.法律产品成功.一般以下价格制作更新论坛软件.'], ['张楠', '150202199301163821', '13130298100', 'jingzhou@example.net', '澳门特别行政区张家港县普陀杜街H座 935373', '387859', '毕博诚信息有限公司', 'https://chenhou.cn/', '189.105.169.186', {'2.537883': '-28.7122655'}, '根据然后应该通过安全.国家结果经济主题论坛.关系最新今天点击全部名称其他.\n其中虽然方面系列能力.其中帮助个人阅读但是中心.留言合作情况密码游戏.标题阅读人民商品.\n活动解决一样.非常内容操作.\n专业这种首页简介.更新方法觉得其他.项目研究自己电话的是.\n自己为了准备文件重要.留言阅读所以自己不能质量结果.主要电话同时单位注册搜索继续.经济成为一点这样发表投资直接.']]


    print("13，生成10条测试数据并写入数据库test55".center(100, "-"))
    list1 = Fake_PO.genTest(['genName', 'genSsn', 'genPhone_number', 'genEmail', 'genAddress', 'genPostcode', 'genCompany', 'genUrl', 'genIpv4', 'genText'], 10)
    Pandas_PO = PandasPO("192.168.0.234", "root", "Zy123456", "mcis", 3306)
    Pandas_PO.list2db(list1, "test55", "")
    # 字段改名
    Pandas_PO.execute("alter table test55 change `index` id int(100), change `0` `name` varchar(30) ,change `1` ssn char(30), change `2` phone_number char(30), change `3` genEmail varchar(30),"
                      " change `4` genAddress varchar(50), change `5` genPostcode char(30), change `6` genCompany varchar(30), change `7` genUrl char(50), "
                      "change `8` genIpv4 char(30),change `9` genText text(330)")
    # 设置id主键
    Pandas_PO.execute("alter table test55 add primary key(id)")