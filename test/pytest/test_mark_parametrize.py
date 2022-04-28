# coding: utf-8
# ********************************************************************************************************************
# Author     : John
# Date       : 2020-10-27
# Description: pytest
# 显示安装包版本，pip3 show pytest , 6.1.1
# https://www.jianshu.com/p/b07d897cb10c
# Full pytest documentation   https://docs.pytest.org/en/stable/contents.html#toc
# pytest参数列表，https://www.cnblogs.com/wtfm/p/10824461.html
# ********************************************************************************************************************
import pytest

@pytest.fixture(scope="function")
def start():
    print("------start--------")

names = ["羡鱼", "abc123", "admin@123.com"]
@pytest.mark.usefixtures("start")
@pytest.mark.parametrize("name11", names)
def test_user_reg(name11):  # 接收的变量名要和parametrize的"name11"一致
    print(name11)

# ------start--------
# 羡鱼
# .------start--------
# abc123
# .------start--------
# admin@123.com


if __name__ == '__main__':
    pytest.main(["-s","test_mark_parametrize.py"])