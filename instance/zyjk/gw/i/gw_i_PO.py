# *****************************************************************
# Author        : John
# Date          : 2024-6-18
# Description   : gw 公卫接口测试
# 接口文档：http://192.168.0.203:38080/doc.html
# web：http://192.168.0.203:30080  testwjw, Qa@123456

# 在线国密SM2加密/解密 https://the-x.cn/zh-cn/cryptography/Sm2.aspx
# 在线SM2公钥私钥对生成，加密/解密 https://config.net.cn/tools/sm2.html
# 密钥：124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62
# 公钥：04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249

# 【腾讯文档】项目信息表
# https://docs.qq.com/sheet/DYmZMVmFTeXFWRFpQ?tab=BB08J2

# todo nacos
# http://192.168.0.223:8848/nacos/	nacos,Zy123456
# phs-test
# phs-gateway-sqlserver.yml
# publicKey: 04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249
# privateKey: 124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62
# enabled: false    // 改为false无法登录，因为页面加密，用于接口测试
# 安全配置
# # security:
#   验证码
#   # captcha:
#   #   enabled: false    //去掉验证码
# *****************************************************************

import subprocess, json
from PO.WebPO import *

from PO.ColorPO import *
Color_PO = ColorPO()

from ConfigparserPO import *
Configparser_PO = ConfigparserPO('config.ini')


class Gw_i_PO():

    def __init__(self):

        # self.ipAddr = "http://192.168.0.202:38080"
        self.ipAddr = Configparser_PO.HTTP("url")


    def _sm2(self, Web_PO):

        Web_PO.openURL("https://config.net.cn/tools/sm2.html")
        # 私钥
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[1]/textarea[1]",
                          "124c93b524b25e8ca288dde1c08b78e76e188d2e6e6c7a5142cdc3eb38a5ab62")
        # 公钥
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[1]/textarea[2]",
                          '04025d84101aa6ba2835995c2e72c0d9f49f382a87ace7e2770a511e1bbe95a40a2800a40bc966b3a51e4d36735e2b5941dd6e10f502f68fbc42a0ba7cec7ab249')

    def encrypt(self, varSource):

        # 在线sm2加密

        Web_PO = WebPO("noChrome")
        self._sm2(Web_PO)
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[2]/textarea[1]", varSource)
        Web_PO.clkByX("/html/body/div[2]/div/div[1]/div[2]/div[1]/a[1]", 1)
        r = Web_PO.getAttrValueByX("/html/body/div[2]/div/div[1]/div[2]/textarea[2]", "value")
        return r

    def decrypt(self, varEncrypt):

        # 在线sm2解密

        Web_PO = WebPO("noChrome")
        self._sm2(Web_PO)
        Web_PO.setTextByX("/html/body/div[2]/div/div[1]/div[2]/textarea[2]", varEncrypt)
        Web_PO.clkByX("/html/body/div[2]/div/div[1]/div[2]/div[2]/a[1]", 1)
        r = Web_PO.getAttrValueByX("/html/body/div[2]/div/div[1]/div[2]/textarea[1]", "value")
        return r


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

        Color_PO.outColor([{"35": "token =>"}, {"35": self.token}])

        # print("token =>", self.token)

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




    # todo REST-用户信息表

    def getDocByOrg(self):
        # 根据当前所在的机构获取医生
        return self.curl("GET", "/system/sysUser/getDocByOrg")

    def getFamilyDoc(self):
        # 获取家庭医生
        return self.curl("GET", "/system/sysUser/getFamilyDoc")

    def getOrgUser(self):
        # 当前登录用户所在机构及子机构用户
        return self.curl("GET", "/system/sysUser/getOrgUser")

    def getUser(self):
        # 根据用户名获取用户信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/getUser/lbl")

    def getUserByOrg(self):
        # 根据机构获取医生
        return self.curl("GET", "/system/sysUser/getUserByOrg")

    def getVisitUser(self):
        # 根据机构获取医生--随访使用
        return self.curl("GET", "/system/sysUser/getVisitUser")

    def selectUserInfo(self):
        # 根据token获取用户信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/selectUserInfo?0=61b9ee3ad031da7b01c6429d5ad3b21757ee9766d5b9e964a77ce621d29bbf7e296f482360155e6e01b29bc557eeedf702b643456ba5b39fe6febf284537a91f88468105d513684ae1abd790025a95df6590470dcc6c5a21c79a105cce1cdbdd5d45")

    def sysUser(self, id):
        # 单条查询
        return self.curl("GET", "/system/sysUser/" + str(id))



    # todo phs-system, REST-系统信息表

    def querySystemRole(self, userId):
        # 获取所有系统的角色
        return self.curl("GET", "/system/sysSystem/querySystemRole?" + str(userId))

    def systemMenuInfoBySystemId(self):
        # 根据系统Id获取所有菜单
        return self.curl("GET", "/system/sysSystem/systemMenuInfoBySystemId?0=950c364d4694618ca13897b742ac7db1752f96c4a778dcb046847e4004d3b62f96e6a125ec604492a0915a47d3b6f6ef87df2f8ec7e718dd308e52f74135ed223adbfeac733f4cc9616f97146cc572d8e748ce23514798982364bd5171e5291ff8c3c34ac2aa8d2d8796e92a4f3d")

    def systemMenuInfo(self, systemId):
        # 获取系统菜单
        return self.curl("GET", "/system/sysSystem/systemMenuInfo?" + str(systemId))

    def systemMenuInfoBySystemId(self, systemId):
        # 根据系统Id获取所有菜单
        return self.curl("GET", "/system/sysSystem/systemMenuInfoBySystemId?" + str(systemId))

    def systemMenuInfoByUserId(self):
        # 根据用户ID获取能够使用的系统及菜单
        return self.curl("GET", "/system/sysSystem/systemMenuInfoByUserId")


    def sysSystem(self, Id):
        # 单条查询
        return self.curl("GET", "/system/sysSystem/?" + str(Id))



    # todo phs-auth, 登录模块

    def logined(self, userName):
        # 确认用户是否已经登录
        return self.curl("POST", '/auth/logined')

    def logout(self):
        # 登出
        return self.curl("DELETE", '/auth/logout')

    def refresh(self):
        # 刷新
        return self.curl("POST", '/auth/refresh')




