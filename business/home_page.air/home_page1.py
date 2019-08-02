# -*- encoding=utf8 -*-
__author__ = "geqiuli"

from airtest.core.api import *

auto_setup(__file__)

def home_init():
    '''首页-等待加载'''
    #start_app("com.yiwang.fangkuaiyi")

    wait(Template(r"tpl1563958466577.png", record_pos=(-0.391, 0.815), resolution=(1080, 1920)),timeout=10)
    return exists(Template(r"tpl1563958466577.png", record_pos=(-0.391, 0.815), resolution=(1080, 1920)))

def home_go_to_country_hot():
    '''首页-跳转全国热销'''

    touch(Template(r"tpl1564631187238.png", record_pos=(0.228, -0.604), resolution=(1440, 2560)))


    sleep(1)
    return exists(Template(r"tpl1564631204711.png", record_pos=(0.231, -0.608), resolution=(1440, 2560)))

    

def home_go_to_1yaodai():
    '''首页-跳转1药贷'''

    touch(Template(r"tpl1563958531724.png", record_pos=(0.394, -0.091), resolution=(1080, 1920)))

    sleep(1)
    return exists(Template(r"tpl1564631268298.png", record_pos=(0.019, -0.136), resolution=(1440, 2560)))

    
def home_go_mine():
    '''首页-跳转 我的'''
    touch(Template(r"tpl1564631351644.png", record_pos=(0.397, 0.817), resolution=(1440, 2560)))
    sleep(1)
    return exists(Template(r"tpl1564631396373.png", record_pos=(0.397, 0.809), resolution=(1440, 2560)))

    
if __name__ == '__main__':
    connect_device('Android:///')
    start_app("com.yiwang.fangkuaiyi")
    f=home_init()
    print(f)
    stop_app("com.yiwang.fangkuaiyi")

