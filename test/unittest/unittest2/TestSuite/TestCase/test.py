# coding:utf-8
from selenium import webdriver
import time,unittest
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import firefox
from selenium.webdriver.common.keys import Keys
from time import sleep
import datetime

# varTimeYMDHSM = datetime.datetime.now().strftime('%Y%m%d%H%M%S');  #20160623183734

varTimeY_M_D = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print varTimeY_M_D

print 1%5
print 7%5
print 13%5

sleep(1212)
print
str1='2333'
str12='2,3,4'

list1=[]
print len(str1.split(','))
for i in range(len(str1.split(','))):
    list1.append(str1.split(',')[i])
    print int(list1[i])

sleep(1212)



class Untitled(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.url = "https://www.hao123.com/"
        x='121212'

    def test_Untitled (self):
        driver = self.driver
        driver.get(self.url)
        now_handle = driver.current_window_handle #获取当前窗口句柄
        driver.find_element_by_id("search-input").send_keys("selenium")
        driver.find_element_by_xpath("//*[@id='search-form']/div[2]/input").click()
        time.sleep(5)
        print now_handle
        print type(now_handle)
        driver.switch_to_window(now_handle)


        # driver.switch_to_window(driver.window_handles[0])

        time.sleep(1212)
        all_handles = driver.window_handles #获取所有窗口句柄

        for handle in all_handles:

            if handle != now_handle:
                print handle    #输出待选择的窗口句柄
                driver.switch_to_window(handle)
                driver.find_element_by_id("search-input").send_keys("selenium")
                driver.find_element_by_xpath("//*[@id='search-form']/div[2]/input").click()
                time.sleep(5)
                driver.close() #关闭当前窗口
        time.sleep(3)
        print now_handle   #输出主窗口句柄
        driver.switch_to_window(now_handle) #返回主窗口
        time.sleep(2)
        driver.find_element_by_id("kw").clear()
        driver.find_element_by_id("kw").send_keys("abc")
        driver.find_element_by_id("su").click()

        time.sleep(10)

    def tearDown(self):
        self.driver.quit()
        #pass


if __name__ == "__main__":
    unittest.main()