import pytest
from airtest.core.api import *

@pytest.mark.test_2
def test_shopcart(poco):
    '''购物车'''
    pass
    poco("com.yiwang:id/navigation_cart_tv").click()
    print(poco("购物车"))
    print(poco("android.webkit.WebView"))
    poco("购物车").child("android.view.View")[0].child("android.view.View")[1].child("android.view.View").child("android.view.View")[1].child("javascript:;")[0].click()







if __name__ == '__main__':
    args0=[__file__,'-s','--startapp=False','--stopapp=False']
    args1=[__file__,
          '--html=../report/report-9.html',
          '--htmlhead=UI测试用例demo',
          '--jkbuildid=9',
          '--jkjobname=testdemo',
          '--simple-html',
          '--self-contained-html'
          ]
    pytest.main(args0)

    #from poco.drivers.android.uiautomation import AndroidUiautomationPoco
    #poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
