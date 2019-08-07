# -*- encoding=utf8 -*-
"""
Created on 2019-08-07

@author: geqiuli
"""
import pytest
from airtest.core.api import *
# import your elements, eg. from set_element.home import *
from set_business import home_page as h
from set_business.user_center import *

# your functions ...
@pytest.mark.test_0
def test_go_to_mine(air_dr):
    home=h.home_init()
    assert home,'首页应加载出来'
    #assert_not_equal(home, False, '首页应加载出来')
    mine=h.home_go_mine()
    assert mine,'应切换到 我的 页面'
    




if __name__ == '__main__':
    auto_setup(__file__, devices=[
            "Android:///",
    ], logdir=None)
    
    
    # debug codes ...
    # func()
    
    # generate html report, put this in the bottom
    # from airtest.report.report import simple_report
    # simple_report(__file__, logpath=None)