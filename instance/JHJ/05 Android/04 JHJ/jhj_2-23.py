import os
import sys
import unittest
from appium import webdriver
from time import sleep

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)

class Jhj1_2(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['appPackage'] = 'cn.jihaojia'
        desired_caps['appActivity'] = 'cn.jihaojia.activity.GuidanceActivity'
        reload(sys)
        sys.setdefaultencoding('utf-8')  
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    @classmethod 
    def tearDownClass(self):
        self.driver.quit()

    @unittest.skip("skip")  
    def test1_homepage(self):
        #首页
        print "1212"
        
    @unittest.skip("skip")  
    def test2_zdm(self):
        #值得买
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[1].click()

    @unittest.skip("skip")  
    def test3_live(self):
        #生活家
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[2].click()

    @unittest.skip("skip")  
    def test4_search(self):
        #搜索
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[3].click()

    def test5_my(self):        
        #我的
        sleep(6)
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
        sleep(2)
        #我的 - 我的订单
        myorders=self.driver.find_elements_by_class_name("android.widget.TextView")
        for myorder1 in myorders :
            if myorder1.text=="我的订单" :
               myorder1.click()
        sleep(2)
        
        #C1，验证“全部、代付款、待发货、待收货、评价”
        #未完成？？

        #获取购物车右上角数字        
        ShopCarIconNum= self.driver.find_element_by_id("cn.jihaojia:id/goshopnum").text
        #self.assertEqual(int(ShopCarIconNum.encode("utf-8")),4)  #将字符串转整数
        #self.assertEqual(int(a),2100)               
        #我的 - 我的订单 - 点击购物车
        self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click()
        #C2，验证购物车里商品数量与购物车右上角数字是否一致
        ShopCarQTYs=self.driver.find_elements_by_id("cn.jihaojia:id/shopping_checkbox")
        qtys=0
        for ShopCarQTY in ShopCarQTYs:
            qtys=qtys+1
        self.assertEqual(int(ShopCarIconNum.encode("utf-8")),qtys)
        #选择一个商品
        self.driver.find_elements_by_id("cn.jihaojia:id/shopping_checkbox")[0].click()        
        sleep(3)
        #C3,验证所选商品（价格*数量）的合计是否与总计一致
        #价格
        SinglePrices0=self.driver.find_elements_by_id("cn.jihaojia:id/shoping_money")
        tmp1=0
        for SinglePrice0 in SinglePrices0 :
            if tmp1==0 :
               SglPrs0=float(SinglePrice0.text.replace("¥","")) 
               self.assertEqual(float(SinglePrice0.text.replace("¥","")),27.6)  #27.6
               break
             
            tmp1=tmp1+1
        sleep(2)
        
        #数量
        SingleQtys0=self.driver.find_elements_by_id("cn.jihaojia:id/shoping_cart_number")
        tmp2=0
        for SingleQTY0 in SingleQtys0 :
            if tmp2==0 :
               SglNum0=int(SingleQTY0.text)
               self.assertEqual(int(SingleQTY0.text),5)  #5
               break
        
            tmp1=tmp1+1
        sleep(2)
        ShopCarMoney=self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_money").text
        AllTotal=SglPrs0*SglNum0
        self.assertEqual(float(ShopCarMoney.replace("¥","")),AllTotal)  #AllTotal

        self.assertEqual(SingleQty0,12)  
        
        
        #去结算
        #self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_pay").click()
        sleep(4)
        self.driver.find_element_by_id("cn.jihaojia:id/pay").click()
        sleep(5)
        #支付宝页面返回
        self.driver.find_element_by_class_name("android.widget.Button").click()
        sleep(2)
        self.driver.find_element_by_class_name("android.widget.ImageView").click()
        sleep(3)
        self.driver.find_element_by_id("android:id/button1").click()
        
      
                
        sleep(5)

        #android.widget.FrameLayout
        
        
        #self.driver.find_element_by_name("ÎÒµÄ¶©µ¥").click()
        #抵用券
        self.driver.find_element_by_id("cn.jihaojia:id/coupon_layout").click()
        sleep(4)        
        #输入错误抵用券
        self.driver.find_element_by_id("cn.jihaojia:id/input_recommendcode").send_keys("122")        
        self.driver.find_element_by_id("cn.jihaojia:id/dialog_button_ok").click()
        if "¶Ò»»Âë´íÎó" in self.driver.find_element_by_id("cn.jihaojia:id/txt_title").text :
            print "Test pass"
        else :
            print "Test error"
        sleep(2)
        self.driver.find_element_by_id("cn.jihaojia:id/btn_pos").click()
        sleep(4)
        #回退
        self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()

        #常用联系人/地址
        sleep(2)
        self.driver.find_element_by_id("cn.jihaojia:id/address").click()
        
       


        #self.driver.find_element_by_name("John").click()
        sleep(5)
            
        #el.click()
            

if __name__ == '__main__':
## 对多个不同类进行测试    
    suite1 = unittest.TestLoader().loadTestsFromTestCase(Jhj1_2)
##    suite2 = unittest.TestLoader().loadTestsFromTestCase(MainTest2)
##    allTests = unittest.TestSuite([suite1,suite2])
##    unittest.TextTestRunner(verbosity=2).run(allTests)
    unittest.TextTestRunner(verbosity=2).run(suite1)


## unittest https://docs.python.org/2/library/unittest.html
##可以使用unitest.skip装饰器族跳过test method或者test class,这些装饰器包括:
##① @unittest.skip(reason):无条件跳过测试，reason描述为什么跳过测试
##② @unittest.skipif(conditition,reason):condititon为true时跳过测试
##③ @unittest.skipunless(condition,reason):condition不是true时跳过测试
    # @unittest.skipIf(os.path.isfile("~/1.txt") != True , "can't find files) #带条件判断
##数字变为字符串 str(4)
##字符串变为数字 string.atoi(s,[，base]) //base为进制基数
##浮点数转换 string.atof(s)
##字符转数字 int(str)
