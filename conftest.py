'''
Created on 2019年8月1日

@author: geqiuli
'''
import pytest
import os
from py.xml import html #html的错误提示请忽略
from datetime import datetime
import io
import json
import argparse
import copy
from datetime import datetime
import os
import io
import pytest
from localplugins.simplehtml import store_run_collections,update_run_collections
from localplugins.simplehtml import HTMLReport
from airtest.core.api import connect_device,start_app,stop_app,ST

#import logging
#LOGGER = logging.getLogger(__name__)

PROJ_ROOT = os.path.dirname(os.path.abspath(__file__))
print('conftest - PROJ_ROOT :',PROJ_ROOT)

APP_PACKAGE = 'com.yiwang.fangkuaiyi'
APP_ACTIVITY = 'com.yhyc.mvp.ui.LoadingActivity'

def pytest_addoption(parser):
    '''命令行参数'''
    parser.addoption("--devices", action="store", default='Android:///',
                     help="udid of the device to run scripts")
    parser.addoption("--uuid", action="store", 
                     help="udid of the device to run scripts")
    parser.addoption("--adbport", action="store", default=5037,
                     help="port of adb server")
    parser.addoption("--startapp", action="store", default=True,
                     help="determaine wether start app or not")
    parser.addoption("--stopapp", action="store", default=True,
                     help="determaine wether stop app or not")
    
    parser.addoption("--username", action="store", 
                     help="the username to login in")
    parser.addoption("--password", action="store", 
                     help="the password to login in")
    parser.addoption("--exc_env", action="store", default='test',
                     help="the environment to run case")
    
    group = parser.getgroup('terminal reporting')
    group.addoption('--htmlhead', action='store', dest='htmlhead',default='测试报告',
                    help='the head of html report.')
    group.addoption('--simple-html', action='store_true',
                    help='use simple html moudle.')
    group.addoption('--jkbuildid', action='store',default=-1,
                    help='jenkins buildid, to make online html report.')
    group.addoption('--jkjobname', action='store',
                    help='jenkins jobname, to make online html report.')

def read_json(file_name, subdir=""):
    if subdir:
        fpath=os.sep.join([PROJ_ROOT, "files", subdir, file_name]) + ".json"
    else:
        fpath=os.sep.join([PROJ_ROOT, "files", file_name]) + ".json"
    json_content={}    
    with open(fpath, "r", encoding="utf-8") as f:
        json_content = json.loads(f.read())
    return json_content

@pytest.fixture(scope="session")
def driver_class(request):
    ST.LOG_DIR=os.path.join(PROJ_ROOT,'log')
    devices = request.config.getoption("devices")
    print()
    print("conftest: device_session")
    device_session=connect_device(devices)
    print('conftest: ',device_session)
    return device_session

@pytest.fixture
def air_dr(request,driver_class):
    """Returns a WebDriver instance based on options and capabilities"""
    print('    request: ',request)
    startapp = request.config.getoption("startapp")
    if startapp:
        print('conftest: start app')
        start_app(APP_PACKAGE)
    yield driver_class
    stopapp = request.config.getoption("stopapp")
    if stopapp:
        stop_app(APP_PACKAGE)
        print()
        print('conftest: stop app')

@pytest.fixture
def startapp(request):
    '''用例teardown：是否重新打开app'''
    return request.config.getoption("startapp")

@pytest.fixture
def stopapp(request):
    '''用例teardown：是否关闭app'''
    return request.config.getoption("stopapp")

@pytest.fixture
def username(request):
    '''命令行输入用例的用户名'''
    return request.config.getoption("username")

@pytest.fixture
def password(request):
    '''命令行输入用例的密码'''
    return request.config.getoption("password")

@pytest.fixture
def account(request):
    '''命令行输入username，读取账号密码'''
    username=request.config.getoption("username")
    password=request.config.getoption("password")
    if password:
        print('use specific password')
        return {"uname": username,"upwd": password}
    else:
        print('use stored password from file')
        exc_env=request.config.getoption("exc_env")
        if exc_env in ['prd','PRD','prOd','PROD','product','PRODUCT']:
            user_account=read_json('account_list','prod_env')
        else:
            user_account=read_json('account_list','test_env')
        return {"uname": username,"upwd": user_account[username]}

@pytest.fixture
def exc_env(request):
    '''命令行输入用例运行的环境: prd-生产环境，test-测试环境'''
    return request.config.getoption("exc_env")

