# # coding: utf-8
# # ****************************************************************
# # Author     : John
# # Version    : 1.0.0
# # Date       : 2017-5-5
# # Description: winrm远程连接win服务器，查看或操作文件
# # ****************************************************************
# # pywinrm 0.2.2
# # https://pypi.python.org/pypi/pywinrm
#
# # 前置条件：配置win服务器上的winrm服务。
#
# # Q1:WinRM - the specified credentials were rejected by the server
# # A1:配置服务器，服务器端执行 winrm configSDDL default , 添加登录账号，如Administrator，勾选 full control, read,execute
#
#
# # winrm service 默认都是未启用的状态，先查看状态；如无返回信息，则是没有启动；
# # winrm enumerate winrm/config/listener
# #
# # 针对winrm service 进行基础配置：
# # winrm quickconfig
# #
# # 查看winrm service listener:
# # winrm e winrm/config/listener
# #
# # 为winrm service 配置auth:
# # winrm set winrm/config/service/auth @{Basic="true"}
# #
# # 为windows开启winrm service, 以便进行远程管理
# # 为winrm service 配置加密方式为允许非加密：
# # winrm set winrm/config/service @{AllowUnencrypted="true"}
# #
#
# # 注意：TrustedHosts 列表中的计算机未经过身份验证。
# # 执行以下命令可将所有计算机都纳入TrustedHosts。
# # winrm s winrm/config/Client @{TrustedHosts="*"}
#
# # 执行以下命令能够以每组多达50个实例的速度获取实例。
# # winrm set winrm/config @{MaxBatchItems="50"}
# #
# # 此外，通过增大分配的最大封包大小和超时设置，也可以提高性能。
# # winrm set winrm/config @{MaxEnvelopeSizekb="150"}
# # winrm set winrm/config @{MaxTimeoutms ="60000"}
# #
# # 下面列出了其他可选的WinRM配置命令，以便您参考。要获取当前的WinRM配置设置，请执行以下命令：
# # winrm g winrm/config
#
# # pywinrm安装
# # sudo pip install pywinrm
#
#
#
# import winrm, sys, argparse
#
# s = winrm.Session('http://10.111.3.22:5985/wsman', auth=('Administrator', '1q2w3e$R'))
#
# # 打印服务端目录内容
# r = s.run_ps('dir e:\engine\demo')
# # print r.std_out
# # print r.std_err
# #
# # if "job2_1.01" in r.std_out:
# #     print "ok"
# # else:
# #     print "error "
#
#
# # 执行批处理
# r = s.run_cmd('cd /d e:\\temp & 1.bat')
# print r.std_out
#
# # 打印 服务端网络配置
# # r2 = s.run_cmd('ipconfig', ['/all'])
# # print r2.status_code
# # print r2.std_out
#
# # # 命令行模式多次使用
# def _runCommand(comm):
#     if (comm == "q"):
#         sys.exit()
#     r = s.run_cmd(comm)
#     print r.std_out
#
# while 1:
#     comm = raw_input("command >")
#     _runCommand(comm)
#
#
# # ps_script = """$strComputer = $Host
# # Clear
# # $RAM = WmiObject Win32_ComputerSystem
# # $MB = 1048576
# #
# # "Installed Memory: " + [int]($RAM.TotalPhysicalMemory /$MB) + " MB" """
# #
# # r3 = s.run_ps(ps_script)
# # print r3.status_code
# # print r3.std_out