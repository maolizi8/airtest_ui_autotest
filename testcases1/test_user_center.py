# -*- encoding=utf8 -*-
__author__ = "geqiuli"
import pytest
# from airtest.core.api import *
# from airtest.core.api import using

# ST.PROJECT_ROOT = 'E:\\mypython\\airtest_ui_autotest\\business'
# print('    ST.PROJECT_ROOT: ',ST.PROJECT_ROOT)

# using("home_page.air")
# using("user_center.air")
from business.home_tab import home_page
#from business import user_center


# from airtest.cli.parser import cli_setup
# 
# if not cli_setup():
#     auto_setup(__file__, logdir=True, devices=[
#             "Android://127.0.0.1:5037/02157df271610a1b",
#     ])
# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)

@pytest.mark.test_0
def test_go_to_mine(air_dr):
    #print(air_dr)
    #print('test_go_to_mine>  ST.PROJECT_ROOT: ',ST.PROJECT_ROOT)
    home=home_page.home_init()
    assert home,'首页应加载出来'
    #assert_not_equal(home, False, '首页应加载出来')
    mine=home_page.home_go_mine()
    assert mine,'应切换到 我的 页面'
    #assert_not_equal(mine, False, '应切换到 我的 页面')
    
#     login=user_center.user_login('testzdauto03','qqq123456',entername='测试终端自动化13')
#     #assert login,'应登录成功'
#     assert_not_equal(login, False, '应登录成功')

@pytest.mark.test_0
def test_go_to_mine2(air_dr):
    #print(air_dr)
    #print('test_go_to_mine>  ST.PROJECT_ROOT: ',ST.PROJECT_ROOT)
    home=home_page.home_init()
    assert home,'首页应加载出来'
    #assert_not_equal(home, False, '首页应加载出来')
    mine=home_page.home_go_mine()
    assert mine,'应切换到 我的 页面'
    #assert_not_equal(mine, False, '应切换到 我的 页面')
    
#     login=user_center.user_login('testzdauto03','qqq123456',entername='测试终端自动化13')
#     #assert login,'应登录成功'
#     assert_not_equal(login, False, '应登录成功')   
 
if __name__ == '__main__':
    args=[__file__,'-s','--html=../../reports/report.html']
    pytest.main(args)