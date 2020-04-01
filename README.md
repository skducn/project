# PO封装包

### BasePO()
---

find_element() # 重写元素定位方法

find_elements()

send_keys() # 重写定义send_keys方法

assertTrue
 
assertEqual

assertContain

getError() # 当函数返回error时，获取当前语句行号及错误提示。

check_contain_chinese() # 功能： 判断字符串中是否包含中文符合

inputId

inputIdClear

inputName

inputNameClear

inputXpath

inputXpathClear

inputXpathEnter

inputXpathEnterClear

clickId

clickLinktext

clickLinkstext

clickTagname

clickXpath

clickXpathEnter

clickXpaths

clickXpathsNum # 遍历同一属性的多个click，点击第N个。

clickXpathsTextContain # 遍历路径，点击text中包含某内容的连接。

clickXpathsContain # 遍历路径，点击属性dimAttr中包含某内容的连接。

？clickXpathsXpathTextContain # 遍历路径之路径，点击text中包含某内容的连接。

clickXpathsXpath # 遍历路径之路径

？floatXpath 

？clickXpathRight

getXpathText # 获取路径的文本

getXpathsText  # 获取遍历路径的文本

getXpathsTextPlace  # 获取遍历路径，定位内容在第几个

getXpathsPartTextPlace  # 获取遍历路径，定位内容模糊在第几个

getXpathAttr   # 获取路径属性

getXpathsQty  # 获取遍历路径数量

getXpathsAttr  # 获取遍历路径属性

getXpathsDictTextAttr  # 获取遍历路径字典{文本：属性值}

getLinktextAttr  # 获取连接文本的属性

printLinktextAttr

printIdTagnameText

printIdTagnamesText

printXpathText 

printXpathsText

printXpathAttr

printXpathsAttr

？isCheckbox   # ? 判断是否选中复选框 ，返回 True 或 False

checkboxXpathsClear   # 遍历路径反勾选复选框 （不勾选）

selectIdValue    # 通过Id属性选择值

selectIdText   # 通过Id属性选择文本

selectNameText   # 通过Name属性选择文本

selectNameValue   # 通过Name属性选择值

？selectIdStyle

selectXpathsMenu1Menu2  # 遍历级联菜单（选择一级菜单后再选择二级菜单）

？get_selectNAMEvalue

？get_selectOptionValue

iframeId  # 定位iframe的id

iframeXpath  # 定位iframe的Xpath

? inIframeTopDiv

iframeSwitch # 多个iframe之间切换

iframeQuit  # 退出 iframe

jsExecute # 执行js

jsIdReadonly  # 定位id ，去掉js控件只读属性，一般第三方控件日期

jsNameReadonly  # 定位Name，去掉js控件只读属性，一般第三方控件日期

jsNameDisplay   # 去掉js隐藏属性

? displayBlockID

printColor 

sElementId

isElementName

isElementPartialText

isElementLinkText

isElementXpath

isElementVisibleXpath



### CharPO
---
isContainChinese  判断字符串中是否包含中文

isChinese 判断字符串是否全部是中文



### ColorPO
---
consoleColor  控制台输出各种颜色字体，多个参数颜色间隔开。



### DataPO
---
getRandomName  随机生成中文用户名

getRandomPhone  随机生成手机号码

getRandomIdcard  随机生成身份证号

getRandomNum  随机生成n个数字

getRandomIp  随机生成一个有效IP

getRandomIp2  随机生成一个有效IP2

getRandomContent  从列表中随机获取n个元素

isIdcard  判断是否是有效身份证

getBirthday  从身份证中获取出生年月

getAge  从身份证中获取年龄

getSex  从身份证中获取性别

getSeriesIp  从当前IP地址开始连续生成N个IP

getJsonPath  解析json

md5  用MD5  加密内容

md5Segment  MD5分段加密



### DevicePO
---
getLocalPlatform  获取当前系统平台

getLocalMac  获取本机硬件mac地址

getLocalIp  获取当前IP地址

getLocalName  获取本机电脑名

callCamera   调用当前笔记本摄像头拍照

？installAPK  安装apk

？uninstallAPK  卸载apk




### FilePO
---

#### 1，环境变量

1.1 os.environ.keys() 获取环境变量信息

1.2 os.getenv("JAVA_HOME") 获取环境变量的值

1.3 sys.path.append() 添加路径到系统环境变量

1.4 os.path.expandvars(path)用法


#### 2，路径

2.1 os.getcwd() 获取当前路径（反斜线）

2.2 os.path.dirname(__file__) 获取当前路径

2.3 File_PO.getUpPath() 获取上层目录路径（反斜线）

2.4 File_PO.getUpPathSlash() 获取上层目录路径

2.5 File_PO.getLayerPath("../../") 获取自定义上层目录路径

2.6 File_PO.getChdirPath() 切换路径，影响os.getcwd()

#### 3，目录与文件

