# -*- encoding=utf8 -*-
__author__ = "geqiuli"

from airtest.core.api import *
from airtest.core.api import using
from airtest.cli.parser import cli_setup
# generate html report
from airtest.report.report import simple_report
simple_report(__file__, logpath="E:/mypython/airtest_ui_autotest/logs")

android='02157df271610a1b'
android='46709b100104'
if not cli_setup():
    auto_setup(__file__, logdir="E:/mypython/airtest_ui_autotest/logs", devices=[
            "Android://127.0.0.1:5037/"+android,
    ], project_root="E:/mypython/airtest_ui_autotest/logss")

print('  ST.PROJECT_ROOT: ',ST.PROJECT_ROOT)
ST.PROJECT_ROOT = 'E:\\mypython\\airtest_ui_autotest\\business'
print('    ST.PROJECT_ROOT: ',ST.PROJECT_ROOT)
# 相对路径或绝对路径，确保代码能够找得到即可

using("home_page.air")
using("user_center.air")
import home_page
import user_center


start_app("com.yiwang.fangkuaiyi")
using("home_page.air")
home=home_page.home_init()
#assert home,'首页应加载出来'
assert_not_equal(home, False, '首页应加载出来')
mine=home_page.home_go_mine()
#assert mine,'应切换到 我的 页面'
assert_not_equal(mine, False, '应切换到 我的 页面')


# login=user_center.user_login('testzdauto03','qqq123456',entername='测试终端自动化13')
# #assert login,'应登录成功'
# assert_not_equal(login, False, '应登录成功')
#     from home_page import home_init,home_go_mine
#     home_init()
#     home_go_mine()
#     using("user_center.air")
#     from user_center import user_login
#     user_login('testzdauto03','qqq123456',entername='测试终端自动化03')


stop_app("com.yiwang.fangkuaiyi")




# if __name__=='__main__':
#     start_app("com.yiwang.fangkuaiyi")
#     using("home_page.air")
#     home=home_page.home_init()
#     assert home,'首页应加载出来'
#     home_page.home_go_mine()
#     user_center.user_login('testzdauto03','qqq123456',entername='测试终端自动化03')
# #     from home_page import home_init,home_go_mine
# #     home_init()
# #     home_go_mine()
# #     using("user_center.air")
# #     from user_center import user_login
# #     user_login('testzdauto03','qqq123456',entername='测试终端自动化03')


#     stop_app("com.yiwang.fangkuaiyi")