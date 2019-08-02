# -*- encoding=utf8 -*-
__author__ = "geqiuli"

from airtest.core.api import *

auto_setup(__file__)

start_app("com.yiwang.fangkuaiyi")

wait(Template(r"tpl1563958466577.png", record_pos=(-0.391, 0.815), resolution=(1080, 1920)),timeout=10)

touch(Template(r"tpl1563958531724.png", record_pos=(0.394, -0.091), resolution=(1080, 1920)))

sleep(3)


assert_not_exists(Template(r"tpl1563958562728.png", record_pos=(0.03, -0.054), resolution=(1080, 1920)), "测试 - 错误的校验点")

stop_app("com.yiwang.fangkuaiyi")
