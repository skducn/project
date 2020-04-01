import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import common
from common import configHttp as ConfigHttp
from common import businessCommon

addAddress_xls = common.get_xls("userCase.xlsx", "addAddress")
localReadConfig = readConfig.ReadConfig()
configHttp = ConfigHttp.ConfigHttp()


@paramunittest.parametrized(*addAddress_xls)
class AddAddress(unittest.TestCase):
    def setParameters(self, case_name, method, token, sex, fname, lname, tel, standby_tel, address1, address2, city, state, postcode, country_id, tax_number, company, fax, is_default, result, code, msg):
        """
        set params
        :param case_name:
        :param method:
        :param token:
        :param sex:
        :param fname:
        :param lname:
        :param tel:
        :param standby_tel:
        :param address1:
        :param address2:
        :param city:
        :param state:
        :param postcode:
        :param country_id:
        :param tax_number:
        :param company:
        :param fax:
        :param is_default:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.token = str(token)
        self.sex = str(sex)
        self.fname = str(fname)
        self.lname = str(lname)
        self.tel = str(tel)
        self.standby_tel = str(standby_tel)
        self.address1 = str(address1)
        self.address2 = str(address2)
        self.city = str(city)
        self.state = str(state)
        self.postcode = str(postcode)
        self.country_id = str(country_id)
        self.tax_number = str(tax_number)
        self.company = str(company)
        self.fax = str(fax)
        self.is_default = str(is_default)
        self.result = str(result)
        self.code = str(code)
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
        self.login_token = businessCommon.login()

    def testAddAddress(self):
        """
        test body
        :return:
        """
        # set url
        self.url = common.get_url_from_xml('addAddress')
        configHttp.set_url(self.url)

        # get token
        if self.token == '0':
            token = self.login_token
        elif self.token == '1':
            token = localReadConfig.get_headers("TOKEN_U")
        else:
            token = self.token

        # set headers
        header = {"token": str(token)}
        configHttp.set_headers(header)

        # set params
        data = {"sex": self.sex,
                "fname": self.fname,
                "lname": self.lname,
                "tel": self.tel,
                "standby_tel": self.standby_tel,
                "address1": self.address1,
                "address2": self.address2,
                "city": self.city,
                "state": self.state,
                "postcode": self.postcode,
                "country_id": self.country_id,
                "tax_number": self.tax_number,
                "company": self.company,
                "fax": self.fax,
                "is_default": self.is_default}
        configHttp.set_data(data)

        # test interface
        self.return_json = configHttp.post()

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
        self.info = self.return_json.json()
        common.show_return_msg(self.return_json)

        if self.result == '0':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
            self.assertEqual(common.get_value_from_return_json(self.info, 'address', 'sex'), self.sex)
            self.assertEqual(common.get_value_from_return_json(self.info, 'address', 'fname'), self.fname)
            self.assertEqual(common.get_value_from_return_json(self.info, 'address', 'lname'), self.lname)
            self.assertEqual(common.get_value_from_return_json(self.info, 'address', 'tel'), self.tel)
            self.assertEqual(common.get_value_from_return_json(self.info, 'address', 'address1'), self.address1)
            self.assertEqual(common.get_value_from_return_json(self.info, 'address', 'city'), self.city)
            self.assertEqual(common.get_value_from_return_json(self.info, 'address', 'state'), self.state)
            self.assertEqual(common.get_value_from_return_json(self.info, 'address', 'postcode'), self.postcode)
            self.assertEqual(common.get_value_from_return_json(self.info, 'address', 'countryId'), self.country_id)

        if self.result == '1':
            self.assertEqual(self.info['code'], self.code)
            self.assertEqual(self.info['msg'], self.msg)
