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
from localplugins.simplehtml import store_run_collections,store_run_cases,update_run_tests
from localplugins.simplehtml import HTMLReport
from airtest.core.api import connect_device,start_app,stop_app,ST
from airtest.core.helper import G, set_logdir

#import logging
#LOGGER = logging.getLogger(__name__)
from localplugins.helper import GL
PROJ_NAME = GL.proj_name
PROJ_ROOT = os.path.dirname(os.path.abspath(__file__))
print('conftest - PROJ_ROOT :',PROJ_ROOT)

APP_PACKAGE = 'com.yiwang.fangkuaiyi'
APP_ACTIVITY = 'com.yhyc.mvp.ui.LoadingActivity'

def pytest_addoption(parser):
    '''命令行参数'''
    parser.addoption("--devices", action="append",  default=[],
                     help="udid of the device to run scripts")
    parser.addoption("--uuid", action="store", 
                     help="udid of the device to run scripts")
    parser.addoption("--adbport", action="store", default=5037,
                     help="port of adb server")
    parser.addoption("--startapp", action="store", default=True,
                     help="determaine wether start app or not")
    parser.addoption("--stopapp", action="store", default=True,
                     help="determaine wether stop app or not")
    
    parser.addoption("--airtestlog", action="store", default=True,
                     help="generate airtest log")
    parser.addoption("--airtesthtml", action="store", default=True,
                     help="generate airtest html")
    
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


@pytest.fixture(scope="session")
def driver_class(request):
    ST.LOG_DIR=os.path.join(PROJ_ROOT,'log')
    devices = request.config.getoption("devices")
    print()
    print("conftest: device_session")
    #device_session=connect_device(devices)
    device_session=[]
    if devices:
        for dev in devices:
            print('    dev: ',dev)
            device_session.append(connect_device(dev))
    else:
        dev = 'Android:///'
        device_session.append(connect_device(dev))
    print('conftest: ',device_session)
    return device_session

@pytest.fixture
def air_dr(request,driver_class):
    """Returns a WebDriver instance based on options and capabilities"""
    #print('    request: ',request)
    dict_list = request.__dict__
    dir_list = dir(request)
#     print('    request.__dict__: ',dict_list)
#     print('    request dir: ',dir_list)
#     
#     #print('    request._pyfuncitem: ',request._pyfuncitem)
#     print('    request.function: ',request.function)
#     print('    request.function.__dict__: ',request.function.__dict__)
#     print('    request.module: ',request.module)
#     print('    request.module.__dict__: ',request.module.__dict__)
#     print('    request.module dir: ',dir(request.module))
#     print('    request.node: ',request.node)
#     print('    request.node.__dict__: ',request.node.__dict__)
#     print('    request.node dir: ',dir(request.node))
    
    case_name = request.node._nodeid
    airtestlog = request.config.getoption("airtestlog")
    if airtestlog:
        split_path = request.module.__file__.split(PROJ_NAME)
        log_parentdir = split_path[0]+PROJ_NAME+'\\'+'reports'
        if not os.path.exists(log_parentdir):
            os.mkdir(log_parentdir)
        jkbuildid=request.config.getoption("--jkbuildid")
        jkjobname=request.config.getoption("--jkjobname")
        htmlhead=request.config.getoption("--htmlhead")
        if jkbuildid!=-1 and jkjobname:
            logdir = os.path.join(log_parentdir,jkjobname)
            if not os.path.exists(logdir):
                os.mkdir(logdir)
            logdir = os.path.join(logdir,jkbuildid)
            if not os.path.exists(logdir):
                os.mkdir(logdir)
        else:
            logdir = log_parentdir
        #log_subdir = request.module.__name__+' '+request.function.__name__
        logdir = os.path.join(logdir,request.module.__name__)
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        logdir = os.path.join(logdir,request.function.__name__)
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        print('    logdir: ',logdir)
        #request.logdir=logdir
        G.LOGGING.debug('logdir: %s' % logdir)
        set_logdir(logdir)
    
    startapp = request.config.getoption("startapp")
    if startapp:
        print('conftest: start app')
        start_app(APP_PACKAGE)
    yield driver_class
    
    def dr_finalizer():
        stopapp = request.config.getoption("stopapp")
        if stopapp:
            stop_app(APP_PACKAGE)
            print()
            print('conftest: stop app')
        
        airtesthtml = request.config.getoption("airtesthtml")
        if airtesthtml:
            from airtest.report.report import custom_report
            custom_report(case_name, logpath=logdir)
    request.addfinalizer(dr_finalizer)
    
            
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
            fpath=os.path.join(PROJ_ROOT,'files','prod_env', 'account_list.json')
            f=open(fpath, 'r', encoding='utf-8')
            user_account = json.loads(f.read())
        else:
            fpath=os.path.join(PROJ_ROOT,'files','test_env', 'account_list.json')
            f=open(fpath, 'r', encoding='utf-8')
            user_account = json.loads(f.read())
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
    
