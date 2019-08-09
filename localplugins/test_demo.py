'''
Created on 8 May 2019

@author: geqiuli
'''
import pytest
from time import sleep

# def test_demo_01(selenium):
#     '''打开百度页面1'''
#     selenium.get('https://www.baidu.com')
#     sleep(2)
#     print('page title:',selenium.title)
#     assert '百度' in selenium.title
    
# def test_demo_02(selenium):
#     '''打开百度页面2'''
#     selenium.get('https://www.baidu.com')
#     sleep(2)
#     print('页面标题:',selenium.title)
#     selenium.find_element_by_id('kkkkk')

# def test_demo_03():
#     '''过滤的用例1'''
#     print('----打印跳过demo03----')
#     pytest.skip('test skip') 
#     print('----被跳过的用例，不会执行此句----')

def test_demo_03(air_dr):
    '''用例3'''
    print('----测试失败的用例，中文----')
    print(r'D:\test_autotest\AutoTest\testenv_case')
    print('D:\\test_autotest\\AutoTest\\testenv_case')
    sleep(1)
    assert 1==1,'1==1！！'
    
def test_demo_04(air_dr):
    '''失败的用例4'''
    print('----测试失败的用例，中文----')
    print(r'D:\test_autotest\AutoTest\testenv_case')
    print('D:\\test_autotest\\AutoTest\\testenv_case')
    assert 1==2,'1竟然不等于2！！'

if __name__ == '__main__' :
    
    args=[__file__,
          #'-s'
          #'--driver=Chrome',
          '--html=../reports/report-6.html',
          '--htmlhead=UI测试用例demo',
          '--jkbuildid=6',
          '--jkjobname=testdemo',
          '--simple-html',
          '--self-contained-html'
          ]
    pytest.main(args)