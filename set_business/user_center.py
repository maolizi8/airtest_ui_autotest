# -*- encoding=utf8 -*-
"""
Created on 2019-08-06

@author: geqiuli
"""
from set_element.mine import *
from airtest.core.api import *


# your script content
def login_without_check(poco,username,password,entername=''):
    '''登录，前提：未登录状态'''
    
    poco("com.yiwang.fangkuaiyi:id/user_login_btn").click()
    del_name=poco("com.yiwang.fangkuaiyi:id/del_name")
    if del_name:
        del_name.click()
    poco("com.yiwang.fangkuaiyi:id/user_name").click()
    text(username)
    del_pwd=poco("com.yiwang.fangkuaiyi:id/del_pwd")
    if del_pwd:
        del_pwd.click()
    poco("com.yiwang.fangkuaiyi:id/user_pwd").click()
    text(password)
    poco("com.yiwang.fangkuaiyi:id/login_btn").click()
    sleep(1)
    display_name=poco("com.yiwang.fangkuaiyi:id/company_name").get_text()
    print('登录完成，显示名称为：',display_name)
    return display_name

def login_with_account(poco,username,password,entername=''):
    '''登录：未登录-则登录；已登录则判断后退出重登或结束'''
    #poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=True)
    if exists(login_and_register):
        print('用户未登录，先登录')
        return login_without_check(poco,username,password,entername)
        
    else:
        display_name=poco("com.yiwang.fangkuaiyi:id/company_name").get_text()
        print('已登录状态，显示名称为：',display_name)
        if display_name!=entername:
            print('已登录用户与预期用户不一致，先退出，重新登录')
            poco("com.yiwang.fangkuaiyi:id/setting").click()
            poco("com.yiwang.fangkuaiyi:id/logout_btn").click()
            sleep(1)
            return login_without_check(poco,username,password,entername)
        else:
            return display_name
    
def go_to_all_order_list():
    ''''''
    poco(text="查看全部订单").click()

    

if __name__ == '__main__':
    #if not cli_setup():
    auto_setup(__file__, devices=[
            "Android://127.0.0.1:5037/46709b100104",
    ], logdir=True)
    from poco.drivers.android.uiautomation import AndroidUiautomationPoco
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=True)
    # YOUR CODES .....
    login_with_account(poco,'xxxx','xxxxx',entername='xxxxx')
    #go_to_all_order_list()
    
    # generate html report, put this in the bottom
    from airtest.report.report import simple_report
    simple_report(__file__, logpath=True)
    

    
