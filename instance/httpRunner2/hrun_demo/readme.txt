文件目录结构管理:
debugtalk.py 放置在项目根目录下，假设为 PRJ_ROOT_DIR
.env 放置在项目根目录下，路径为 PRJ_ROOT_DIR/.env
接口定义（API）放置在 PRJ_ROOT_DIR/api/ 目录下
测试用例（testcase）放置在 PRJ_ROOT_DIR/testcases/ 目录下
测试用例集（testsuite）文件必须放置在 PRJ_ROOT_DIR/testsuites/ 目录下
data 文件夹：存储参数化文件，或者项目依赖的文件，路径为 PRJ_ROOT_DIR/data/
reports 文件夹：存储 HTML 测试报告，生成路径为 PRJ_ROOT_DIR/reports/


项目脚手架
$ hrun --startproject demo
Start to create new project: demo
CWD: /Users/debugtalk/MyProjects/examples

created folder: demo
created folder: demo/api
created folder: demo/testcases
created folder: demo/testsuites
created folder: demo/reports
created file: demo/debugtalk.py
created file: demo/.env


测试用例分层
https://v2.httprunner.org/prepare/testcase-layer/


测试用例分层详细示例：HttpRunner/tests
https://github.com/HttpRunner/HttpRunner/tree/master/tests


在.env 文件中放置敏感数据信息，存储采用 name=value 的格式
UserName=admin
Password=123456
PROJECT_KEY=ABCDEFGH
同时，.env 文件不应该添加到代码仓库中，建议将 .env 加入到 .gitignore 中。
HttpRunner 运行时，会自动将 .env 文件中的内容加载到运行时（RunTime）的环境变量中，然后在运行时中就可以对环境变量进行读取了。
若需加载其它名称的 .env 文件（例如 production.env），可以采用 --dot-env-path 参数指定文件路径：
$ hrun /path/to/testcase.yml --dot-env-path /path/to/.env --log-level debug
INFO     Loading environment variables from /path/to/.env
DEBUG    Loaded variable: UserName
DEBUG    Loaded variable: Password
DEBUG    Loaded variable: PROJECT_KEY

脚本中引用环境变量
username: ${ENV(UserName)}
password: ${ENV(Password)}

还可以在 debugtalk.py 通过 Python 内置的函数 os.environ 对环境变量进行引用，然后再实现处理逻辑。
例如，若发起请求的密码需要先与密钥进行拼接并生成 MD5，那么就可以在 debugtalk.py 文件中实现如下函数：
import os

def get_encrypt_password():
    raw_passwd = os.environ["Password"]
    PROJECT_KEY = os.environ["PROJECT_KEY"])
    password = (raw_passwd + PROJECT_KEY).encode('ascii')
    return hmac.new(password, hashlib.sha1).hexdigest()

在yaml中引用
username: ${ENV(UserName)}
password: ${get_encrypt_password()}

测试用例运行遇到失败则终止
参考：https://v2.httprunner.org/run-tests/cli/
若希望测试用例在运行过程中，遇到失败时不再继续运行后续用例，则可通过在命令中添加--failfast实现。
$ hrun filepath/testcase.yml --failfast


日志级别，默认info
参考：https://v2.httprunner.org/run-tests/cli/
若需要查看到更详尽的信息，例如请求的参数和响应的详细内容，可以将日志级别设置为DEBUG，即在命令中添加--log-level debug。
$ hrun docs/data/demo-quickstart-6.json --log-level debug


保存详细过程数据
参考：https://v2.httprunner.org/run-tests/cli/
为了方便定位问题，运行测试时可指定 --save-tests 参数，即可将运行过程的中间数据保存为日志文件。
$ hrun docs/data/demo-quickstart-6.json --save-tests

