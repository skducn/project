import unittest
import paramunittest
import readConfig as readConfig
from common import configHttp
from common import businessCommon
from common import common
from common.Log import MyLog

localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()
localUpdatePassword_xls = common.get_xls("userCase.xlsx", "updatePassword")


@paramunittest.parametrized(*localUpdatePassword_xls)
class UpdatePassword(unittest.TestCase):

    def setParameters(self, case_name, method, token, old_password, password, password_confirm, result, code, msg):
        """
        set parameters
        :param case_name:
        :param method:
        :param token:
        :param old_password:
        :param password:
        :param password_confirm:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.oldPwd = str(old_password)
        self.pwd = str(password)
        self.pwdConfirm = str(password_confirm)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.response = None
        self.info = None
        self.login_token = None

    def description(self):
        """

        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        # login
        self.login_token = businessCommon.login()

    def testUpdatePassword(self):
        """
        test body
        :return:
        """

        # set url
        self.url = common.get_url_from_xml('updatePassword')
        localConfigHttp.set_url(self.url)

        # set header
        if self.token == '0':
            token = self.login_token
        elif self.token == '1':
            token = localReadConfig.get_headers("token_v")
        else:
            token = self.token
        header = {'token': token}
        localConfigHttp.set_headers(header)

        # set param
        data = {'old_password': self.oldPwd,
                'password': self.pwd,
                'password_confirm': self.pwdConfirm}
        localConfigHttp.set_data(data)

        # test interface
        self.response = localConfigHttp.post()

        # check result
        self.checkResult()

    def tearDown(self):
        """

        :return:
        """
        # logout
        businessCommon.logout(self.login_token)
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.response.json()
        common.show_return_msg(self.response)

        if self.result == '0':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            self.assertEqual(self.info['info']['result'], 1)
            # restore environment
            data = {
                'old_password': self.pwd,
                'password': self.oldPwd,
                'password_confirm': self.oldPwd
            }
            localConfigHttp.set_data(data)
            localConfigHttp.post()

        if self.result == '1':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
