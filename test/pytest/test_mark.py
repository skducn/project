# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2021-9-17
# Description: pytest 全能的mark
# mark功能作用就是灵活的管理和运行测试用例，通过不同的标记实现不同的运行策略，主要用途:
# 标记和分类用例: @pytest.mark.level1
# 标记用例执行顺顺序pytest.mark.run(order=1) (需安装pytest-ordering)
# 标记用例在指定条件下跳过或直接失败 @pytest.mark.skipif()/xfail()
# 标记使用指定fixture(测试准备及清理方法) @pytest.mark.usefixtures()
# 参数化 @pytest.mark.parametrize
# 标记超时时间 @pytest.mark.timeout(60) (需安装pytest-timeout)
# 标记失败重跑次数@pytest.mark.flaky(reruns=5, reruns_delay=1) (需安装pytest-rerunfailures)
# ********************************************************************************************************************
import pytest

# 一、自定义mark标记
# ​标签可是使用在类、方法上，标记的两种方式：
# 1，直接标记类、方法、函数，如：@pytest.mark.标签名
# 2，类属性：pytestmark = [pytest.mark.标签名, pytest.mark.标签名]，需要注意的是属性名称是固定的

# 注册标签名
# 要想运行已经打好标记的函数，还需要对标签名进行注册，告诉pytest有哪些标签，如果不进行注册运行时（pytest的高级版本）可能会报警告让你进行注册。
# 在项目根目录下创建一个pytest.ini文件，格式如下：
# # 注册标签
# markers =
#     qc
#     beta
#     smoke

# 二、skip跳过标记
# 直接跳过： @pytest.mark.skip(reason = “原因”) //这里原因是可选参数
# 条件跳过，即满足某个条件才跳过：@pytest.mark.skipif(a == 1, reason = “原因”)

@pytest.mark.beta  # 类标签
class TestLogin:
    @pytest.mark.qc
    @pytest.mark.beta  # 方法标签
    def test_login(self):
        print("121212")

    db_host = 'localhost'
    @pytest.mark.skip("和现在的需求不符合")  # 不满足当下了，或别人编写的暂时不能删的
    def test_yuz(self):
        pass

    @pytest.mark.skipif(db_host == 'localhost', reason='只测试线上环境，不测试本地环境')
    def test_develop_env(self):
        pass

@pytest.mark.smoke  # 函数标签
def test_register():
    pass

class TestClass:
    # pytestmark的类属性
    pytestmark = [pytest.mark.qc, pytest.mark.beta]  # 标签存放在一个列表



if __name__ == '__main__':
    pytest.main(['-m not qc', "-s", "test_mark.py"])   #  执行不带qc标签的用例，-s表示输出print信息
    # pytest.main(['-m qc and beta', "-s", "test_mark.py"])  # 执行带qc与beta标签的用例
    # pytest.main(['-m qc and beta', "-s"])  # 在当前目录下，执行带qc与beta标签的所有用例

    # 注意：标签名一定要加双引号，单引号是会报错的。