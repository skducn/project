# coding: utf-8
import pytest
@pytest.fixture(scope='function')
def setup_function(request):
    def teardown_function():
        print("teardown_function called!")
    request.addfinalizer(teardown_function)
    print("\nsetup_function called!")

@pytest.fixture(scope='module')
def setup_module(request):
    def teardown_module():
        print("teardown_module called!")
    request.addfinalizer(teardown_module)
    print("setup_module called!")

def test_1(setup_function):
    print("test_1 called!")

def test_2(setup_module):
    print("test_2 called!")
    assert 4 == 41

def test_3(setup_module):
    print("test_3 called!")
    assert 4 == 41

def test_4(setup_function):
    print("test_4 called!")

# def test1():
#     print('test_numbers_3_4  <============================ actual test code')
#     assert 3 * 4 == 12
#
# def test4():
#     print('test_strings_a_3  <============================ actual test code')
#     assert 4 == 44
#
# def test2():
#     print('test_strings_a_3  <============================ actual test code')
#     assert 4 == 4
#
# def test3():
#     print( 'test_strings_a_3  <============================ actual test code')
#     assert 4 == 4

