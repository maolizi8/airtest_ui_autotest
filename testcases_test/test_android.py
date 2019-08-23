# -*- encoding=utf8 -*-
"""
Created on 2019-08-07

@author: geqiuli
"""
import pytest
from set_business import home_page as h
from set_business import user_center as uc
from airtest.core.api import *

# your functions ...
# @pytest.mark.test_0
# def test_go_to_mine(air_dr):
#     '''首页-进入个人中心'''
#     find,home=h.home_init()
#     assert find,'首页应加载出来'
#     assert_exists(home, msg="首页应加载出来")
#     #assert_not_equal(home, False, '首页应加载出来')
#     mine=h.home_go_mine()
#     assert mine,'应切换到 我的 页面'

@pytest.mark.test_2
def test_login(poco):
    '''个人中心-登录'''
    home=h.home_init()
    assert home,'首页应加载出来'
    #assert_not_equal(home, False, '首页应加载出来')
    mine=h.home_go_mine()
    assert mine,'应切换到 我的 页面'
    name=uc.login_with_account(poco,'testzdauto03','qqq123456',entername='测试终端自动化03')
    assert name=='测试终端自动化03'



if __name__ == '__main__':
    args0=[__file__,'-s']
    args1=[__file__,
          '--html=../report/report-9.html',
          '--htmlhead=UI测试用例demo',
          '--jkbuildid=9',
          '--jkjobname=testdemo',
          '--simple-html',
          '--self-contained-html'
          ]
    pytest.main(args0)