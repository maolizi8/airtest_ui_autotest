# -*- encoding=utf8 -*-
'''
Created on 2019-08-02

@author: geqiuli
'''
from airtest.core.api import *
from airtest.cli.parser import cli_setup
auto_setup(__file__)
# if not cli_setup():
#     auto_setup(__file__, logdir=False, devices=[
#             "Android:///",
#     ])


# script content
print("start...")


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)
if __name__ == '__main__':
    connect_device('Android:///') #android:/// or Android://127.0.0.1:5037/YOUR_UUID
    # YOUR CODES .....
    print('main')
    f=exists(Template(r"tpl1563958466577.png", record_pos=(-0.391, 0.815), resolution=(1080, 1920)))
    print(f)
