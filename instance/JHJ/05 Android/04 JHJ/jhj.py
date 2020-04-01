# coding: utf-8
import os
import sys
import unittest
from appium import webdriver
from time import sleep

#import chardet
#print chardet.detect('中国')

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
        desired_caps['unicodeKeyboard'] ='True'
        desired_caps['resetKeyboard'] = 'True'
        reload(sys)
        sys.setdefaultencoding('utf8')
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    @classmethod 
    def tearDownClass(self):
        self.driver.quit()

    @unittest.skip("未做 首页")
    def test1_homepage(self):
        #首页
      print "12121"
        
    @unittest.skip("未做 值得买")
    def test2_zdm(self):
        #值得买
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[1].click()

    @unittest.skip("未做 生活家")
    def test3_live(self):
        #生活家
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[2].click()

    @unittest.skip("未做 搜索")
    def test4_search(self):
        #搜索
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[3].click()

    @unittest.skip("已完成 我的订单")
    def test5_1_My(self):
        #我的
        sleep(3)
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
        ##################################################################################
        #调用购物车方法 ShorCar(2)表示选择2个商品
        self.ShopCar(2)
        ##################################################################################

        self.assertEqual(11111,12)

        sleep(4)
        self.driver.find_element_by_id("cn.jihaojia:id/pay").click()
        sleep(5)
        #支付宝页面返回
        self.driver.find_element_by_class_name("android.widget.Button").click()
        sleep(2)
        self.driver.find_element_by_class_name("android.widget.ImageView").click()
        sleep(3)
        self.driver.find_element_by_id("android:id/button1").click()
        
    @unittest.skip("处理中 抵用券")
    def test5_2_Voucher(self):
        #抵用券
        self.driver.find_element_by_id("cn.jihaojia:id/coupon_layout").click()
        sleep(4)
        #C1,输入错误抵用券，提示错误信息
        self.driver.find_element_by_id("cn.jihaojia:id/input_recommendcode").send_keys("122")
        self.driver.find_element_by_id("cn.jihaojia:id/dialog_button_ok").click()
        if "兑换码错误" in self.driver.find_element_by_id("cn.jihaojia:id/txt_title").text :
            self.assertEqual(1,1,"OK，提示信息显示正确")
        else :
            self.assertEqual(1,0,"Err，抵用券提示信息显示错误！！！")
        sleep(2)
        self.driver.find_element_by_id("cn.jihaojia:id/btn_pos").click()

        #输入正确抵用券 ，未做？？？
        sleep(4)
        #回退
        self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()

    @unittest.skip("已完成 常用联系人地址")
    def test5_3_Address(self):
         #常用联系人地址
         sleep(3)
         self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
         sleep(2)
         self.driver.find_element_by_id("cn.jihaojia:id/address").click()

         #C1,新增地址，获取常用地址个数，如果个数小4个则循环新增，直到大于等于4个
         AddressNums=self.driver.find_elements_by_id("cn.jihaojia:id/addres_name")
         AddressCounts=0
         for AddressNum in AddressNums:  #遍历常用地址个数
              AddressCounts=AddressCounts+1
         for i in range(5):
             if AddressCounts < 4:
                  #添加地址，点击+
                  self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click()
                  self.driver.find_element_by_id("cn.jihaojia:id/reciver").send_keys(u"令狐冲")
                  self.driver.find_element_by_id("cn.jihaojia:id/mobile").send_keys("13816109050")
                  self.driver.find_element_by_id("android:id/text1").click()
                  Revtimes=self.driver.find_elements_by_id("android:id/text1")
                  for Revtime in Revtimes:  #周一至周五收货、周六日节假日收货
                      if Revtime.text=="收货时间不限":
                         Revtime.click()
                         break
                  self.driver.find_element_by_id("cn.jihaojia:id/region_layout").click()
                  sleep(2)
                  #红米5.0.2
                  self.driver.swipe(300, 1150, 300, 680, 0); #省 上海
                  self.driver.swipe(500, 1000, 500, 900, 0); #市 上海市内
                  self.driver.swipe(800, 1000, 800, 800, 0); #区 徐汇区
                  sleep(2)
                  self.driver.find_element_by_id("cn.jihaojia:id/btn_pos").click()
                  self.driver.find_element_by_id("cn.jihaojia:id/detail_addres").send_keys(u"上海浦东南路100号")
                  self.driver.find_element_by_id("cn.jihaojia:id/savebtn").click()
                  AddressCounts=AddressCounts+1
             else:
                 break

         #C2,删除地址 默认删除从左到右，从上到下第4个
         self.driver.tap([(800, 1000)], 3000)
         #确定要删除这个地址吗？
         if "确定要删除这个地址吗" in self.driver.find_element_by_id("cn.jihaojia:id/txt_title").text :
            self.assertEqual(1,1,"OK，提示信息显示正确")
         else :
            self.assertEqual(1,0,"Err，提示信息显示错误！！！")
         self.driver.find_element_by_id("cn.jihaojia:id/btn_pos").click()

         #C3,设置默认地址，默认在第一二个之间切换
         XYdict=self.driver.find_element_by_id("cn.jihaojia:id/addres_start").location
         if XYdict.get('x') == 448 :
              self.driver.tap([(800, 500)], 50) #点击第二个地址
              sleep(2)
              self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click() #设为默认
              sleep(2)
              self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
              sleep(3)
              XYdict=self.driver.find_element_by_id("cn.jihaojia:id/addres_start").location
              if XYdict.get('x') != 448 :
                 self.assertEqual(1,1,"OK，默认地址切换正确")
              else :
                 self.assertEqual(1,0,"Err，第二个地址右上角没有默认字样！！！")
         else:
              self.driver.tap([(300, 500)], 50) #点击第一个地址
              sleep(2)
              self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click() #设为默认
              sleep(2)
              self.driver.find_element_by_id("cn.jihaojia:id/backbtncomm").click()
              sleep(3)
              XYdict=self.driver.find_element_by_id("cn.jihaojia:id/addres_start").location
              if XYdict.get('x') != 980 :
                 self.assertEqual(1,1,"OK，默认地址切换正确")
              else :
                 self.assertEqual(1,0,"Err，第一个地址右上角没有默认字样！！！")

    #@unittest.skip("跳过 我的购物车")
    def test5_4_Shopcar(self):
        #我的购物车
        sleep(3)
        self.driver.find_elements_by_id("cn.jihaojia:id/imageview")[4].click()
        sleep(2)
        myshopcars=self.driver.find_elements_by_class_name("android.widget.TextView")
        for myshopcar1 in myshopcars :
            if myshopcar1.text=="我的购物车" :
               myshopcar1.click()
        sleep(2)
        self.ShopCar(1)

    #@unittest.skip("公共 我的购物车")
    def ShopCar(self,goodsqty):
         #购物车
         #遍历选择1个或多个商品
        tmp1 = tmp2 = AllTotal = QJSSglNum = 0
        # #C?,选择所有商品，检查总计单选框为自动选中。 ???总计单选框选中后checked仍然是false （暂停）
        # tmpAllradios=0
        # Allradios=self.driver.find_elements_by_id("cn.jihaojia:id/shopping_checkbox")
        # for Allradio in Allradios:
        #     self.driver.find_elements_by_id("cn.jihaojia:id/shopping_checkbox")[tmpAllradios].click()
        #     sleep(2)
        #     tmpAllradios=tmpAllradios+1
        # sleep(5)
        #print self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_button").get_attribute("checked")
        #C?,反选总计单选框，检查所有商品单选框为全部为反选。(暂停)
        #C?,勾选总计单选框，反选1个商品单选框，检查总计单选框为反选。（暂停）

        for i in range(goodsqty):  #range(2)=0,1
            self.driver.find_elements_by_id("cn.jihaojia:id/shopping_checkbox")[i].click()
            sleep(2)
        #C1,选择商品（1个或多个），验证商品（价格*数量）的总价是否与总计、去结算一致
        #价格
            SinglePrices=self.driver.find_elements_by_id("cn.jihaojia:id/shoping_money")
            for SinglePrice in SinglePrices :
               if tmp1==i :  #累加2个价格之和
                  SglPrs=float(SinglePrice.text.replace("¥",""))
                  #self.assertEqual(float(SinglePrice.text.replace("¥","")),27.6)  #27.6
                  break
               tmp1=tmp1+1
            sleep(2)
        #数量
            SingleQtys=self.driver.find_elements_by_id("cn.jihaojia:id/shoping_cart_number")
            for SingleQty in SingleQtys :
                if tmp2==i :
                   SglNum=int(SingleQty.text)
                   #self.assertEqual(int(SingleQty.text),5)  #5
                   break
                tmp2=tmp2+1
            sleep(2)
        #所有商品累加价格验证
            ShopCarMoney=self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_money").text
            SglTotal = SglPrs * SglNum
            AllTotal = AllTotal + SglTotal
            QJSSglNum = QJSSglNum + SglNum

        self.assertEqual(float(ShopCarMoney.replace("¥","")),round(AllTotal,2))

        #去结算
        QJSNums=self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_pay").text
        tmp111=int(QJSNums.replace("去结算(","").replace(")",""))
        self.assertEqual(tmp111,QJSSglNum)
        self.driver.find_element_by_id("cn.jihaojia:id/shoping_cart_pay").click()

        #C2,切换默认地址，验证地址是否及时更新
        self.driver.find_element_by_id("cn.jihaojia:id/iv_indext").click()
        #常用地址 - 管理页面
        XYdict1=self.driver.find_element_by_id("cn.jihaojia:id/addres_start").location #默认
        if XYdict1.get('x') == 448 :
              sleep(2)
              tmp5=0
              t1s=self.driver.find_elements_by_id("cn.jihaojia:id/addres_consignee") #收货人
              for t1 in t1s:
                  if tmp5==1:
                      tt1=t1.text
                      break
                  tmp5=tmp5+1
              tmp5=0
              t2s=self.driver.find_elements_by_id("cn.jihaojia:id/addres_phone") #手机号码
              for t2 in t2s:
                  if tmp5==1:
                      tt2=t2.text
                      break
                  tmp5=tmp5+1
              tmp5=0
              t3s=self.driver.find_elements_by_id("cn.jihaojia:id/addres_province") #所在地区
              for t3 in t3s:
                  if tmp5==1:
                      tt3=t3.text
                      break
                  tmp5=tmp5+1
              tmp5=0
              t4s=self.driver.find_elements_by_id("cn.jihaojia:id/addres_specifically") #详细地址
              for t4 in t4s:
                  if tmp5==1:
                      tt4=t4.text
                      break
                  tmp5=tmp5+1
              tmp5=0
              t5s=self.driver.find_elements_by_id("cn.jihaojia:id/deliveryTime") #收货时间
              for t5 in t5s:
                  if tmp5==1:
                      tt5=t5.text
                      break
                  tmp5=tmp5+1
              self.driver.tap([(800, 500)], 50) #点击第二个地址
              sleep(2)
              #验证以上5个信息是否及时更新
              self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/Verify_name").text,tt1)
              self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/Verify_phone").text,tt2)
              self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/Verify_add").text,tt3)
              self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/Verify_adddetail").text,tt4)
              self.assertEqual(self.driver.find_element_by_id("cn.jihaojia:id/Verify_takeTime").text,tt5)
              sleep(111)

        else:
              self.driver.tap([(300, 500)], 50) #点击第一个地址
              sleep(2)

        self.driver.find_element_by_id("cn.jihaojia:id/my_btn").click()  #点击管理

        self.test5_3_Address() #调用常用地址



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
