# -*- encoding=utf8 -*-
"""
Created on 2019-08-07

@author: geqiuli
"""
from airtest.core.api import *
# import your elements, eg.
# from set_element.home import *

# your functions ...
def func():
    """
    descriptions
    """
    pass




if __name__ == '__main__':
    auto_setup(__file__, devices=[
            "Android://127.0.0.1:5037/46709b100104",
    ], logdir=True)
    
    
    # debug codes ...
    # func()
    
    # generate html report, put this in the bottom
    # from airtest.report.report import simple_report
    # simple_report(__file__, logpath=True)