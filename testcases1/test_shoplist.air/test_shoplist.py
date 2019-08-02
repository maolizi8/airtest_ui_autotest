# -*- encoding=utf8 -*-
__author__ = "geqiuli"

from airtest.core.api import *
from airtest.core.api import using
import os

print('  ST.PROJECT_ROOT: ',ST.PROJECT_ROOT)
ST.PROJECT_ROOT = 'E:\\test-androidapp\\airtest_ui_autotest\\business'
print('    ST.PROJECT_ROOT: ',ST.PROJECT_ROOT)
# 相对路径或绝对路径，确保代码能够找得到即可
using("home_page.air")
#using("home_page.air")

#auto_setup(__file__)

from home_page import home_init,go_to_1yaodai
home_init()
go_to_1yaodai()