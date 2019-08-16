# -*- encoding=utf8 -*-
'''
Created on 2019-08-02

@author: geqiuli
'''
from airtest.core.api import *
from set_element.home import *


def home_init():
    '''首页-等待加载'''
    #start_app("com.yiwang.fangkuaiyi")
    print('等待首页加载：超时时间=10秒')
    wait(bottom_home_active,timeout=10)
    print('首页已加载')
    return exists(bottom_home_active),bottom_home_active


def home_go_to_1yaodai():
    '''首页-跳转1药贷'''
    touch(menu_1yaodai)
    sleep(1)
    return exists(menu_1yaodai)

    
def home_go_mine():
    '''首页-跳转 我的'''
    touch(bottom_mine_inactive)
    sleep(1)
    return exists(bottom_mine_active)

if __name__ == '__main__':
    auto_setup(__file__, devices=['Android:///'],
                logdir=True)
    #connect_device('Android:///') #android:/// or Android://127.0.0.1:5037/YOUR_UUID
    # YOUR CODES .....
    print('main')
    home_init()
    from airtest.report.report import simple_report
    simple_report(__file__, logpath=True)
