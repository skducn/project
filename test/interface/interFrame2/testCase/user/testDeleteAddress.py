import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp

deleteAddress_xls = common.get_xls("userCase.xlsx", "deleteAddress")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()


@paramunittest.parametrized(*deleteAddress_xls)
class DeleteAddress(unittest.TestCase):
    def setParameters(self, case_name, method, address_id, result, code, msg):
        """
        set params
        :param case_name:
        :param method:
        :param address_id:
        :param code:
        :param result:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.address_id = str(address_id)
        self.code = str(code)
        self.result = str(result)
        self.msg = str(msg)
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
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()

    def testGetAddressList(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('deleteAddress')
        configHttp.set_url(self.url)

        # get visitor token
        token = localReadConfig.get_headers("TOKEN_U")

        # set headers
        header = {"token": str(token)}
        configHttp.set_headers(header)

        # set params
        params = {"address_id": self.address_id}
        configHttp.set_params(params)

        # test interface
        self.return_json = configHttp.get()

        # check result
        self.checkResult()

    def tearDown(self):
        """

        :return:
        """
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        common.show_return_msg(self.return_json)

        if self.result == '0':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            value = self.info['info']['result']
            self.assertEqual(str(value), 1)

        if self.result == '1':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