3.1 getListDir  获取路径下目录及文件清单（排列顺序按照数字、字符、中文输出
）
3.2 getWalk  获取路径下目录及文件清单（包括路径）

3.3 getListFile 获取文件清单

3.4 os.path.basename 获取路径中的文件名

3.5 getFileSize 获取文件大小（字节数）

3.6 os.path.split 分割路径和文件名

3.7 os.path.splitext 分割文件名和扩展名

3.8 os.path.splitdrive 分割驱动器名和路径（用在windows下）

3.9 os.path.dirname 去掉路径后端文件名或目录（就是os.path.split(path)的第一个元素）

3.10 os.path.join 连接两个或更多的路径名组件

3.11 os.path.commonprefix 获取列表中公共最长路径

3.12 os.path.abspath  获取规范化的绝对路径

3.13 os.path.isabs  判断路径是否是绝对路径

3.14 os.path.isdir  判断路径是否是目录

3.15 os.path.isfile  判断路径是否是文件


#### 4，操作目录文件

4.1 newFolder  新建目录

4.2 newLayerFolder  新建多级目录

4.3 copyFolder  复制目录

4.4 renameFolder  目录改名/移动（先移动，在改名，如重名则原路返回）

4.5 newFile  新建文件

4.6 copyFile  复制文件

4.7 renameFile  文件改名/移动

4.8 delEmptyFolder  删除空目录

4.9 newFolder  递归删除目录

4.10 delFile  删除文件（支持通配符）

4.11 deltreeFolder  强制删除目录

4.12  delCascadeFiles  级联删除一个目录下的所有文件，包括子目录下的文件（保留所有子目录，最终保留这个目录架构）



### ListPO
---

listSplitArray  一个列表拆分成N个数组

listSplitSubList  一个列表拆分成N个子列表

listJointChar 列表合并字符串元素

listReplace  替换列表内容

listAlignKey  键值对齐

listKeyValueDict  列表转字典(列表形式符合字典要求key:value)

listBorderDict  列表合并成字典(列表中相邻两元素组成键值对队)

list2MergeDict  两列表合成一个字典



### WebPO
---
dbDesc  查看数据库表结构

dbRecord  搜索表记录

dbCreateDate  查表的创建时间及区间




###  NetPO
---

sendEmail  发邮件

getURLCode  获取网站statuscode

getHeaders  获取网站的header

getHtml  # 获取网站内容

downloadProgram  下载程序

downloadFile 下载html，图片, css 等单个文件



###  TimePO
---

getDate())  # 20190919

getDate_minus())  # 2019-09-19

getDate_divide())  # 2019/03/19

getDatetime())  # 20200319151928

getDatetime_divide())  # 2020/03/19 15:19:28

getDatetimeEditHour(0))  # 2020-03-19 15:35:55

getDatetimeEditHour(0.5))  # 2020-03-19 15:49:28  //晚30分钟

getDatetimeEditHour(-1))  # 2020-03-19 14:19:28   //早1小时

getNow())  # 2019-09-19 17:50:10.470652

getNowEditHour(0.5))  # 2019-09-19 18:20:10.470652  //晚半小时

getNowEditHour(-0.5))  # 2019-09-19 17:20:10.470652  //早半小时

getYear())  # 2019

getMonth())  # 09

getDay())  # 19

getYearMonth())  # 200919

getMonthDay())  # 0919

getWeekday())  # 星期日

now2timestamp())  # 1584603355.0

datetime2timestamp(Time_PO.getDatetimeEditHour(0)))  # 1584603355   //日期时间转时间戳

timestamp2datetime(Time_PO.now2timestamp()))  # 2020-03-19 15:35:55  //时间戳转日期时间

get_day_of_day(20))  # 2019-10-09  //20天后

get_day_of_day(-3))  # 2019-09-16  //3天前

get_days_of_month(2019, 2))  # 28   //2019年2月的天数

get_firstday_of_month(2019, 7))  # 2019-07-01  //返回某年某月的第一天

get_lastday_of_month(2019, 7))  # 2019-07-31  //返回某年某月的最后一天

get_firstday_month(-2))  # 2020-01-01  //返回n月前/后的第一天。

get_lastday_month(-1))   # 2020-02-29  //返回n月前/后的最后一天。

get_lastday_month(2))   # 2020-05-31   //返回n月前/月后的最后一天。

getDate_tuple(1))  # ('2020', '04', '30')    //列表形式返回下个月及最后一天

addzero(9))  # 09    //自动在 1 - 9 前加上0

get_today_month(-1))  # 2020-02-19   //返回上个月的今天

get_today_month(3))  # 2020-06-19   //返回3个月后的今天




### WebPO
---
openURL

closeURL

getScreenWidthHeight  获取当前屏幕分辨率

getFullScreen  截取全屏

getBrowserScreen  截取浏览器内屏幕(因此要打开浏览器后才能截图)

scrollLeft

scrollTop

scrollDown

scrollIntoView

scrollTopById

getCode  获取验证码

populAlert()  弹出框操作
















