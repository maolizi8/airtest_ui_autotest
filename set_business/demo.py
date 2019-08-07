# -*- encoding=utf8 -*-
__author__ = "geqiuli"

from airtest.core.api import *
from airtest.cli.parser import cli_setup

auto_setup(__file__,)

if not cli_setup():
    auto_setup(__file__, logdir="E:\\airtest_proj\\airtest_ui_autotest\\logs", devices=[
            "Android:///",
    ])

exists(Template(r"tpl1564721049802.png", record_pos=(-0.391, 0.807), resolution=(1080, 1920)))

# script content
print("start...")
touch(Template(r"tpl1564717731381.png", record_pos=(-0.187, 0.812), resolution=(1080, 1920)))






# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=None)