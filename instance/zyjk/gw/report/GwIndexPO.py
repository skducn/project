# coding=utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author :John
# Created on : 2024-7-30
# Description: gw报表包
# 在线国密SM2加密/解密 https://the-x.cn/zh-cn/cryptography/Sm2.aspx

# 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
# 密钥：124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62
# 公钥：04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249
# privateKey = 00c68ee01f14a927dbe7f106ae63608bdb5d2355f18735f7bf1aa9f2e609672681
# publicKey = 047e2c1440d05e86f9677f710ddfd125aaea7f3a390ce0662f9ef9f5ff1fa860d5174251dfa99e922e224a51519a53cd71063d81e64345a0c352c4eb68d88b0cc9

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import random
import subprocess
import pyperclip as pc
# 1、复制内容到剪贴板
# 2、粘贴剪贴板里的内容

from PO.WebPO import *

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')

from PO.SqlserverPO import *
Sqlserver_PO = SqlServerPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database"))  # 测试环境
Sqlserver_PO1 = SqlServerPO(Configparser_PO.DB("host"), Configparser_PO.DB("user"), Configparser_PO.DB("password"), Configparser_PO.DB("database1"))  # 测试环境
# SqlServerPO = SqlServerPO(Configparser_PO.DB_DM("host"), Configparser_PO.DB_DM("user"), Configparser_PO.DB_DM("password"), Configparser_PO.DB_DM("port"))  # 测试环境

from PO.StrPO import *
Str_PO = StrPO()

from PO.ColorPO import *
Color_PO = ColorPO()

from PO.TimePO import *
Time_PO = TimePO()

from PO.ListPO import *
List_PO = ListPO()

from PO.DictPO import *
Dict_PO = DictPO()

from PO.DataPO import *
Data_PO = DataPO()

from PO.CharPO import *
Char_PO = CharPO()



