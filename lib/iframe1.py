# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2017-12-19
# Description: iframe 哪些规则
# ********************************************************************************************************************

'''实例'''

# driver.switch_to.frame(0)     # 1.用frame的index来定位，第一个是0
# driver.switch_to.frame("frame1")  # 2.用id来定位
# driver.switch_to.frame("myframe")  # 3.用name来定位
# driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))  # 4.用WebElement对象来定位

# 2.从frame中切回主文档(switch_to.default_content())


# frameset不用切，frame需层层切！
# frame 有三种标签，分别是 frameset、frame、iframe ；
# frameset 跟其他普通标签没有区别，不会影响到正常的定位，而frame与iframe对selenium定位而言是一样的，selenium有一组方法对frame进行操作。
#
# selenium提供了switch_to.frame()方法来切换frame ， 如：switch_to.frame(reference)
# reference是传入的参数，用来定位frame，可以传入id、name、index以及selenium的WebElement对象，假设有如下HTML代码 index.html：
#
# <html lang="en">
# <head>
#     <title>FrameTest</title>
# </head>
# <body>
# <iframe src="a.html" id="frame1" name="myframe"></iframe>
# </body>
# </html>
#
# driver.switch_to.frame(0)  # 1.用frame的index来定位，第一个是0
# driver.switch_to.frame("frame1")  # 2.用id来定位
# driver.switch_to.frame("myframe")  # 3.用name来定位
# driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))  # 4.用WebElement对象来定位
#
#
# 通常采用id和name就能够解决绝大多数问题。但有时候frame并无这两项属性，则可以用index和WebElement来定位：
#
#     index从0开始，传入整型参数即判定为用index定位，传入str参数则判定为用id/name定位
#     WebElement对象，即用find_element系列方法所取得的对象，我们可以用tag_name、xpath等来定位frame对象
#
# 举个栗子：
#
# <iframe src="myframetest.html" />
# driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains(@src,'myframe')]"))
#
#
#
# 2.从frame中切回主文档(switch_to.default_content())
# 切到frame中之后，我们便不能继续操作主文档的元素，这时如果想操作主文档内容，则需切回主文档。
#

#
# 3.嵌套frame的操作(switch_to.parent_frame())
#
# 有时候我们会遇到嵌套的frame，如下：
#
# <html>
#     <iframe id="frame1">
#         <iframe id="frame2" / >
#     </iframe>
# </html>
#
#
# 1.从主文档切到frame2，一层层切进去
#
# driver.switch_to.frame("frame1")
# driver.switch_to.frame("frame2")
#
#
# 2.从frame2再切回frame1，这里selenium给我们提供了一个方法能够从子frame切回到父frame，而不用我们切回主文档再切进来。
#
# driver.switch_to.parent_frame()  # 如果当前已是主文档，则无效果
#
#
# 有了parent_frame()这个相当于后退的方法，我们可以随意切换不同的frame，随意的跳来跳去了。
#
# 所以只要善用以下三个方法，遇到frame分分钟搞定：
#
# driver.switch_to.frame(reference)
# driver.switch_to.parent_frame()
# driver.switch_to.default_content()
#
