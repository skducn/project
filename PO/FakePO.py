# coding=utf-8
# ***************************************************************
# Author     : John
# Created on : 2019-9-19
# Description: fake
# 关于大数据测试，你一定要试试python的fake库！ http://www.51testing.com/html/53/15150753-7793925.html
# 官网 https://faker.readthedocs.io/en/master/
# pip3.9 install faker
# ***************************************************************

from faker import Faker
from faker.providers import internet

fake = Faker()
fake.add_provider(internet)

print(fake.ipv4_private())

class FakePO():

    ...



if __name__ == '__main__':

    Fake_PO = FakePO()
    faker = Faker()
    faker_zh = Faker(locale='Zh_CN')
    faker_jp = Faker(locale='ja_JP')
    list1 = []
    list3 = ['今天','你好','谢谢','意愿']
    for i in range(30):
        zh_name = faker_zh.name()
        zh_company = faker_zh.company()
        zh_phone = faker_zh.phone_number()
        zh_email = faker_zh.email()
        zh_birthday = faker_zh.date(pattern="%Y-%m-%d")
        zh_city = faker_zh.city()
        zh_ssn = faker_zh.ssn()
        url = faker_zh.url()
        src = faker_zh.ipv4(network=False)
        dst = faker_zh.ipv4(network=False)
        name = faker.name()
        jp_name = faker_jp.name()
        test = faker.sentence(ext_word_list=list3)
        zh_add = faker_zh.address()
        zh_text = faker_zh.text()

        data = [zh_text,zh_add,test,zh_name,zh_company,zh_phone,zh_email,zh_birthday,zh_city,zh_ssn,url,src,name,jp_name]

    list1.append(data)

    print(list1)