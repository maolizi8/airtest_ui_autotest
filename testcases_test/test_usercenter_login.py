# -*- encoding=utf8 -*-
"""
Created on 2019-08-07

@author: geqiuli
"""
import pytest
from set_business import home_page as h
from set_business import user_center as uc

# your functions ...
@pytest.mark.test_0
def test_go_to_mine(air_dr):
    '''首页-进入个人中心'''
    home=h.home_init()
    assert home,'首页应加载出来'
    #assert_not_equal(home, False, '首页应加载出来')
    mine=h.home_go_mine()
    assert mine,'应切换到 我的 页面'

@pytest.mark.test_1
def test_login(air_dr):
    '''个人中心-登录'''
    home=h.home_init()
    assert home,'首页应加载出来'
    #assert_not_equal(home, False, '首页应加载出来')
    mine=h.home_go_mine()
    assert mine,'应切换到 我的 页面'
    uc.login_with_account('testzdauto03','qqq123456',entername='测试终端自动化03')



if __name__ == '__main__':
    args=[__file__,'-m test_0','--html=../reports/report.html',
          '--jkbuildid=1','--jkjobname=testdemo','--simple-html']
    pytest.main(args)