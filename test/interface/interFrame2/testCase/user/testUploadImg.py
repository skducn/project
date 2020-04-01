import os
import unittest
import paramunittest
import readConfig as readConfig
from common import common
from common import configHttp
from common import businessCommon
from common.Log import MyLog

localUploadImg_xls = common.get_xls("userCase.xlsx", "uploadImg")
localReadConfig = readConfig.ReadConfig()
localConfigHttp = configHttp.ConfigHttp()


@paramunittest.parametrized(*localUploadImg_xls)
class UploadImg(unittest.TestCase):

    def setParameters(self, case_name, method, token, whole, file, result, code, msg):
        """
        set param
        :param case_name:
        :param method:
        :param token:
        :param whole:
        :param file:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.whole = str(whole)
        self.file = str(file)
        self.result = str(result)
        self.code = str(code)
        self.msg = str(msg)
        self.response = None
        self.info = None

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
        self.login_token = businessCommon.login()

    def testUploadImg(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('uploadImg')
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

        # set files
        localConfigHttp.set_files(self.file)

        # set data
        data = {'whole': self.whole}
        localConfigHttp.set_data(data)

        # test interface
        self.response = localConfigHttp.postWithFile()

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
            if self.whole == '1':
                self.assertEqual(self.info['code'], self.code)
                self.assertEqual(self.info['msg'], self.msg)
                self.assertIn('http://img.shein.com/', self.info['info']['imgUrl'])
            if self.whole == '0':
                self.assertEqual(self.info['code'], self.code)
                self.assertEqual(self.info['msg'], self.msg)
                self.assertNotIn('http://img.shein.com/', self.info['info']['imgUrl'])

        if self.result == '1':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)

