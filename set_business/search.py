'''
Created on 2019年8月2日

@author: geqiuli
'''
from airtest.core.api import *
#from set_element.home import *
auto_setup(__file__, logdir="E:\\airtest_proj\\airtest_ui_autotest\\logs", project_root="E:\\airtest_proj\\airtest_ui_autotest")


f=exists(Template(r"tpl1564997336781.png", record_pos=(-0.392, 0.806), resolution=(1080, 1920)))
print(f)

# def home_init():
#     '''首页-等待加载'''
#     #start_app("com.yiwang.fangkuaiyi")

#     wait(bottom_home_active,timeout=10)
#     return exists(bottom_home_active)

if __name__ == '__main__':
    #connect_device('Android:///') #android:/// or Android://127.0.0.1:5037/YOUR_UUID
    # YOUR CODES .....
    print('main')
    

    #home_init()