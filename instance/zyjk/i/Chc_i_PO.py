# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-3-6
# Description   : CHC 社区健康（静安）包，加密接口测试
# 接口文档：http://192.168.0.202:22081/doc.html
# todo nacos
# http://192.168.0.223:8848/nacos/	nacos,Zy123456
# chc-pp-test  //社区健康（静安）
# chc-gateway-sqlserver.yml
# thirdPublicKey: 0471d15668167f40390ee07e16f9515cf64c1bfab1d09c492c618c7caadf0c4285ce11bdebc420f5ebc13a79fab49e506aa8e24797891e67c2705fd38b4833b33b
# thirdPrivateKey: 686b3ec76f53610bbfbf171bf8b9ff9d17a15fb928155a2248f601b021e13b6b
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

class Chc_i_PO():

    def __init__(self, sm_account):
        # 登录
        # 获取用户token(lbl,Ww123456) '{"password": "Ww123456", "username": "lbl"}'
        # -d '4fa9de3518e897f29468be4e4e3956e53bae3cbdb8a.. 是用sm2对'{"password": "Ww123456", "username": "lbl"}'的加密，
        # 非加密写法 -d '{"password": "Ww123456", "username": "lbl"}'

        # todo chc-auth, 登录模块
        # 登录
        self.ipAddr = "http://192.168.0.202:22081"
        command = "curl -X POST '" + self.ipAddr + "/auth/login' -d '" + sm_account + "' -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Authorization:' -H 'Content-Type:application/json'"
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


    def curl(self, varRequestMethod, varUrl):
        command = "curl -X " + varRequestMethod + " " + self.ipAddr + varUrl + " -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Authorization:' -H 'Content-Type:application/json' -H 'Authorization:Bearer " + self.token + "'  -H 'token:" + self.token + "' "
        # print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        return d_r



    # todo REST-用户信息表

    def getFamilyDoc(self):
        # 获取家庭医生
        return self.curl("GET", "/system/sysUser/getFamilyDoc")

    def getAssistantList(self):
        # 获取家医助手
        return self.curl("GET", "/system/sysUser/getAssistantList")

    def getHealthManagerList(self):
        # 获取健康管理师
        return self.curl("GET", "/system/sysUser/getHealthManagerList")

    def getUser(self):
        # 根据用户名获取用户信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/getUser/lbl")

    def getUserByOrg(self):
        # 根据机构获取医生
        return self.curl("GET", "/system/sysUser/getUserByOrg")

    def getUserConfigByThird(self, orgCode, thridNO):
        # 获取用户配置信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/getUserConfigByThird")

    def getUserInfoByThirdNo(self, thirdNO):
        # 根据用户名获取用户信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/getUserInfoByThirdNo")

    def getUserInfoByThirdNoAndOrgCode(self, orgCode, thirdNO):
        # 根据用户名和机构号获取用户信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/getUserInfoByThirdNoAndOrgCode")

    def getUserInfoThirdInfo(self, orgCode, thirdNO):
        # 根据用户名获取用户信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/getUserInfoThirdInfo")

    def selectUserInfo(self):
        # 根据token获取用户信息（chc-system, REST-用户信息表）
        return self.curl("GET", "/system/sysUser/selectUserInfo?0=61b9ee3ad031da7b01c6429d5ad3b21757ee9766d5b9e964a77ce621d29bbf7e296f482360155e6e01b29bc557eeedf702b643456ba5b39fe6febf284537a91f88468105d513684ae1abd790025a95df6590470dcc6c5a21c79a105cce1cdbdd5d45")

    def sysUser(self, id):
        # 单条查询
        return self.curl("GET", "/system/sysUser/" + str(id))



    # todo REST-系统信息表

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

    def sysSystem(self, Id):
        # 单条查询
        return self.curl("GET", "/system/sysSystem/?" + str(Id))



    # todo chc-auth, 登录模块

    def logined(self, userName):
        # 确认用户是否已经登录
        return self.curl("POST", '/auth/logined')

    def logout(self):
        # 登出
        return self.curl("DELETE", '/auth/logout')

    def refresh(self):
        # 刷新
        return self.curl("POST", '/auth/refresh')

    def thirdLogin(self, orgCode, thirdNo):
        # 第三方登录
        return self.curl("POST", '/auth/thirdLogin')


# *****************************************************************

if __name__ == "__main__":


    # 登录(lbl,Ww123456)
    chc_i_PO = Chc_i_PO('9580414215bd76bf8ddd310c894fdfb155f439b427a43fb3dbb13a142055e4b7236fd7498a6e8d2febc7a44688c45d68c11606a34632ce07aa94d037124c0c15c0a19ab3c9f35bab234dd5bc8a3b37d419786c17b2e26d46d0f378e3691f2823e48804aecfb23ebc8511fd66e9b927bb5344d97a9f6c9c001ba4e76865f4890a5c6f7c21810fdedf6bbe85625e6ca990e1fe1cef025760c3382326c993')


    # todo chc-system, REST-系统信息表
    # print(chc_i_PO.querySystemRole(userId))  # 获取所有系统的角色
    print(chc_i_PO.systemMenuInfoBySystemId())  # 根据用户ID获取能够使用的系统
    # print(chc_i_PO.systemMenuInfo(systemId))  # 获取系统菜单
    # print(chc_i_PO.systemMenuInfoBySystemId(systemId))  # 根据系统Id获取所有菜单
    # print(chc_i_PO.sysSystem(Id))  # 单条查询


    # todo chc-system, REST-用户信息表
    # print(chc_i_PO.getFamilyDoc())  # 获取家庭医生
    # print(chc_i_PO.getAssistantList())  # 获取家医助手
    # print(chc_i_PO.getHealthManagerList())  # 获取健康管理师
    # print(chc_i_PO.getUser())  # 根据用户名获取用户信息
    # print(chc_i_PO.getUserByOrg())  # 根据机构获取医生
    # print(chc_i_PO.getUserConfigByThird(orgCode,thirdNO))  # 获取用户配置信息
    # print(chc_i_PO.getUserInfoByThirdNo(thirdNO))  # 根据用户名获取用户信息
    # print(chc_i_PO.getUserInfoByThirdNoAndOrgCode(orgCode,thirdNO))  # 根据用户名和机构号获取用户信息
    # print(chc_i_PO.getUserInfoThirdInfo(orgCode,thirdNO))  # 根据用户名获取用户信息
    print(chc_i_PO.selectUserInfo())  # 根据token获取用户信息
    # print(chc_i_PO.sysUser(id))  # 单条查询



    # todo chc-auth, 登录模块
    # print(chc_i_PO.logined())  # 确认用户是否已经登录
    print(chc_i_PO.logout())  # 登出
    # print(chc_i_PO.refresh())  # 刷新
    # print(chc_i_PO.thirdLogin(orgCode,thridNo))  # 第三方登录


