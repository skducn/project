##########################################################################
## python 包 ， Unofficial Windows Binaries for Python Extension Packages
## http://www.lfd.uci.edu/~gohlke/pythonlibs/#pywin32

##########################################################################
## Web UI 浏览器弹出上传、下载文件
## Selenium 是基于 JavaScript 的库，对于浏览器弹出的上传、下载文件对话框不支持。但在 Windows 操作系统中，可以通过 PyWin32 库操作对话框。
##　当然，对于 <input type="file" />控件，直接通过 send_keys() 即可上传。
## 参考资料：http://stackoverflow.com/questions/17235228/which-is-the-best-way-to-interact-with-already-open-native-os-dialog-boxes-like

# -*- coding: utf-8 -*-
import win32gui,re,SendKeys,time

class WindowFinder:
    """Class to find and make focus on a particular Native OS dialog/Window """
    def __init__ (self):
        self._handle = None
    def find_window(self, class_name, window_name = None):
        """Pass a window class name & window name directly if known to get the window """
        self._handle = win32gui.FindWindow(class_name, window_name)
    def _window_enum_callback(self, hwnd, wildcard):
        '''Call back func which checks each open window and matches the name of window using reg ex'''
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) != None:
            self._handle = hwnd
    def find_window_wildcard(self, wildcard):
        """ This function takes a string as input and calls EnumWindows to enumerate through all open windows """
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)
    def set_foreground(self):
        """Get the focus on the desired open window"""
        win32gui.SetForegroundWindow(self._handle)

def send_keys_to_dialog(title=r".*Upload.*", key_valus=r""):
    win_dialog = WindowFinder()
    win_dialog.find_window_wildcard(title)
    #win_dialog.set_foreground()
    time.sleep(2)
    SendKeys.SendKeys(key_valus)
    SendKeys.SendKeys("{ENTER}")

if __name__ == "__main__":
    send_keys_to_dialog(u"Open", r"E:\documents\Selenium.docx")
    send_keys_to_dialog(u".*文件上传.*","C:\\1\\QQ.png")
##########################################################################
###webdriver下拉框的选择几种方法
#1
driver.find_element_by_id("aaa").find_elements_by_tag_name("option")[1].click();
#2
select=driver.find_element_by_xpath("//select[@id='ShippingMethod']")
select.find_element_by_xpath("//option[@value='8.34']").click()
#3.
from selenium.webdriver.support.ui import Select
select = Select(driver.find_element_by_tag_name("select"))
select.deselect_all()
select.select_by_visible_text("Edam")