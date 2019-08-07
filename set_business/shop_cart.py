# -*- encoding=utf8 -*-
"""
Created on 2019-08-06

@author: geqiuli
"""
from airtest.core.api import *
# import your elements
#from set_element.home import *

# your functions ...



# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)

if __name__ == '__main__':
    auto_setup(__file__, devices=[
            "Android://127.0.0.1:5037/46709b100104",
    ], logdir=True)
    # android:/// or Android://127.0.0.1:5037/YOUR_UUID
    # debug codes ...