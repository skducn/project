import unittest
import paramunittest
import readConfig as readConfig
from common.Log import MyLog
from common import common
from common import configHttp

localGenerate_xls = common.get_xls("userCase.xlsx", "generate")
localConfigHttp = configHttp.ConfigHttp()
localReadConfig = readConfig.ReadConfig()


@paramunittest.parametrized(*localGenerate_xls)
class Generate(unittest.TestCase):

    def setParameters(self, case_name, method, result, code, msg):
        """
        set parameters
        :param case_name:
        :param method:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
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

    def testGenerate(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('generate')
        localConfigHttp.set_url(self.url)

        # test interface
        self.response = localConfigHttp.get()

        # check result
        self.checkResult()

    def tearDown(self):
        """

        :return:
        """
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])

    def checkResult(self):
        """
        check test reslt
        :return:
        """
        self.info = self.response.json()
        common.show_return_msg(self.response)

        if self.result == '0':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
