# -*- coding: utf-8 -*-
# *****************************************************************
# Author        : John
# Date          : 2024-3-6
# Description   : CHC封装包，加密接口测试（静安），无场景
# 接口文档：http://192.168.0.202:22081/doc.html
# *****************************************************************


import subprocess, json

class Chc_i_PO():

    def __init__(self):
        # 登录（登录模块）
        # 获取用户token(lbl,Ww1234567)

        self.ipAddr = "http://192.168.0.202:22081"

        command = "curl -X POST '" + self.ipAddr + "/auth/login' -d '4fa9de3518e897f29468be4e4e3956e53bae3cbdb8a64310f41ecbdf76843eb4c81acf3721bf8113cf4d3563c698ab74e060989daab802154ea144938bfcdc228608df8ec3548140f9fe745b6fc11bdf0d1c679116d56648d55e362fd3334b0a5f2a0995918b49e3f273c96dc3fd9f1a0b719dccd5910039783c6315bbf2156432003e34d8dada6e81c58d42a674a455ccdfeb41323b379fe1c06ab36462' " \
                  "-H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Authorization:' -H 'Content-Type:application/json'"
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


    def curl(self, status, curl, token=""):
        command = "curl -X " + status + " " + self.ipAddr + curl + " -H 'Request-Origion:SwaggerBootstrapUi' -H 'accept:*/*' -H 'Authorization:' -H 'Content-Type:application/json' -H 'Authorization:Bearer " + token + "'  -H 'token:" + token + "' "
        # print(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        str_r = bytes.decode(out)
        d_r = json.loads(str_r)
        return d_r


    def logout(self):
        # 登出（登录模块）
        return self.curl("DELETE", '/auth/logout', self.token)

    def systemMenuInfoBySystemId(self):
        # 根据用户ID获取能够使用的系统（系统信息表）
        return self.curl("GET", "/system/sysSystem/systemMenuInfoBySystemId?0=950c364d4694618ca13897b742ac7db1752f96c4a778dcb046847e4004d3b62f96e6a125ec604492a0915a47d3b6f6ef87df2f8ec7e718dd308e52f74135ed223adbfeac733f4cc9616f97146cc572d8e748ce23514798982364bd5171e5291ff8c3c34ac2aa8d2d8796e92a4f3d", self.token)

    def selectUserInfo(self):
        # 根据token获取用户信息（用户信息表）
        return self.curl("GET", "/system/sysUser/selectUserInfo?0=61b9ee3ad031da7b01c6429d5ad3b21757ee9766d5b9e964a77ce621d29bbf7e296f482360155e6e01b29bc557eeedf702b643456ba5b39fe6febf284537a91f88468105d513684ae1abd790025a95df6590470dcc6c5a21c79a105cce1cdbdd5d45", self.token)


# *****************************************************************

if __name__ == "__main__":

    # 登录
    chc_i_PO = Chc_i_PO()

    # 根据用户ID获取能够使用的系统（系统信息表）
    print(chc_i_PO.systemMenuInfoBySystemId())

    # 根据token获取用户信息（用户信息表）
    print(chc_i_PO.selectUserInfo())

    # 登出
    print(chc_i_PO.logout())

