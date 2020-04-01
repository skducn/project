import pytesseract
from PIL import Image
image = Image.open('code3.png')
code = pytesseract.image_to_string(image)
print code


   def screenWidthHeight(self,rightCornerPicID):
        # self.screenWidthHeight("com.mowin.tsz:id/my_tab")
        # 获取屏幕右下角图片的长度和高度, 一般是屏幕的长度和高度(1440,2392)
        location =  self.driver.find_element_by_id('captcha').location
        size = self.driver.find_element_by_id('captcha').size
        varWidth = int(location["x"] + size["width"])
        varHeight = int(location["y"] + size["height"])
        return varWidth,varHeight


   def captureCustomScreen(self,imageName,startX, startY, endX, endY):
    # 功能:截取屏幕(自定义范围)   # 如: captureCustomScreen("test.png",0,1080,1,1920)
    self.driver.save_screenshot(imageName)
    box=(startX, startY, endX, endY)
    i = Image.open(imageName)
    newImage = i.crop(box)
    newImage.save(imageName)