def pytest_configure(config):
    htmlpath = config.getoption('htmlpath')
    htmlhead = config.getoption('htmlhead')
    is_simplehtml = config.getoption('--simple-html')
    
    if htmlpath and is_simplehtml:
        for csspath in config.getoption('css') or []:
            open(csspath)
        if not hasattr(config, 'slaveinput'):
            config._html = HTMLReport(htmlpath, config, htmlhead)
            config.pluginmanager.register(config._html)


def pytest_unconfigure(config):
    html = getattr(config, '_html', None)
    if html:
        del config._html
        config.pluginmanager.unregister(html)
        
'''测试报告'''            
def _gather_driver_log(item, summary, extra):
    pytest_html = item.config.pluginmanager.getplugin('html')
    if hasattr(item.config, '_driver_log') and \
       os.path.exists(item.config._driver_log):
        if pytest_html is not None:
            with io.open(item.config._driver_log, 'r', encoding='utf8') as f:
                extra.append(pytest_html.extras.text(f.read(), 'Driver Log'))
            summary.append('Driver log: {0}'.format(item.config._driver_log))
            
# def _gather_screenshot(item, report, driver, summary, extra):
#     try:
#         #截图前先切回原生： NATIVE_APP
#         pre_context=driver.current_context
#         if pre_context!='NATIVE_APP':
#             driver.switch_to.context('NATIVE_APP')
#         screenshot = driver.get_screenshot_as_base64()
#         
#         if pre_context!='NATIVE_APP':
#             driver.switch_to.context(pre_context)
#     except Exception as e:
#         summary.append('WARNING: Failed to gather screenshot: {0}'.format(e))
#         return
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     if pytest_html is not None:
#         # add screenshot to the html report
#         extra.append(pytest_html.extras.image(screenshot, 'Screenshot'))
# 
# def _gather_html(item, report, driver, summary, extra):
#     try:
#         html = driver.page_source
#     except Exception as e:
#         summary.append('WARNING: Failed to gather HTML: {0}'.format(e))
#         return
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     if pytest_html is not None:
#         # add page source to the html report
#         extra.append(pytest_html.extras.text(html, 'HTML'))
# 
# def format_log(log):
#     timestamp_format = '%Y-%m-%d %H:%M:%S.%f'
#     entries = [u'{0} {1[level]} - {1[message]}'.format(
#         datetime.utcfromtimestamp(entry['timestamp'] / 1000.0).strftime(
#             timestamp_format), entry).rstrip() for entry in log]
#     log = '\n'.join(entries)
#     return log
# 
# def _gather_logs(item, report, driver, summary, extra):
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     try:
#         types = driver.log_types
#     except Exception as e:
#         # note that some drivers may not implement log types
#         summary.append('WARNING: Failed to gather log types: {0}'.format(e))
#         return
#     for name in types:
#         try:
#             log = driver.get_log(name)
#         except Exception as e:
#             summary.append('WARNING: Failed to gather {0} log: {1}'.format(
#                 name, e))
#             return
#         if pytest_html is not None:
#             extra.append(pytest_html.extras.text(
#                 format_log(log), '%s Log' % name.title()))

                 
def pytest_collection_finish(session):
    print('----pytest_collection_finish--------')
    store_run_collections(session)


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    summary = []
    extra = getattr(report, 'extra', [])
    
    driver=None
    if 'app_driver' in item.funcargs:
        driver = item.funcargs['app_driver']
        
    xfail = hasattr(report, 'wasxfail')
    failure = (report.skipped and xfail) or (report.failed and not xfail)
    when = item.config.getini('selenium_capture_debug').lower()
    capture_debug = when == 'always' or (when == 'failure' and failure)
    
    
    if capture_debug:
        exclude = item.config.getini('selenium_exclude_debug').lower()
        if 'logs' not in exclude:
            # gather logs that do not depend on a driver instance
            _gather_driver_log(item, summary, extra)
        #print('--------------driver--------------')
        #print(driver)
#         if driver is not None:
#             # gather debug that depends on a driver instance
#             if 'screenshot' not in exclude:
#                 _gather_screenshot(item, report, driver, summary, extra)
#             #if 'html' not in exclude:
#             #    _gather_html(item, report, driver, summary, extra)
#             #if 'logs' not in exclude:
#             #    _gather_logs(item, report, driver, summary, extra)

    if summary:
        report.sections.append(('pytest-appdriver', '\n'.join(summary)))
    report.extra = extra
    
    update_run_collections(item, call, report)
    
    