#@pytest.mark.hookwrapper
def pytest_runtest_protocol(item, nextitem):
    #print('    hook pytest_runtest_protocol!!!!')
    store_run_cases(item, nextitem)
                 


# def _gather_screenshot(item, report, driver, summary, extra):
#     try:
#         screen = G.DEVICE.snapshot()
# #         #截图前先切回原生： NATIVE_APP
# #         pre_context=driver.current_context
# #         if pre_context!='NATIVE_APP':
# #             driver.switch_to.context('NATIVE_APP')
# #         screenshot = driver.get_screenshot_as_base64()
# #          
# #         if pre_context!='NATIVE_APP':
# #             driver.switch_to.context(pre_context)
#     except Exception as e:
#         summary.append('WARNING: Failed to gather screenshot: {0}'.format(e))
#         return
#     pytest_html = item.config.pluginmanager.getplugin('html')
#     if pytest_html is not None:
#         # add screenshot to the html report
#         extra.append(pytest_html.extras.image(screenshot, 'Screenshot'))


# def pytest_runtest_logstart(nodeid, location):
#     print('    >>>>>pytest_runtest_logstart nodeid: ',nodeid)   
#     print('    >>>>>pytest_runtest_logstart location: ',location)   
        
# def pytest_runtest_logfinish(nodeid, location):
#     print('    <<<<<<<<pytest_runtest_logfinish nodeid: ',nodeid)   
#     print('    <<<<<<<<pytest_runtest_logfinish location: ',location)  
    
@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
 
    outcome = yield
    report = outcome.get_result()
    
    #print('    call.__dict__: ',call.__dict__)
    #print('    call dir: ',dir(call))
    
#     run_phase=getattr(report, 'when', 'call')
#     if run_phase == 'call':
#         print('    outcome: ',outcome)
#         print('    ~~~~')
#         print('    outcome __dict__: ',outcome.__dict__)
#         print('    ~~~~')
#         print('    outcome dir: ',outcome.excinfo)
#         print('    ~~~~')
#         print('    outcome dir: ',outcome.force_result)
#         print('    ~~~~')
#         print('    outcome dir: ',outcome.from_call)
#         print('    ~~~~')
#         print('    outcome dir: ',outcome.__dict__)
#         print('    ~~~~')
#         print('    report: ',report)
#         print('    ~~~~')
#         print('    report __dict__: ',report.__dict__)
#         print('    ~~~~')
#         print('    report dir: ',dir(report))
#         print('    ~~~~')
    
    report.description = str(item.function.__doc__)
    summary = []
    extra = getattr(report, 'extra', [])
    
    #print('    item.funcargs:',item.funcargs)
#     driver=None
#     if 'air_dr' in item.funcargs:
#         driver = item.funcargs['air_dr']
         
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
        #if driver is not None:
#         if 'air_dr' in item.funcargs:
#             # gather debug that depends on a driver instance
#             if 'screenshot' not in exclude:
#                 _gather_screenshot(item, report, driver, summary, extra)
            #if 'html' not in exclude:
            #    _gather_html(item, report, driver, summary, extra)
            #if 'logs' not in exclude:
            #    _gather_logs(item, report, driver, summary, extra)

    if summary:
        report.sections.append(('pytest-appdriver', '\n'.join(summary)))
    report.extra = extra
    
    update_run_tests(item, call, report)
    
    