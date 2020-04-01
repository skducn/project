


import sys
from com.android.monkeyrunner import MonkeyRunner,MonkeyDevice,MonkeyImage

device = MonkeyRunner.waitForConnection()
device.reboot('None')

package = 'com.mowin.tsz'
activity='.SplashActivity'
component = package +'/' + activity

device = MonkeyRunner.waitForConnection()
# device.installPackage('~/Downloads/app-sit2-debug.apk')
device.startActivity(component)
MonkeyRunner.sleep(6)
device.touch(1000,1800,'DOWN_AND_UP')

MonkeyRunner.sleep(6)
device.touch(1000,300,'DOWN_AND_UP')


MonkeyRunner.sleep(6)
device.touch(200,1300,'DOWN_AND_UP')

MonkeyRunner.sleep(6)
device.touch(400,300,'DOWN_AND_UP')

qq = MonkeyRunner.input('please input qq:','6678','bugben','save','cancel')
MonkeyRunner.alert(qq,'bugben','save')

device.touch(500,300,'DOWN_AND_UP')
device.type(qq)

