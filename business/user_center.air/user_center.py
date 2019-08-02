# -*- encoding=utf8 -*-
__author__ = "geqiuli"

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


auto_setup(__file__)

def user_login_status():
    '''用户是否登录'''
    return exists(Template(r"tpl1564631443501.png", record_pos=(-0.181, -0.657), resolution=(1440, 2560)))

def user_login(username,password,entername=''):
    '''使用指定账号登录'''
    poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=True)
    if user_login_status():
        print('用户未登录')
        touch(Template(r"tpl1564631549220.png", record_pos=(-0.167, -0.657), resolution=(1440, 2560)))
        
        
        i=0
        while i<2:
            i+=1
            if exists(Template(r"tpl1564631746019.png", record_pos=(0.316, -0.105), resolution=(1440, 2560))):
                touch(Template(r"tpl1564631768000.png", record_pos=(0.316, -0.103), resolution=(1440, 2560)))
            

        touch(Template(r"tpl1564631848958.png", record_pos=(-0.04, -0.084), resolution=(1440, 2560)))
        text(username)
        touch(Template(r"tpl1564631889124.png", record_pos=(-0.033, 0.034), resolution=(1440, 2560)))
        text(password)
        touch(Template(r"tpl1564632316729.png", record_pos=(0.009, 0.378), resolution=(1440, 2560)))

    else:
        login_enter=poco("com.yiwang.fangkuaiyi:id/company_name").get_text()
        print('已有用户登录: ',login_enter)



        if entername == login_enter:
            print('已登录用户与需要登录的用户一致，不需要退出')
        else:
            print('已登录用户与需要登录的用户不一致，需要退出')
    return True    
            





    
