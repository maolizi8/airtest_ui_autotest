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
import logging
import pytest
from airtest.core.api import start_app,stop_app,connect_device,ST

LOGGER = logging.getLogger(__name__)


PROJ_ROOT = os.path.dirname(os.path.abspath(__file__))
print('conftest - PROJ_ROOT :',PROJ_ROOT)

'''
增加命令行参数
'''
def pytest_addoption(parser):
    '''命令行参数'''
    parser.addoption("--uuid", action="store", default='Android://127.0.0.1:5037/46709b100104',
        help="udid of the device to run scripts")

@pytest.fixture(scope="session")
def driver_class(request):
    #print('conftest:   ST.PROJECT_ROOT: ',ST.PROJECT_ROOT)
    #ST.PROJECT_ROOT = 'E:\\mypython\\airtest_ui_autotest\\business'
    #print('conftest:     ST.PROJECT_ROOT: ',ST.PROJECT_ROOT)
    ST.LOG_DIR=os.path.join(PROJ_ROOT,'logs')
    uuid = request.config.getoption("uuid")
    
    print("conftest: driver_class。。。。。")
    devices=connect_device(uuid)
    print('conftest: ',devices)
    return devices

@pytest.fixture
def air_dr(request,driver_class):
    """Returns a WebDriver instance based on options and capabilities"""
    
    print('conftest: start app')
    start_app("com.yiwang.fangkuaiyi")
    yield driver_class
    stop_app("com.yiwang.fangkuaiyi")
    print('conftest: stop app')

    
# @pytest.fixture(scope="session")
# def session_capabilities(pytestconfig):
#     """Returns combined capabilities from pytest-variables and command line"""
#     driver = pytestconfig.getoption("air_dr")
#     
#     return capabilities
# 
# 
# @pytest.fixture
# def capabilities(
#     request, driver_class, chrome_options, firefox_options, session_capabilities
# ):
#     """Returns combined capabilities"""
#     capabilities = copy.deepcopy(session_capabilities)  # make a copy
#     if driver_class == webdriver.Remote:
#         browser = capabilities.get("browserName", "").upper()
#         key, options = (None, None)
#         if browser == "CHROME":
#             key = getattr(chrome_options, "KEY", "goog:chromeOptions")
#             options = chrome_options.to_capabilities()
#             if key not in options:
#                 key = "chromeOptions"
#         elif browser == "FIREFOX":
#             key = firefox_options.KEY
#             options = firefox_options.to_capabilities()
#         if all([key, options]):
#             capabilities[key] = _merge(capabilities.get(key, {}), options.get(key, {}))
#     capabilities.update(get_capabilities_from_markers(request.node))
#     return capabilities
# 
# 
# def get_capabilities_from_markers(node):
#     capabilities = dict()
#     for level, mark in node.iter_markers_with_node("capabilities"):
#         LOGGER.debug(
#             "{0} marker <{1.name}> "
#             "contained kwargs <{1.kwargs}>".format(level.__class__.__name__, mark)
#         )
#         capabilities.update(mark.kwargs)
#     LOGGER.info("Capabilities from markers: {}".format(capabilities))
#     return capabilities
# 
# 
# @pytest.fixture
# def driver_args():
#     """Return arguments to pass to the driver service"""
#     return None
# 
# 
# @pytest.fixture
# def driver_kwargs(
#     request,
#     capabilities,
#     chrome_options,
#     driver_args,
#     driver_class,
#     driver_log,
#     driver_path,
#     firefox_options,
#     firefox_profile,
#     pytestconfig,
# ):
#     kwargs = {}
#     driver = getattr(drivers, pytestconfig.getoption("driver").lower())
#     kwargs.update(
#         driver.driver_kwargs(
#             capabilities=capabilities,
#             chrome_options=chrome_options,
#             driver_args=driver_args,
#             driver_log=driver_log,
#             driver_path=driver_path,
#             firefox_options=firefox_options,
#             firefox_profile=firefox_profile,
#             host=pytestconfig.getoption("host"),
#             port=pytestconfig.getoption("port"),
#             service_log_path=None,
#             request=request,
#             test=".".join(split_class_and_test_names(request.node.nodeid)),
#         )
#     )
#     pytestconfig._driver_log = driver_log
#     return kwargs
# 
# 
# @pytest.fixture(scope="session")
# def driver_class(request):
#     driver = request.config.getoption("driver")
#     if driver is None:
#         raise pytest.UsageError("--driver must be specified")
#     return SUPPORTED_DRIVERS[driver]
# 
# 
# @pytest.fixture
# def driver_log(tmpdir):
#     """Return path to driver log"""
#     return str(tmpdir.join("driver.log"))
# 
# 
# @pytest.fixture
# def driver_path(request):
#     return request.config.getoption("driver_path")
# 
# 
# @pytest.fixture
# def driver(request, driver_class, driver_kwargs):
#     """Returns a WebDriver instance based on options and capabilities"""
#     driver = driver_class(**driver_kwargs)
# 
#     event_listener = request.config.getoption("event_listener")
#     if event_listener is not None:
#         # Import the specified event listener and wrap the driver instance
#         mod_name, class_name = event_listener.rsplit(".", 1)
#         mod = __import__(mod_name, fromlist=[class_name])
#         event_listener = getattr(mod, class_name)
#         if not isinstance(driver, EventFiringWebDriver):
#             driver = EventFiringWebDriver(driver, event_listener())
# 
#     request.node._driver = driver
#     yield driver
#     driver.quit()
# 
# 
# @pytest.fixture
# def selenium(driver):
#     yield driver
# 
# 
# @pytest.hookimpl(trylast=True)
# def pytest_configure(config):
#     capabilities = config._variables.get("capabilities", {})
#     capabilities.update({k: v for k, v in config.getoption("capabilities")})
#     config.addinivalue_line(
#         "markers",
#         "capabilities(kwargs): add or change existing "
#         "capabilities. specify capabilities as keyword arguments, for example "
#         "capabilities(foo="
#         "bar"
#         ")",
#     )
#     if hasattr(config, "_metadata"):
#         config._metadata["Driver"] = config.getoption("driver")
#         config._metadata["Capabilities"] = capabilities
#         if all((config.getoption("host"), config.getoption("port"))):
#             config._metadata["Server"] = "{0}:{1}".format(
#                 config.getoption("host"), config.getoption("port")
#             )
#     config._capabilities = capabilities