# -*- encoding=utf8 -*-
__author__ = "geqiuli"

# from airtest.core.api import *

# auto_setup(__file__)
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

poco = AndroidUiautomationPoco()

poco("com.yiwang.fangkuaiyi:id/tabhost").offspring("android:id/tabs").child("android.widget.LinearLayout")[2].offspring("com.yiwang.fangkuaiyi:id/iv_icon").click(desc='店铺馆')
poco("com.yiwang.fangkuaiyi:id/search_box").click()
poco("com.yiwang.fangkuaiyi:id/seek_type_iv").click()
poco("com.yiwang.fangkuaiyi:id/pop_store_tv").click()
poco("com.yiwang.fangkuaiyi:id/seek_content_et").click()
poco(text="广东").click()
poco("com.yiwang.fangkuaiyi:id/title_back").click()
poco("com.yiwang.fangkuaiyi:id/seek_cancel_tv").click()
poco("com.yiwang.fangkuaiyi:id/drawer_layout").offspring("com.yiwang.fangkuaiyi:id/seek_store_product").offspring("com.yiwang.fangkuaiyi:id/shop_recyclerview").child("android.widget.LinearLayout")[0].offspring("com.yiwang.fangkuaiyi:id/shop_info_layout").offspring("com.yiwang.fangkuaiyi:id/shop_icon").click()
poco("com.yiwang.fangkuaiyi:id/new_shop_back_img").click()
poco(text="广东壹号药业有限公司").click()
poco("com.yiwang.fangkuaiyi:id/product_number").click()
poco("com.yiwang.fangkuaiyi:id/back_btn").click()
poco(text="全部商品").click()
poco("com.yiwang.fangkuaiyi:id/total_count_tv").click()
