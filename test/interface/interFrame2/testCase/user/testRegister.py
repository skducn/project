import readConfig as readConfig
from common.Log import MyLog
from common import configHttp
from common import common
import unittest
import paramunittest
from common import configDB

register_xls = common.get_xls("userCase.xlsx", "register")
localConfigHttp = configHttp.ConfigHttp()
localReadConfig = readConfig.ReadConfig()
localConfigDB = configDB.MyDB()


@paramunittest.parametrized(*register_xls)
class Register(unittest.TestCase):

    def setParameters(self, case_name, method, token, email, password, confirmpwd, result, code, msg):
        """
        set parameters
        :param case_name:
        :param method:
        :param token:
        :param email:
        :param password:
        :param confirmpwd:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.email = str(email)
        self.password = str(password)
        self.confirmpwd = str(confirmpwd)
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

    def testRegister(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('register')
        localConfigHttp.set_url(self.url)

        # set header
        if self.token == '0':
            token = localReadConfig.get_headers("token_v")
        elif self.token == '1':
            token = None
        header = {'token': token}
        localConfigHttp.set_headers(header)

        # set params
        data = {'email': self.email,
                'password': self.password,
                'password_confirm': self.confirmpwd}
        localConfigHttp.set_data(data)

        # test interface
        self.response = localConfigHttp.post()

        # check result
        self.checkResult()

    def tearDown(self):
        """

        :return:
        """
        # build line
        self.log.build_case_line(self.case_name, self.info['code'], self.info['msg'])

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.response.json()
        # show return message
        common.show_return_msg(self.response)
        if self.result == '0':
            # get register email
            email = common.get_value_from_return_json(self.info, 'member', 'email')
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            self.assertEqual(email, self.email)

        if self.result == '1':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            if self.case_name == 'register_EmailExist':
                # delete register user from db
                sql = common.get_sql('newsitetest', 'rs_member', 'delete_user')
                localConfigDB.executeSQL(sql, self.email)
                localConfigDB.closeDB()
