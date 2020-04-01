# project - PO封装包

=====================================
BasePO()

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
isElementText
isElementXpath
isElementVisibleXpath

========================================
WebPO

openURL
closeURL
getScreenWidthHeight 获取当前屏幕分辨率
getFullScreen 截取全屏
getBrowserScreen 截取浏览器内屏幕(因此要打开浏览器后才能截图)
scrollLeft
scrollTop
scrollDown
scrollIntoView
scrollTopById
getCode  获取验证码
populAlert()  弹出框操作

========================================
NetPO

sendEmail
getURLCode
getHeaders
getHtml
getJsonPath
downloadFile
downloadHtml
downloadImage

========================================
FilePO

# 1，环境变量
1.1 os.environ.keys() 获取环境变量信息
1.2 os.getenv("JAVA_HOME") 获取环境变量的值
1.3 sys.path.append() 添加路径到系统环境变量
1.4 os.path.expandvars(path)用法

# 2，路径
2.1 os.getcwd() 获取当前路径（反斜线）
2.2 os.path.dirname(__file__) 获取当前路径
2.3 File_PO.getUpPath() 获取上层目录路径（反斜线）
2.4 File_PO.getUpPathSlash() 获取上层目录路径
2.5 File_PO.getLayerPath("../../") 获取自定义上层目录路径
2.6 File_PO.getChdirPath() 切换路径，影响os.getcwd()

 # 3，目录与文件
3.1 getListDir  获取路径下目录及文件清单（排列顺序按照数字、字符、中文输出）
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

# 4，操作目录文件
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





























