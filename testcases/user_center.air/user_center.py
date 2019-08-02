# -*- encoding=utf8 -*-
__author__ = "geqiuli"

from airtest.core.api import *

auto_setup(__file__)

start_app("com.yiwang.fangkuaiyi")

touch(Template(r"tpl1563949507131.png", record_pos=(0.4, 0.815), resolution=(1080, 1920)))
if exists(Template(r"tpl1563949567559.png", record_pos=(-0.241, -0.683), resolution=(1080, 1920))):
    print('用户已经登录')
    touch(Template(r"tpl1563949652998.png", record_pos=(0.428, -0.748), resolution=(1080, 1920)))
    touch(Template(r"tpl1563949666457.png", record_pos=(0.008, 0.787), resolution=(1080, 1920)))

    assert_exists(Template(r"tpl1563949756180.png", record_pos=(-0.178, -0.66), resolution=(1080, 1920)), "应：未登录状态")

else:
    print('用户未登录')
    assert_exists(Template(r"tpl1563949756180.png", record_pos=(-0.178, -0.66), resolution=(1080, 1920)), "应：未登录状态")


stop_app("com.yiwang.fangkuaiyi")        


    
    

        