class GwIndexPO():

    def __init__(self, sheetName=''):

        self.ipAddr = Configparser_PO.HTTP("url")

        # self.TOKEN = self.getToken(Configparser_PO.USER("user"), Configparser_PO.USER("password"))
        self.dbTable = Char_PO.chinese2pinyin(sheetName)
        self.dbTable = "a_" + self.dbTable
        self.sheetName = sheetName
        # print(self.sheetName)

        # # 读取测试对应的表(a_7jingshenzhangai)
        # self.csgz = "a_" + Char_PO.chinese2pinyin(Configparser_PO.FILE("csgz"))
        # print(self.csgz)


    def createTable(self, sheetName):

        # 中文转拼音
        dbTable = Char_PO.chinese2pinyin(sheetName)
        dbTable = "a_" + dbTable
        # print(dbTable)


        Sqlserver_PO.execute("drop table if exists " + dbTable)
        # if dbTable == 'a_temporaryTable':
        #     Sqlserver_PO.crtTable('a_temporaryTable', '''id INT IDENTITY(1,1) PRIMARY KEY, key1 VARCHAR(500), value1 VARCHAR(500)''')
        # else:
        # excel导入db
        Sqlserver_PO.xlsx2db(Configparser_PO.FILE("case"), dbTable, sheetName)

        Sqlserver_PO.execute("ALTER table %s alter column result varchar(10)" % (dbTable))  # 此列没数据，创建后是float，需转换成char
        # Sqlserver_PO.execute("ALTER TABLE %s alter column id int not null" % (dbTable))  # 设置主id不能为Null
        # Sqlserver_PO.execute("ALTER TABLE %s add PRIMARY KEY (id)" % (dbTable))  # 设置主键（条件是id不能为Null）
        Sqlserver_PO.execute("ALTER table %s alter column datetime char(11)" % (dbTable))  # 将float改为char类型
        Sqlserver_PO.execute("ALTER table %s alter column datetime DATE" % (dbTable))  # 注意sqlserver无法将float改为date，先将float改为char，再将char改为data，
        # Sqlserver_PO.execute("ALTER TABLE %s ADD id1 INT NOT NULL IDENTITY(1,1) primary key (id1) " % ('健康评估'))  # 新增id自增主键
        # Sqlserver_PO.execute("ALTER TABLE %s ADD var varchar(111)" % (tableName))  # 临时变量
        # 添加表注释
        Sqlserver_PO.execute("EXECUTE sp_addextendedproperty N'MS_Description', N'%s', N'user', N'dbo', N'table', N'%s', NULL, NULL" % (sheetName + '(报表用例)', dbTable))  # sheetName=注释，dbTable=表名
        print("[ok] 表'%s(%s)'创建成功! " % (dbTable, sheetName))


    def initDiseaseIdcard(self, varIdcard):

        # 初始化单个疾病身份证

        l_d_param = Sqlserver_PO.select("select diseaseRuleCode, diseaseName, sql1,sql2,sql3,sql4,sql5,sql6 from %s where [idcard]='%s'" % (self.jbsfz, str(varIdcard)))
        # print(l_d_param)

        # # 删除基本信息表
        Sqlserver_PO.execute("delete from HRPERSONBASICINFO where ARCHIVENUM = '%s'" % (varIdcard))
        # 插入基本信息表
        Sqlserver_PO.execute('set identity_insert HRPERSONBASICINFO on')
        r = Sqlserver_PO.select('select max(ID) as qty from HRPERSONBASICINFO')
        a = r[0]['qty'] + 1
        Sqlserver_PO.execute("insert into HRPERSONBASICINFO(ARCHIVENUM,NAME,sex,IDCARD,CREATETIME,ID,ISGOVERNANCE) values ('%s', '%s', '1', '%s','%s', %s, '0')" % (varIdcard, Data_PO.getChineseName(), varIdcard, time.strftime("%Y-%m-%d %H:%M:%S.000"), str(a)))
        Sqlserver_PO.execute('set identity_insert HRPERSONBASICINFO off')


        # # 删除签约信息表
        Sqlserver_PO.execute("delete from QYYH where SFZH = '%s'" % (varIdcard))
        # 插入签约信息表
        Sqlserver_PO.execute('set identity_insert QYYH on')
        r = Sqlserver_PO.select('select max(ID) as qty from QYYH')
        a = r[0]['qty'] + 1
        Sqlserver_PO.execute("insert into QYYH(CZRYBM, CZRYXM, JMXM, SJHM, SFZH, JJDZ, ARCHIVEUNITCODE, ARCHIVEUNITNAME, DISTRICTORGCODE, DISTRICTORGNAME, TERTIARYORGCODE, TERTIARYORGNAME, SIGNSTATUS, SIGNDATE, ID, CATEGORY_CODE, CATEGORY_NAME, SEX_CODE, SEX_NAME) values ('%s', '%s','%s', '13817261777', '%s', '上海浦东100号', '0000001', '彭浦新村街道社区健康管理中心', '310118000000', '青浦区', '12345', '上海人民医院', 1, '2020-03-23', %s, '4', N'老年人', '2', N'女')" % (l_d_param[0]['diseaseRuleCode'], l_d_param[0]['diseaseName'], Data_PO.getChineseName(), varIdcard, a))
        Sqlserver_PO.execute('set identity_insert QYYH off')

        # 删除患者主索引表
        Sqlserver_PO.execute("delete from TB_EMPI_INDEX_ROOT where IDCARDNO = '%s'" % (varIdcard))
        # 插入患者主索引表
        Sqlserver_PO.execute("insert into TB_EMPI_INDEX_ROOT(GUID, NAME, IDCARDNO) values('%s', '%s', '%s')" % (l_d_param[0]['diseaseRuleCode'], Data_PO.getChineseName(), varIdcard))

        print("[OK] ", varIdcard)

    def getToken(self, varUser, varPass):

        # 获取登录用户的token

        command = "curl -X POST \"" + Configparser_PO.HTTP("url") + ":8012/login\" -H \"accept: */*\" -H \"Content-Type: application/json\" -d \"{ \\\"password\\\": \\\"" + str(varPass) + "\\\", \\\"username\\\": \\\"" + str(varUser) + "\\\"}\""
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        if Configparser_PO.SWITCH("token") == "on":
            print(d_r['data']['access_token'])
        return d_r['data']['access_token']

    def curl(self, varMethod, varUrl):

        # 跑接口
        # r = gw_i_PO.curl('GET', "/server/tEhrInfo/getEhrHomeInfo?0=47c8d0444e60f4ee4348b3611c62e6aa071e81981f40195294d3424177bb400732c3ce5e782259d9302a642fbc9723a20aec65bf6d7a138933a52da1dd0aa67bcf7c48b51f712248988be78445dbddc1e9c2449e4d93b64b1b4a3f26ed748ac44ccf5c871807de69e8268f986c6e")

        command = "curl -X " + varMethod + ' "' + self.ipAddr + varUrl + '" ' + '-H "Request-Origion:SwaggerBootstrapUi" -H "accept:*/*" -H "Content-Type:application/json" -H "Authorization:' + self.token + '"'
        # print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        # print(d_r)  # {'code': 200, 'msg': None, 'data': {'manageEhrNum': 100, 。。。
        try:
            if d_r['code'] == 200:
                return d_r
        except:
            # {'code': 500, 'msg': '非法参数！'}
            d_r = 500
        return d_r

    def curlLogin(self, encrypt_data):

        # 登录
        # 注意需要关闭验证码

        command = "curl -X POST '" + self.ipAddr + "/auth/login' -d '" + encrypt_data + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Authorization:' -H 'Content-Type:application/json'"
        # print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        # print(d_r)  # {'code': 200, 'msg': None, 'data': {'access_token': 'eyJhbGciOiJIUzUxMiJ9.eyJhZmZpbGlhdGVkX2lkIjoiIiwidXNlcl9pZCI6ODIsImNhdGVnb3J5X2NvZGUiOiIxIiwidXNlcl9rZXkiOiIwYzU3YmM3OC05OTNiLTQ1M2ItYjZkMC0yMmNlZTBhMWFkNzMiLCJ0aGlyZF9ubyI6IjEyMzEyMyIsImhvc3BpdGFsX2lkIjoiMDAwMDAwMSIsInVzZXJuYW1lIjoi5YiY5paM6b6ZIiwiaG9zcGl0YWxfbmFtZSI6IumdmeWuieeyvuelnueXhemZoiIsImFmZmlsaWF0ZWRfbmFtZSI6IiJ9.-xh2D7Obdensd3OcL_dqRaA7Qs4I0l0h--3ZYpYifgBZBP16Gzzq24W3IxS8c5ofcQTNyczRK2e3JipcCuyTqg', 'expires_in': 30}}
        try:
            # {'code': 200, 'msg': None, 'data': {'access_token': 'eyJhbGciOiJIUzUxMiJ9.eyJhZmZpbGlhdGVkX2lkIjoiIiwidXNlcl9pZCI6ODIsImNhdGVnb3J5X2NvZGUiOiIxIiwidXNlcl9rZXkiOiIwYzU3YmM3OC05OTNiLTQ1M2ItYjZkMC0yMmNlZTBhMWFkNzMiLCJ0aGlyZF9ubyI6IjEyMzEyMyIsImhvc3BpdGFsX2lkIjoiMDAwMDAwMSIsInVzZXJuYW1lIjoi5YiY5paM6b6ZIiwiaG9zcGl0YWxfbmFtZSI6IumdmeWuieeyvuelnueXhemZoiIsImFmZmlsaWF0ZWRfbmFtZSI6IiJ9.-xh2D7Obdensd3OcL_dqRaA7Qs4I0l0h--3ZYpYifgBZBP16Gzzq24W3IxS8c5ofcQTNyczRK2e3JipcCuyTqg', 'expires_in': 30}}
            self.token = d_r['data']['access_token']
        except:
            # {'code': 500, 'msg': '非法参数！'}
            self.token = d_r['code']

        # Color_PO.outColor([{"35": "token =>"}, {"35": self.token}])
        # print("token =>", self.token)

    def _sm2(self, Web_PO):

        # 在线sm2加密/解密

        Web_PO.openURL("https://config.net.cn/tools/sm2.html")
        # 私钥
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[1]/textarea[1]", Configparser_PO.HTTP("privateKey"))
        # 公钥
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[1]/textarea[2]", Configparser_PO.HTTP("publicKey"))

    def encrypt(self, varSource):

        # 在线sm2加密

        Web_PO = WebPO("noChrome")
        self._sm2(Web_PO)
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[2]/textarea[1]", varSource)
        Web_PO.clkByX("/html/body/div[2]/div/div[1]/div[2]/div[1]/a[1]", 1)
        r = Web_PO.getAttrValueByX("/html/body/div[2]/div/div[1]/div[2]/textarea[2]", "value")
        Web_PO.cls()
        return r

    def decrypt(self, varEncrypt):

        # 在线sm2解密

        Web_PO = WebPO("noChrome")
        self._sm2(Web_PO)
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[2]/textarea[2]", varEncrypt)
        Web_PO.clkByX("/html/body/div[2]/div/div[1]/div[2]/div[2]/a[1]", 1)
        r = Web_PO.getAttrValueByX("/html/body/div[2]/div/div[1]/div[2]/textarea[1]", "value")
        Web_PO.cls()
        return r


    # def dysphrenia(self, varSql):
    #
    #     # 精神障碍健康管理报表
    #     r = self.curl(l[0], l[1] + self.encrypt(str(l[2])))
    #     print(r)  # {'code': 200, 'msg': None, 'data': {'manageEhrNum': 8, 'familyEhrNum': 8,
    #     for i in range(len(r['data'])):
    #         if r['data'][i]['orgName'] == l[3]['orgName']:
    #             print(r['data'][i]['registered'])

    def runParam(self, d_content):

        # 执行sql

        print("param =>", d_content)  # {'login': {'username': 'ej', 'password': '12345678'}, 'param': {'year': '2024', 'orgCode': '370685009'}, 'method': 'GET', 'path': '/serverExport/report/getSmiBi?0=', 'res': 'registered'}

        d_temp = {}

        # # # 精神障碍健康管理报表
        # 获取三级机构卫生室的registered合计
        param = self.encrypt(str(d_content['param']))
        param = d_content['path'] + param
        r = self.curl(d_content['method'], param)
        print("res =>", r)  # {'code': 200, 'msg': None, 'data': [{'orgName': '招远市齐山镇北寨子村卫生室', 'orgCode': '370685009014', 'registered': 0, 'standardizedManagement': 0,...

        orgDownCount = 0
        for i in range(len(r['data'])):
            # 下级机构（如：招远市齐山镇北寨子村卫生室）
            if r['data'][i]['orgCode'] != d_content['param']['orgCode']:
                len_orgCode = len(r['data'][i]['orgCode'])
                orgDownCount = orgDownCount + r['data'][i][d_content['res']]
            # 上级机构（道头卫生院）
            if r['data'][i]['orgCode'] == d_content['param']['orgCode']:
                orgUp = r['data'][i][d_content['res']]
                len_orgCode = len(r['data'][i]['orgCode'])

        if len_orgCode == 12:
            # 三级机构
            print("三级机构之和 = " + str(orgDownCount))
            print("二级机构 = " + str(orgUp))
            orgDownCount = orgDownCount + 1
            if orgDownCount == orgUp:
                Color_PO.outColor([{"36": '[ok]，三级机构之和+1等于二级机构'}])
                return "ok"
            else:
                Color_PO.outColor([{"31": '[error]，三级机构之和+1不等于二级机构'}])
                return "error"
        elif len_orgCode == 9:
            # 二级机构
            print("三级机构之和 = " + str(orgDownCount))
            print("二级机构 = " + str(orgUp))
            orgDownCount = orgDownCount + 1
            if orgDownCount == orgUp:
                Color_PO.outColor([{"36": '[ok]，三级机构之和+1等于二级机构'}])
                return "ok"
            else:
                Color_PO.outColor([{"31": '[error]，三级机构之和+1不等于二级机构'}])
                return "error"
        elif len_orgCode == 6:
            print("二级机构之和 = " + str(orgDownCount))
            print("一级机构 = " + str(orgUp))
            if orgDownCount == orgUp:
                Color_PO.outColor([{"36": '[ok]，二级机构之和等于一级机构'}])
                return "ok"
            else:
                Color_PO.outColor([{"31": '[error]，二级机构之和不等于一级机构'}])
                return "error"

    def runSql(self, varSql, varContent):

        # 执行sql
        # DELETE from T_EHR_INFO where IDCARD ='370827198908215970';

        varPrefix = varContent.split(" ")[0]
        varPrefix = varPrefix.lower()
        if varPrefix == 'select':
            print(varSql, varContent)
            command = 'Sqlserver_PO.select("' + varContent + '")'
            a = eval(command)
            # sleep(1)
            # 将临时变量存入db
            for k, v in a[0].items():
                Sqlserver_PO.execute("insert into %s (key1,value1) values ('%s', '%s')" % (self.tmp_db, str(k), str(v)))

        elif varPrefix == 'update' or varPrefix == 'insert' or varPrefix == 'delete' :
            # 将db转换成字典
            l = Sqlserver_PO.select("select key1, value1 from %s" % (self.tmp_db))
            if l != []:
                # 输出临时变量
                Color_PO.outColor([{"35": self.tmp_db}, {"35": "=>"}, {"35": l}])
                # print(l) # [{'key1': 'ID', 'value1': '499948'}, {'key1': 'QTY', 'value1': '1'}, {'key1': 'Q2', 'value1': '1'},

            d_update = {}
            for p in range(len(l)):
                d_update[l[p]['key1']] = l[p]['value1']
            # 这里加入变量替换语句
            if 'id' in d_update:
                varContent = str(varContent).replace("{id}", str(d_update['id']))

            print(varSql, varContent)
            command = 'Sqlserver_PO.execute("' + varContent + '")'
            a = eval(command)
            sleep(1)
            # return a
        else:
            sys.exit(0)


    def verifyIdcard(self, varIdcard):

        # 检查患者主索引表身份证是否存在!
        l_d_qty = Sqlserver_PO.select("select count(*) as qty from TB_EMPI_INDEX_ROOT where IDCARDNO='%s'" % (varIdcard))
        # print(l_d_qty)  # [{'qty': 1}]
        if l_d_qty[0]['qty'] == 0:
            guid = Data_PO.getFigures(6)
            name = Data_PO.getChineseName()
            Sqlserver_PO.execute("INSERT INTO [TB_EMPI_INDEX_ROOT] ([GUID], [NAME], [SEXCODE], [SEXVALUE], [DATEOFBIRTH], [IDCARDNO]) VALUES ('" + str(guid) + "', N'" + str(name) + "', '2', '女', '1940-05-11', '" + str(varIdcard) + "')")

        # 检查基本信息表身份证是否存在!
        l_d_qty = Sqlserver_PO.select("select count(*) as qty from HRPERSONBASICINFO where IDCARD='%s'" % (varIdcard))
        if l_d_qty[0]['qty'] == 0:
            Sqlserver_PO.execute("INSERT INTO [dbo].[HRPERSONBASICINFO] ([ARCHIVENUM], [NAME], [SEX], [DATEOFBIRTH], [IDCARD], [WORKUNIT], [PHONE], [CONTACTSNAME], [CONTACTSPHONE], [RESIDENCETYPE], [NATIONCODE], [BLOODTYPE], [RHBLOODTYPE], [DEGREE], [OCCUPATION], [MARITALSTATUS], [HEREDITYHISTORYFLAG], [HEREDITYHISTORYCODE], [ENVIRONMENTKITCHENAERATION], [ENVIRONMENTFUELTYPE], [ENVIRONMENTWATER], [ENVIRONMENTTOILET], [ENVIRONMENTCORRAL], [DATASOURCES], [CREATEID], [CREATENAME], [CREATETIME], [UPDATEID], [UPDATENAME], [UPDATETIME], [STATUS], [ISDELETED], [VERSION], [WORKSTATUS], [TELEPHONE], [OCCUPATIONALDISEASESFLAG], [OCCUPATIONALDISEASESWORKTYPE], [OCCUPATIONALDISEASESWORKINGYEARS], [DUSTNAME], [DUSTFLAG], [RADIOACTIVEMATERIALNAME], [RADIOACTIVEMATERIALFLAG], [CHEMICALMATERIALNAME], [CHEMICALMATERIALFLAG], [OTHERNAME], [OTHERFLAG], [PHYSICSMATERIALNAME], [PHYSICSMATERIALFLAG], [DOWNLOADSTATUS], [NONUMBERPROVIDED], [YLZFMC], [PERSONID], [MEDICAL_PAYMENTCODE], [KALEIDOSCOPE], [ISGOVERNANCE]) VALUES ('" + str(varIdcard) + "', '高血压已患', '2', '1959-03-28 00:00:00.000', '" + str(varIdcard) + "', NULL, '13585543856', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2022-11-14 16:49:32.357', NULL, NULL, '2020-02-19 00:00:00.000', NULL, NULL, NULL, NULL, '13585543856', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,'0')")

        # 检查签约信息表身份证是否存在!
        l_d_qty = Sqlserver_PO.select("select count(*) as qty from QYYH where SFZH='%s'" % (varIdcard))
        if l_d_qty[0]['qty'] == 0:
            guid = Data_PO.getFigures(6)
            Sqlserver_PO.execute("INSERT INTO [dbo].[QYYH] ([CZRYBM], [CZRYXM], [JMXM], [SJHM], [SFZH], [JJDZ], [SFJD], [SIGNORGID], [ARCHIVEUNITCODE], [ARCHIVEUNITNAME], [DISTRICTORGCODE], [DISTRICTORGNAME], [TERTIARYORGCODE], [TERTIARYORGNAME], [PRESENTADDRDIVISIONCODE], [PRESENTADDRPROVCODE], [PRESENTADDRPROVVALUE], [PRESENTADDRCITYCODE], [PRESENTADDRCITYVALUE], [PRESENTADDRDISTCODE], [PRESENTADDDISTVALUE], [PRESENTADDRTOWNSHIPCODE], [PRESENTADDRTOWNSHIPVALUE], [PRESENTADDRNEIGHBORHOODCODE], [PRESENTADDRNEIGHBORHOODVALUE], [SIGNSTATUS], [SIGNDATE],[CATEGORY_CODE], [CATEGORY_NAME], [SEX_CODE], [SEX_NAME], [LAST_SERVICE_DATE], [ASSISTANT_DOC_ID], [ASSISTANT_DOC_NAME], [HEALTH_MANAGER_ID], [HEALTH_MANAGER_NAME], [ASSISTANT_DOC_PHONE], [HEALTH_MANAGER_PHONE]) VALUES ('" + str(guid) + "', N'姚皎情', N'肝癌高危', NULL, '" + str(varIdcard) + "', N'平安街道16号', NULL, NULL, '0000001', '静安精神病院', '310118000000', '青浦区', '12345', '上海人民医院', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, '2020-06-01', 166, '4', N'1',N'男', NULL, NULL, NULL, NULL, NULL, NULL, NULL)")


    def run(self, d_index_type):

        # 执行场景

        print((self.sheetName).center(100, "-"))

        if isinstance(int(d_index_type['index']), int):
            ...
        else:
            print(12121212)
            sys.exit(0)

        # 3, 获取并执行sql语句
        l_d = Sqlserver_PO.select("select content from %s where [index]='%s' and type='%s' and sql='param'" % (self.dbTable, d_index_type['index'], d_index_type['type']))
        # print("param =>", l_d)  # [{'content': '{"login":{"username":"ej", "password":"12345678"},
        # print(l_d[0]['content'])  # {"login":{"username":"ej", "password":"12345678"},
        d_content = json.loads(l_d[0]['content'])
        # print(d['login'])  # {'username': 'ej', 'password': '12345678'}

        # 1，登录
        self.curlLogin(self.encrypt(json.dumps(d_content['login'])))

        if os.name == "posix":
            r = self.runParam(d_content)
            if r == "ok":
                Sqlserver_PO.execute("update %s set result='ok' where [index]=%s and type='%s' and sql='param'" % (
                self.dbTable, d_index_type['index'], d_index_type['type']))
            elif r == "error":
                Sqlserver_PO.execute("update %s set result='error' where [index]=%s and type='%s' and sql='param'" % (
                self.dbTable, d_index_type['index'], d_index_type['type']))
            Sqlserver_PO.execute("update %s set datetime='%s' where [index]=%s and type='%s' and sql='param'" % (
            self.dbTable, Time_PO.getDateTimeByDivide(), d_index_type['index'], d_index_type['type']))
        else:
            r = self.runSql(d_content.encode('latin1').decode('GB2312'))
            # 未写

    def gen(self, d_index_type):


        # l_d = Sqlserver_PO.execute("INSERT INTO [dbo].[T_EHR_INFO]([IDCARD], [EHR_NUM], [NAME], [SEX_CODE], [SEX_NAME], [BIRTH], [NATION_CODE], [NATION_NAME],  [PRESENT_PROVINCE_CODE], [PRESENT_PROVINCE_NAME], [PRESENT_CITY_CODE], [PRESENT_CITY_NAME], [PRESENT_DISTRICT_CODE], [PRESENT_DISTRICT_NAME], [PRESENT_TWON_CODE], [PRESENT_TWON_NAME], [PRESENT_VILLAGE_CODE], [PRESENT_VILLAGE_NAME], [PRESENT_ADDRESS], [PHONE], [CONTACTS_NAME], [CONTACTS_PHONE], [RESIDENCE_CODE], [RESIDENCE_NAME], [DEGREE_CODE], [DEGREE_NAME], [OCCUPATION_CODE], [OCCUPATION_NAME], [WORK_UNIT], [MARRIAGE_CODE], [MARRIAGE_NAME], [BLOOD_TYPE_CODE], [BLOOD_TYPE_NAME], [RH_BLOOD_TYPE_CODE], [RH_BLOOD_TYPE_NAME], [DISEASE_FLAG], [OPERATION_FLAG], [TRAUMA_FLAG], [TRANSFUSION_FLAG], [GENETIC_FLAG], [GENETIC_NAME], [HOST_RELATION_CODE], [HOST_RELATION_NAME], [HOST_NAME], [HOST_IDCARD], [FAMILY_NUMBER], [FAMILY_STRUCTURE], [LIVING_CONDITION_CODE], [LIVING_CONDITION_NAME], [EXHAUST_CODE], [EXHAUST_NAME], [FUEL_CODE], [FUEL_NAME], [WATER_CODE], [WATER_NAME], [TOILET_CODE], [TOILET_NAME], [LIVESTOCK_CODE], [LIVESTOCK_NAME], [CREATE_ORG_CODE], [CREATE_ORG_NAME], [CREATE_SUB_ORG_CODE], [CREATE_SUB_ORG_NAME], [MANAGE_ORG_CODE], [MANAGE_ORG_NAME], [MANAGE_SUB_ORG_CODE], [MANAGE_SUB_ORG_NAME], [CREATOR_ID], [CREATOR_NAME], [RESPONSIBLE_DOC_ID], [RESPONSIBLE_DOC_NAME], [CREATE_DATE], [IS_DELETE], [DELETE_REASON], [FINAL_STATUS], [FINAL_DATE], [OTHER_ALLERGY], [OTHER_PAYMENT], [OTHER_EXPOSURE], [EMPLOYEE_INSURANCE_CARD], [RESIDENT_INSURANCE_CARD], [POVERTY_RELIEF_CARD], [IS_SIGN], [IS_HIGH_RISK], [IS_EXAM], [EXAM_DATE], [IS_UPDATE], [UPDATE_DATE], [TEAM_ID], [EXHAUST_OTHER_NAME], [FUEL_OTHER_NAME], [WATER_OTHER_NAME], [TOILET_OTHER_NAME], [OTHER_DISABILITY], [HZLXBM], [HZLXMC], [UNMANAGED_REASON_CODE], [UNMANAGED_REASON_NAME], [FINAL_DOC_ID], [FINAL_DOC_NAME]) VALUES ( N'310101198004110014', N'310101198004110014', N'hh1', '1', '男', '1989-08-21', '01', '汉族', '37', '山东省', '370600000000', '烟台市', '370685000000', '招远市', N'370685001000', '罗峰街道', '370685001001', '文化区社区居民委员会', '测试', '1332233222', '测试', '1332233222', '1', '户籍', '10', '研究生教育', '10000', '国家机关、党群组织、企业、事业单位负责人', '1', '10', '未婚', '1', 'A型', '3', 'Rh阳性', N'0', '0', '0', '0', '0', '', '02', '户主', '精神障碍', '370827198908215970', 1, '1', '', '', '1', '油烟机', '2', '煤', '1', '自来水', '1', '卫生厕所', '1', '无', N'370685009001', '雀头孙家村卫生室', '370685009001', '雀头孙家村卫生室', N'370685009001', '雀头孙家村卫生室', '', '', 10118, '三级普通用户', -1, '', '2024-07-26', 0, '', 0, '1900-01-01', '', '', '', '', '', '', '0', '0', '0', '1900-01-01', '0', '1900-01-01', -1, '', '', '', '', N'', '0', '本地人员', '', '', -1, N'');")
        # sys.exit(0)

        # 生成测试数据

        if isinstance(int(d_index_type['index']), int):
            ...
        else:
            print(12121212)
            sys.exit(0)

        # 2, 生成动态临时数据库
        self.tmp_db = 'a_temp' + str(Data_PO.getFigures(10))
        Sqlserver_PO.crtTable(self.tmp_db, '''id INT IDENTITY(1,1) PRIMARY KEY, key1 VARCHAR(500), value1 VARCHAR(500)''')
        # print("new =>", self.tmp_db)  # new => a_temp3945770091
        Color_PO.outColor([{"35": "new =>"}, {"35": self.tmp_db}])

        # 3, 获取并执行sql语句
        l_d = Sqlserver_PO.select("select sql,content from %s where [index]='%s' and type='%s' and sql<>'param'" % (self.dbTable, d_index_type['index'], d_index_type['type']))
        # print("sql =>", l_d)  # sql => [{'content': "DELETE from T_EHR_INFO where IDCARD ='370827198908215970';"}, {'content': "DELETE fr...

        # 数据源
        # 随机身份证
        idCard = Data_PO.getIdCard()
        # print(idCard)  # 441427196909022802
        # 随机获取 道头卫生院下的三级卫生院 code和name
        l_tmp = Sqlserver_PO.select("select org_sub_code, org_sub_name from ZYCONFIG.dbo.SYS_SUB_HOSPITAL where org_code='370685009' ")
        # print(l_tmp)  # [{"org_sub_code": "370685009001", "org_sub_name": "雀头孙家村卫生室"}, {"org_sub_code": "370685009002", "org_sub_name": "招远市齐山镇北寨子村卫生室"}]

        if 'org_code' in d_index_type:
            for i in range(len(l_tmp)):
                if l_tmp[i]['org_sub_code'] == d_index_type['org_code']:
                    org3_name = l_tmp[i]['org_sub_name']
                    org3_code = l_tmp[i]['org_sub_code']
                    break
        else:
            # 随机获取三级机构名和编码
            org3 = random.choice(l_tmp)
            org3_name = org3['org_sub_name']
            org3_code = org3['org_sub_code']

        # print(org3)
        Color_PO.outColor([{"35": 'param =>'}, {"35": org3_name}, {"35": org3_code}, {"35": idCard}])
        # 招远市齐山镇北寨子村卫生室 370685009014 310101199609298755

        for i in range(len(l_d)):
            varContent = l_d[i]['content']
            varContent = varContent.replace("{name}", Data_PO.getChineseName())
            varContent = varContent.replace("{idCard}", idCard)
            varContent = varContent.replace("{org_sub_code}", org3_code)
            varContent = varContent.replace("{org_sub_name}", org3_name)

            if os.name == "posix":
                r = self.runSql(l_d[i]['sql'], varContent)
            else:
                r = self.runSql(l_d[i]['sql'].encode('latin1').decode('GB2312'), varContent.encode('latin1').decode('GB2312'))
                # 未写

        Sqlserver_PO.execute("drop table %s" % (self.tmp_db))
        # print("drop => ", self.tmp_db)
        Color_PO.outColor([{"35": "drop =>"}, {"35": self.tmp_db}])
        print("\n")





    def runId(self, l_dbId):

        # 按id执行

        if isinstance(l_dbId, list):
            for i in range(len(l_dbId)):
                self.run(l_dbId[i])

    def runIdArea(self, l_dbId):

        # 按id区间执行

        if isinstance(l_dbId, list):
            if len(l_dbId) == 2:
                for i in range(l_dbId[0], l_dbId[1]):
                    self.run(i)

    def runRule(self, l_dbRule):

        # 按rule规则执行

        if len(l_dbRule) == 1:
            l_dbRule.append('')
        elif len(l_dbRule) > 1:
            ...
        else:
            sys.exit(0)

        t_dbRule = tuple(l_dbRule)
        print(t_dbRule)
        sys.exit(0)
        l_d_id = Sqlserver_PO.select("select id from %s where [rule] in %s" % (self.dbTable, t_dbRule))
        print(l_d_id)  # [{'id': 2}, {'id': 3}]
        for i in range(len(l_d_id)):
            self.run(l_d_id[i]['id'])

    def runResult(self, varResult):

        # 按result执行
        # r.runResult("error")  # 执行result为error的规则
        # r.runResult("all")  # 执行所有的规则(谨慎)

        if varResult == "all":
            l_d_id = Sqlserver_PO.select("select id from %s" % (self.dbTable))
            for i in range(len(l_d_id)):
                self.run(l_d_id[i]['id'])
        elif varResult != "ok":
            l_d_id = Sqlserver_PO.select("select id from %s where result <> 'ok'" % (self.dbTable))
            for i in range(len(l_d_id)):
                self.run(l_d_id[i]['id'])

    def runDate(self, varDate=''):

        # 按照时间执行
        # 如果updateDate不是2024-07-19，就执行
        # r.runDate("2024-07-19")

        if  varDate == '':
            varDate = Time_PO.getDateByMinus()
        l = Sqlserver_PO.select("select id, updateDate from %s" % (self.dbTable))
        for i in range(len(l)):
            if str(varDate) != str(l[i]['updateDate']):
                self.run(l[i]['id'])

    def runDateAgo(self, varN):

        # 执行N天以前的规则
        beforeDate = Time_PO.getDateByMinusPeriod(varN)
        # print(beforeDate)  # 2024-07-16
        l = Sqlserver_PO.select("select id, updateDate from %s" % (self.dbTable))
        for i in range(len(l)):
            if beforeDate > l[i]['updateDate']:
                self.run(l[i]['id'])

    def runDateAgoResult(self, varN, varResult):

        # r.runDateAgoResult(-3, 'error')
        # 执行几天以前且状态是error的规则
        beforeDate = Time_PO.getDateByMinusPeriod(varN)
        # print(beforeDate)  # 2024-07-16
        l = Sqlserver_PO.select("select id, result, updateDate from %s" % (self.dbTable))
        for i in range(len(l)):
            if beforeDate > l[i]['updateDate'] and varResult == l[i]['result']:
                self.run(l[i]['id'])




    def getSql(self):
        
        # 获取sql语句

        # todo 输出第一行
        if self.tester == self.successor:
            print(str(self.sheetName) + " => " + str(self.dbId) + "(" + self.rule + ")" + " => " + self.tester)  # [健康评估 => 9(r1)]
        else:
            print(str(self.sheetName) + " => " + str(self.dbId) + "(" + self.rule + ")" + " => " + self.tester + " => " + self.successor )
        # Color_PO.consoleColor("31", "33", (("[" + str(self.dbTable) + " => " + str(self.dbId) + "(" + rule + ")]").center(100, '-')), "")

        l_0 = Sqlserver_PO.select("select sql from %s where [rule]='%s'" %(self.csgz, self.rule))
        l_sql = []
        for i in range(len(l_0)):
            if os.name == "posix":
                l_sql.append(l_0[i]['sql'])
            else:
                l_sql.append(l_0[i]['sql'].encode('latin1').decode('GB2312'))
        return l_sql


    def param4_auto(self):
        d = {}
        d['l_sql'] = self.getSql()
        l_ruleParam = Str_PO.str2list(self.ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleParam3'] = l_ruleParam[2].replace(".and.", ',')
        d['ruleParam4'] = l_ruleParam[3].replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        self._getAutoIdcard(d)

    def param1_auto(self):
        d = {}
        d['l_sql'] = self.getSql()
        d['ruleParam'] = self.ruleParam.replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        self._getAutoIdcard(d)

    def param1_idcard(self):
        d = {}
        d['l_sql'] = self.getSql()
        d['ruleParam'] = self.ruleParam.replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        d['diseaseRuleCode'] = self.diseaseRuleCode
        self._getDiseaseIdcard2(d)

    def param2_auto(self):
        d = {}
        d['l_sql'] = self.getSql()
        l_ruleParam = Str_PO.str2list(self.ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        self._getAutoIdcard(d)

    def param2_idcard(self):
        d = {}
        d['l_sql'] = self.getSql()
        l_ruleParam = Str_PO.str2list(self.ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        d['diseaseRuleCode'] = self.diseaseRuleCode
        self._getDiseaseIdcard2(d)

    def param1_idcard_hitQty2(self):
        d = {}
        d['l_sql'] = self.getSql()
        d['ruleParam'] = self.ruleParam.replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        d['diseaseRuleCode'] = self.diseaseRuleCode
        d['hitQty'] = self.hitQty
        self._getDiseaseIdcard2(d)

    def param3_idcard_hitQty2(self):
        d = {}
        d['l_sql'] = self.getSql()
        l_ruleParam = Str_PO.str2list(self.ruleParam)
        d['ruleParam1'] = l_ruleParam[0].replace(".and.", ',')
        d['ruleParam2'] = l_ruleParam[1].replace(".and.", ',')
        d['ruleParam3'] = l_ruleParam[2].replace(".and.", ',')
        d['ruleCode'] = self.ruleCode
        d['diseaseRuleCode'] = self.diseaseRuleCode
        d['hitQty'] = self.hitQty
        self._getDiseaseIdcard2(d)

    def _getParamByGW(self):
        d = {}
        d['l_sql'] = self.getSql()
        d['ruleCode'] = self.ruleCode
        d['diseaseRuleCode'] = self.diseaseRuleCode
        self._getDiseaseIdcardGW(d)


    def outResult1(self, varQty):

        if varQty == 1:
            Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => OK]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTable, self.dbId))
        else:
            Color_PO.consoleColor("31", "31", (("error log").center(100, '-')), "")
            print(self.log)
            self.log = (self.log).replace("'", "''")
            Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => ERROR]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
        Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
        # Sqlserver_PO.execute("truncate table a_temporaryTable")
        Sqlserver_PO.execute("drop table %s" % (self.tmp_db))


    def outResult2(self, varQty):

        if varQty == 2:
            Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => OK]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTable, self.dbId))
        else:
            Color_PO.consoleColor("31", "31", (("error log").center(100, '-')), "")
            print(self.log)
            self.log = (self.log).replace("'", "''")
            Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => ERROR]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
        Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
        # Sqlserver_PO.execute("truncate table a_temporaryTable")
        Sqlserver_PO.execute("drop table %s" % (self.tmp_db))



    def outResultGW(self, d_actual):

        varSign = 0
        d_error = {}
        for k, v in d_actual.items():
            if (k == "QTY0" and v == 0) or (k != "QTY0" and v == 1):
                varSign = 0
            else:
                varSign = 1
                d_error[k] = v

        if Configparser_PO.SWITCH("SQL") == "on":
            print('值 => ' + str(d_actual))

        if varSign == 0:
            Color_PO.consoleColor("31", "36", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => OK]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='ok' where id=%s" % (self.dbTable, self.dbId))
            Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
            # Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTable, self.dbId))
        else:
            Color_PO.consoleColor("31", "31", (("error log").center(100, '-')), "")
            print(self.log)
            Color_PO.consoleColor("31", "31", '错误值 => ' + str(d_error), "")
            self.log = self.log + str(d_error)
            self.log = (self.log).replace("'", "''")
            Color_PO.consoleColor("31", "31", (("[" + str(self.sheetName) + " => " + str(self.dbId) + "(" + str(self.rule) + ") => ERROR]").center(100, '-')), "")
            Sqlserver_PO.execute("update %s set result='%s' where id=%s" % (self.dbTable, self.log, self.dbId))
            Sqlserver_PO.execute("update %s set updateDate='%s' where id=%s" % (self.dbTable, Time_PO.getDateTimeByDivide(), self.dbId))
            # Sqlserver_PO.execute("update %s set var='' where id=%s" % (self.dbTable, self.dbId))
        Sqlserver_PO.execute("drop table %s" % (self.tmp_db))


    def _getAutoIdcard(self, d):

        # 随机获取疾病身份证中身份证

        varIdcard = ""
        l_d_diseaseRuleCode_idcard = self.getDiseaseIdcard()
        # print(l_d_diseaseRuleCode_idcard)  # [{'diseaseRuleCode': 'YH_JB001', 'idcard': 310101202308070001}, ...]
        l_1 = []
        for i in range(len(l_d_diseaseRuleCode_idcard)):
            l_1.append(l_d_diseaseRuleCode_idcard[i]['idcard'])
        d["varIdcard"] = random.choice(l_1)
        # print(d["varIdcard"])
        self.verifyIdcard(varIdcard)
        if varIdcard != None:
            if 'hitQty' in d and d['hitQty'] == 2:
                self.outResult2(self.testRule(d))
            else:
                self.outResult1(self.testRule(d))
        else:
            Color_PO.consoleColor("31", "31", "[ERROR => _getDiseaseIdcard2() => 身份证不能为None!]", "")

    def _getDiseaseIdcard2(self, d):

        # 健康干预命中次数之获取身份证

        # print(d)
        varIdcard = ""
        l_d_diseaseRuleCode_idcard = self.getDiseaseIdcard()
        # print(l_d_diseaseRuleCode_idcard)
        for i in range(len(l_d_diseaseRuleCode_idcard)):
            for k, v in l_d_diseaseRuleCode_idcard[i].items():
                # print(l_d_diseaseRuleCode_idcard[i][k])
                if l_d_diseaseRuleCode_idcard[i][k] == d['diseaseRuleCode']:
                    varIdcard = l_d_diseaseRuleCode_idcard[i]['idcard']
                    break

        d["varIdcard"] = varIdcard
        self.verifyIdcard(varIdcard)

        if varIdcard != None:
            if 'hitQty' in d and d['hitQty'] == 2:
                self.outResult2(self.testRule(d))
            else:
                self.outResult1(self.testRule(d))
        else:
            Color_PO.consoleColor("31", "31", "[ERROR => _getDiseaseIdcard2() => 身份证不能为None!]", "")

    def _getDiseaseIdcardGW(self, d):

        # print(d)
        varIdcard = ""
        l_d_diseaseRuleCode_idcard = self.getDiseaseIdcard()
        # print(l_d_diseaseRuleCode_idcard)
        for i in range(len(l_d_diseaseRuleCode_idcard)):
            for k, v in l_d_diseaseRuleCode_idcard[i].items():
                # print(l_d_diseaseRuleCode_idcard[i][k])
                if l_d_diseaseRuleCode_idcard[i][k] == d['diseaseRuleCode']:
                    varIdcard = l_d_diseaseRuleCode_idcard[i]['idcard']
                    break
        d["varIdcard"] = varIdcard
        self.verifyIdcard(varIdcard)
        if varIdcard != None:
            # d_actual = self.gw(d)
            # l_ruleCode, d_actual = self.gw(d)
            # l_ruleCode.remove(d['diseaseRuleCode'])  # ['PG_JWS041', 'PG_JWS043']
            # print(d_actual)
            # self.outResultGW(l_ruleCode, d_all)
            # print(d_actual)
            self.outResultGW(self.gw(d))
        else:
            Color_PO.consoleColor("31", "31", "[ERROR => _getDiseaseIdcard() => 身份证不能为None!]", "")



    def testRule(self, d):

        # 执行r规则

        # print(d)  # {'rule': ['select top(1) ID,ID_CARD from T_ASSESS_INFO order by ID desc', "UPDATE T_ASSESS_INFO set {测试规则参数} where ID_CARD = '{varIdcard}'", "delete from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE = '{规则编码}'", 'self.i_rerunExecuteRule({varID})', "select count(*) QTY from T_ASSESS_RULE_RECORD where ASSESS_ID = {varID} and RULE_CODE= '{规则编码}'"], 'ruleParam': "AGE=55 , CATEGORY_CODE='2'", 'ruleCode': 'PG_Age001'}
        l_sql = d['l_sql']

        self.log = ""
        varQTY = 0
        varQ2 = 0

        for i in range(len(l_sql)):

            # 格式化sql
            if 'varIdcard' in d:
                l_sql[i] = str(l_sql[i]).replace("{身份证}", str(d['varIdcard']))
            if 'ruleParam1' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数1}", d['ruleParam1'])
            if 'ruleParam2' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数2}", d['ruleParam2'])
            if 'ruleParam3' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数3}", d['ruleParam3'])
            if 'ruleParam4' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数4}", d['ruleParam4'])
            if 'ruleParam' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数}", d['ruleParam'])
            if 'ruleCode' in d:
                l_sql[i] = str(l_sql[i]).replace("{规则编码}", d['ruleCode'])
            if "{随机数}" in l_sql[i]:
                l_sql[i] = str(l_sql[i]).replace("{随机数}", Data_PO.getPhone())
            if '{疾病评估规则编码}' in l_sql[i]:
                l_sql[i] = str(l_sql[i]).replace("{疾病评估规则编码}", d['diseaseRuleCode'])

        # pc.copy('')  # 清空剪贴板

        # 生成动态临时数据库
        self.tmp_db = 'a_temp' + str(Data_PO.getFigures(10))
        # print(self.tmp_db)
        Sqlserver_PO.crtTable(self.tmp_db, '''id INT IDENTITY(1,1) PRIMARY KEY, key1 VARCHAR(500), value1 VARCHAR(500)''')

        # 获取临时变量
        d_update = {}  # 更新数据
        # d_clipboard = {}  # 新数据
        for i in range(len(l_sql)):
            # clipboard = pc.paste()  # 从剪贴板获取数据

            # 将db转换成字典
            l = Sqlserver_PO.select("select key1, value1 from %s" % (self.tmp_db))
            # print(l) # [{'key1': 'ID', 'value1': '499948'}, {'key1': 'QTY', 'value1': '1'}, {'key1': 'Q2', 'value1': '1'},
            d_update = {}
            for p in range(len(l)):
                d_update[l[p]['key1']] = l[p]['value1']

            # if "{" in clipboard:
            #     d_clipboard = Str_PO.str2dict(clipboard)
            #     d_update.update(d_clipboard)  # 新数据合并到更新数据中

                if 'ID' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{ID}", str(d_update['ID']))
                if 'IDCARD' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{IDCARD}", str(d_update['IDCARD']))
                if 'ID_CARD' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{ID_CARD}", str(d_update['ID_CARD']))
                if 'GUID' in d_update:
                    l_sql[i] = str(l_sql[i]).replace("{GUID}", str(d_update['GUID']))

            # todo 输出sql语句
            if Configparser_PO.SWITCH("SQL") == "on":
                print(str(i + 1) + ", " + l_sql[i])  # 1, delete from T_ASSESS_INFO where ID_CARD = '310101202308070003'

            # 记录步骤日志
            if self.log == "":
                self.log = str(i + 1) + ", " + l_sql[i]
            else:
                self.log = self.log + "\n" + str(i + 1) + ", " + l_sql[i]

            # todo 执行sql
            a = self.runSql(l_sql[i])

            if a != None:
                if isinstance(a, list) and a != []:
                    if isinstance(a[0], dict):
                        # pc.copy(str(a[0]))  # 复制到剪贴板

                        # 将变量存入db
                        for k, v in a[0].items():
                            Sqlserver_PO.execute("insert into %s (key1,value1) values ('%s', '%s')" % (self.tmp_db, str(k), str(v)))

                        if Configparser_PO.SWITCH("SQL") == "on":
                            Color_PO.consoleColor("31", "33", a[0], "")  # 橙色显示参数值 {'ID': 498228, 'ID_CARD': '110101193001191103'}

                        if "QTY" in a[0]:
                            self.log = self.log + "\n" + str(a[0])  # 步骤日志
                            varQTY = a[0]['QTY']

                        if "hitQty" in d and d['hitQty'] == 2:
                            if "Q2" in a[0]:
                                self.log = self.log + "\n" + str(a[0])  # 步骤日志
                                varQ2 = a[0]['Q2']
                        else:
                            varQ2 = 0

        varQTY = int(varQTY) + int(varQ2)
        return varQTY

    def gw(self, d):

        # todo 执行gw规则

        l_sql = d['l_sql']
        d_actual = {}
        self.log = ""

        for i in range(len(l_sql)):
            # todo 格式化sql - gw
            if 'varIdcard' in d:
                l_sql[i] = str(l_sql[i]).replace("{身份证}", str(d['varIdcard']))
            if 'ruleParam1' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数1}", d['ruleParam1'])
            if 'ruleParam2' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数2}", d['ruleParam2'])
            if 'ruleParam3' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数3}", d['ruleParam3'])
            if 'ruleParam4' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数4}", d['ruleParam4'])
            if 'ruleParam' in d:
                l_sql[i] = str(l_sql[i]).replace("{测试规则参数}", d['ruleParam'])
            if 'ruleCode' in d:
                l_sql[i] = str(l_sql[i]).replace("{规则编码}", d['ruleCode'])
            if "{随机数}" in l_sql[i]:
                l_sql[i] = str(l_sql[i]).replace("{随机数}", Data_PO.getPhone())
            if '{疾病评估规则编码}' in l_sql[i]:
                l_sql[i] = str(l_sql[i]).replace("{疾病评估规则编码}", d['diseaseRuleCode'])

        # pc.copy('')  # 清空剪贴板
        # 生成动态临时数据库
        self.tmp_db = 'a_temp' + str(Data_PO.getFigures(10))
        # print(self.tmp_db)
        Sqlserver_PO.crtTable(self.tmp_db, '''id INT IDENTITY(1,1) PRIMARY KEY, key1 VARCHAR(500), value1 VARCHAR(500)''')

        # todo 获取临时变量 - gw
        d_update = {}  # 更新数据
        d_new = {}  # 新数据
        for i in range(len(l_sql)):
            # s = pc.paste()

            # 将db转换成字典
            l = Sqlserver_PO.select("select key1, value1 from %s" % (self.tmp_db))
            # print(l) # [{'key1': 'ID', 'value1': '499948'}, {'key1': 'QTY', 'value1': '1'}, {'key1': 'Q2', 'value1': '1'},
            d_update = {}
            for p in range(len(l)):
                d_update[l[p]['key1']] = l[p]['value1']

            # if "{" in s:
            #     d_new = Str_PO.str2dict(s)
            #     d_update.update(d_new)  # 新数据合并到更新数据中

            if 'ID' in d_update:
                l_sql[i] = str(l_sql[i]).replace("{ID}", str(d_update['ID']))
            if 'IDCARD' in d_update:
                l_sql[i] = str(l_sql[i]).replace("{IDCARD}", str(d_update['IDCARD']))
            if 'GUID' in d_update:
                l_sql[i] = str(l_sql[i]).replace("{GUID}", str(d_update['GUID']))

            # todo 输出sql语句 - gw
            if Configparser_PO.SWITCH("SQL") == "on":
                print(str(i + 1) + ", " + l_sql[i])  # 2, delete from T_ASSESS_INFO where ID_CARD = '310101202308070003'

            # todo 记录步骤日志 - gw
            if self.log == "":
                self.log = str(i + 1) + ", " + l_sql[i]
            else:
                self.log = self.log + "\n" + str(i + 1) + ", " + l_sql[i]

            # todo 执行sql - gw
            a = self.runSql(l_sql[i])

            if a != None:
                if isinstance(a, list) and a != []:
                    if isinstance(a[0], dict):
                        # pc.copy(str(a[0]))

                        # 将变量存入db
                        for k, v in a[0].items():
                            Sqlserver_PO.execute("insert into %s (key1,value1) values ('%s', '%s')" % (self.tmp_db, str(k), str(v)))

                        self.log = self.log + "\n" + str(a[0])
                        if Configparser_PO.SWITCH("SQL") == "on":
                            for k, v in a[0].items():
                                if k == "QTY0" or k == "ID":
                                    Color_PO.consoleColor("31", "33", a[0], "")
                                else:
                                    if v != 1 :
                                        Color_PO.consoleColor("31", "31", a[0], "")
                                    else:
                                        Color_PO.consoleColor("31", "33", a[0], "")
                        # print(a[0])
                        # print(d_actual)
                        from collections import ChainMap
                        d_actual = dict(ChainMap(a[0], d_actual))
                        # d_actual = Dict_PO.mergeDictReserveFirstKey(a[0], d_actual)  # {'a': 1, 'b': 2, 'dev': 30, 'test': 3}

        # ruleCode = d['ruleCode'].replace("(", '').replace(")", '').replace("'", '')
        # # print(ruleCode)  # 'GW_JB011','PG_JWS041','PG_JWS043'
        # l_ruleCode = Str_PO.str2list(ruleCode)
        if "ID" in d_actual:
            del d_actual['ID']
        if "ID_CARD" in d_actual:
            del d_actual['ID_CARD']
        if "GUID" in d_actual:
            del d_actual['GUID']
        return d_actual
