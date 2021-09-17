# coding: utf-8
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Author     : John
# Date       : 2021/9/16
# Description: pytest  pytest-html（完美html测试报告生成）
# pip3 install -U pytest
# pip install -U pytest-html
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# pytest test_html.py --html=report.html  //运行后生成测试报告（htmlReport）


# # 实例1，执行1个test开头的方法
# 结果：F  ,执行后报错，因为func(3)不返回5。
# # pytest pytest1.py
# def func(x):
#     return x + 1
#
# def test_answer():
#     assert func(3) == 5