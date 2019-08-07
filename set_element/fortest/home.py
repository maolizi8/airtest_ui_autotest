# -*- encoding=utf8 -*-
"""
Created on 2019-08-05

@author: geqiuli
"""
from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=None, devices=[
            "Android:///",
    ])


# your script content
print("start...")

print('首页被选中： ',exists(Template(r"tpl1564987080585.png", record_pos=(-0.39, 0.805), resolution=(1080, 1920))))
print('首页未被选中： ',exists(Template(r"tpl1564987124719.png", record_pos=(-0.394, 0.808), resolution=(1080, 1920))))



# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=None)

if __name__ == '__main__':
    connect_device('Android:///') #android:/// or Android://127.0.0.1:5037/YOUR_UUID
    # YOUR CODES .....