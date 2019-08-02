# -*- encoding=utf8 -*-
from airtest.core.api import *
from airtest.core.api import using
from airtest.cli.parser import cli_setup
# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath="E:/mypython/airtest_ui_autotest/logs")
android='46709b100104'
auto_setup(__file__, logdir="E:/mypython/airtest_ui_autotest/logs",
           devices=["Android://127.0.0.1:5037/"+android,]
           )
ST.PROJECT_ROOT = "E:/mypython/airtest_ui_autotest/business/"
# test1.air的实际路径为/User/test/project/test1.air
using("home_page.air")
import home_page1 as h

# import imp
# #h=imp.load_package('home_page.air', r'E:\mypython\airtest_ui_autotest\business\home_page.air\home_page.py')
# h=imp.load_source('home_page.py', r'E:\mypython\airtest_ui_autotest\business\home_page.air\home_page.py')
# print(h.__file__)
# print(h.__author__)

home=h.home_init()
#assert home,'首页应加载出来'
assert_not_equal(home, False, '首页应加载出来')
mine=h.home_go_mine()
#assert mine,'应切换到 我的 页面'
assert_not_equal(mine, False, '应切换到 我的 页面')


if __name__ == '__main__':
    print(' __main__')
    