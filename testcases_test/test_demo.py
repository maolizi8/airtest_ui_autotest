# -*- encoding=utf8 -*-
"""
Created on 2019-08-22

@author: geqiuli
"""

""" Template 1: business funcs """
from airtest.core.api import *
# from set_element.home import *

# your functions ...
def func():
    """
    descriptions
    """
    pass


if __name__ == '__main__':
    auto_setup(__file__, devices=[
            "Android:///",
    ], logdir=True)
    
    # debug codes ...
    func()
    
    # generate html report, put this in the bottom
    # from airtest.report.report import simple_report
    # simple_report(__file__, logpath=True)

    
""" Template 2: testcases"""
import pytest
# from set_business.home_page import *

# your testcases ...
@pytest.mark.test_level_0
def test_func(poco):
    """
    descriptions
    """
    pass

if __name__ == '__main__':
    args=[__file__,'-m test_1','--html=../reports/report.html']
    pytest.main(args)