# *****************************************************************

if __name__ == "__main__":


    # 登录(testwjw, Qa@123456)
    gw_i_PO = Gw_i_PO('9580414215bd76bf8ddd310c894fdfb155f439b427a43fb3dbb13a142055e4b7236fd7498a6e8d2febc7a44688c45d68c11606a34632ce07aa94d037124c0c15c0a19ab3c9f35bab234dd5bc8a3b37d419786c17b2e26d46d0f378e3691f2823e48804aecfb23ebc8511fd66e9b927bb5344d97a9f6c9c001ba4e76865f4890a5c6f7c21810fdedf6bbe85625e6ca990e1fe1cef025760c3382326c993')

    # todo chc-system, REST-用户信息表
    print(gw_i_PO.getDocByOrg())  # 根据当前所在的机构获取医生
    print(gw_i_PO.getFamilyDoc())  # 获取家庭医生
    print(gw_i_PO.getOrgUser())  # 当前登录用户所在机构及子机构用户
    # print(gw_i_PO.getUser())  # 根据用户名获取用户信息
    # print(gw_i_PO.getUserByOrg())  # 根据机构获取医生
    # print(gw_i_PO.getVisitUser())  # 根据机构获取医生--随访使用
    print(gw_i_PO.selectUserInfo())  # 根据token获取用户信息
    # print(gw_i_PO.sysUser(id))  # 单条查询


    # todo chc-system, REST-系统信息表
    # print(gw_i_PO.querySystemRole(userId))  # 获取所有系统的角色
    print(gw_i_PO.systemMenuInfoBySystemId())  # 根据用户ID获取能够使用的系统
    print(gw_i_PO.systemMenuInfoByUserId())  # 根据用户ID获取能够使用的系统及菜单
    # print(gw_i_PO.systemMenuInfo(systemId))  # 获取系统菜单
    # print(gw_i_PO.systemMenuInfoBySystemId(systemId))  # 根据系统Id获取所有菜单
    # print(gw_i_PO.sysSystem(Id))  # 单条查询






    # todo chc-auth, 登录模块
    # print(gw_i_PO.logined())  # 确认用户是否已经登录
    print(gw_i_PO.logout())  # 登出
    # print(gw_i_PO.refresh())  # 刷新


