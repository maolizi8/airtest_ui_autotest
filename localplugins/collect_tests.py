'''
Created on 2019年7月5日

@author: geqiuli
'''
import sys
import os
import importlib
import inspect
import re
from public import mysql_opr
from public import files
import time    
#import platform 
#print('当前操作系统：',platform.platform())   

current_time=int(time.time()*1000)
print(current_time)
 
def get_funcs(module, package):
    
    module = importlib.import_module(module, package)
    for attr in dir(module):
        if not attr.startswith("__"):
            func = getattr(module, attr)


def get_packages(repodir,projname,package,coll_id,py_project,platform,depth=1,conn=None):
    '''
    @param depth: package下目录深度，暂支持0，1，2
    '''
    except_dir=['__pycache__','Archive','.pytest_cache']
    except_file=['__init__.py']
    pack_path=os.sep.join([repodir,projname,package])
    print('pack_path: ',pack_path)
    all_dirs = {}
    all_pack = {}
    
    def get_sub_dirs(dir_path,pack_name,sub_dir,depth):
        print('sub_dir: ',sub_dir)
        sub_list = os.listdir(dir_path)
        print('sub_list: ',sub_list)
        for item in sub_list:
            #print('item: ',item)
            item_path=os.sep.join([dir_path,item])
            if depth==0:
                if os.path.isfile(item_path) and item=='__init__.py':
                    mname, ext = os.path.splitext(item)
                    module = "." + mname
                    #print('type(module): ',type(module))
                    module = importlib.import_module(module, pack_name)
                    #print('inspect.getfile(module):',inspect.getfile(module))
                    #print('module.__name__: ',module.__name__)
                    if module.__doc__:
                        all_pack[pack_name]=module.__doc__.replace('\n','')
                    else:
                        all_pack[pack_name]=module.__doc__
                    if conn:
                        sql1='''select * from auto_ui_businessmodule where py_package='{}'
                                and py_project={}'''.format(pack_name,py_project)
                        res1=mysql_opr.select_from_mysql(conn, sql1)
                        if res1['code']==0 and len(res1['data'])>0:
                            print('已经存在：',pack_name)
                        else:
                            print('新增子包：',pack_name)
                            sql2='''INSERT INTO auto_ui_businessmodule(name,platform,collection,
                            sub_package,py_package,py_project,
                            run_env,ui_sys)
                                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')
                                    '''.format(all_pack[pack_name],platform,coll_id,
                                               1,pack_name,py_project,
                                               0,1)
                            mysql_opr.query_mysql2(conn,sql2)
            if depth>0:
                if os.path.isdir(item_path) and item not in except_dir:
                    sub_dir[item]={}
                    #print('dirs: ',sub_dir[item])
                    pack_name1 = ('.').join([pack_name,item])
                    get_sub_dirs(item_path,pack_name1,sub_dir[item],depth-1)
    
    get_sub_dirs(pack_path,package,all_dirs,depth)
    print('------- all_dirs: -----')
    print(all_dirs)
    print(all_pack)
    return all_dirs

            
def get_moudles(repodir,projname,package,depth=0):
    '''
    @param depth: package下目录深度，暂支持0，1，2'''
    except_dir=['__pycache__','Archive','.pytest_cache']
    except_file=['__init__.py']
    pack_path=os.sep.join([repodir,projname,package])
    print('pack_path: ',pack_path)
    all_files = {'files':[],'dirs':{}}
    #sub_list = os.listdir(pack_path)
    
    
    def get_sub_dirs_and_files(dir_path,sub_obj,depth):
        print('sub_obj: ',sub_obj)
        sub_list = os.listdir(dir_path)
        for item in sub_list:
            #print('-'*depth+'item: ',item)
            #item_path=os.sep.join([repodir,projname,package,item])
            item_path=os.sep.join([dir_path,item])
            if depth==0:
                if os.path.isfile(item_path) and item not in except_file:
                    print('file path: ',item_path)
                    filename=item.lower()
                    if filename.startswith("test_"):
                        print('test file')
                        sub_obj['files'].append(item_path)
            if depth>0:
                if os.path.isfile(item_path) and item not in except_file:
                    print('file path: ',item_path)
                    filename=item.lower()
                    if filename.startswith("test_"):
                        print('test file')
                        sub_obj['files'].append(item_path)
                elif os.path.isdir(item_path) and item not in except_dir:
                    sub_obj['dirs'][item]={'files':[],'dirs':{}}
                    #sub_list1 = os.listdir(item_path)
                    get_sub_dirs_and_files(item_path,sub_obj['dirs'][item],depth-1)
    
    get_sub_dirs_and_files(pack_path,all_files,depth)
    print('------- all_files: -----')
    print(all_files)
    return all_files



def import_source(module_name,module_file_path):
    #module_file_path = module_name.__file__
    #module_name = module_name.__name__
    print('module_file_path: ',module_file_path)
    print('module_name: ',module_name)
    module_spec = importlib.util.spec_from_file_location(module_name.name ,module_file_path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    print(dir(module))
#     spec = importlib.util.spec_from_file_location('my_module', '/paht/to/my_module')
#     module = importlib.util.module_from_spec(spec)
#     spec.loader.exec_module(module)
        
def get_module_testcase(package,pyfile,run_env,platform,coll_id,conn=None,module_id=None):
    #filename=pyfile.lower()
    mname, ext = os.path.splitext(pyfile)
    module="." + mname
    #print('type(module): ',type(module))
     
    module = importlib.import_module(module, package)
    #testcases=[]
    #print('module.__dict__: ',module.__dict__)
    #print('inspect.getfile(module):',inspect.getfile(module))
    #print('pyfile: ',pyfile)
    print('module.__name__: ',module.__name__)
    file_path=module.__name__.replace('.','/')+'.py'
    #print('file_path: ',file_path)
    #print('module: ',module.__dict__)
    #print('module: ',help(module))
    #file_path=package.replace('.',os.sep)+os.sep+module.__name__
    #print('sourcecode:')
    #print(inspect.getsource(module))
    print('dir(module): ',dir(module))
    for attr in dir(module):
        if attr.startswith("test"):
            func = getattr(module, attr)
            print('    testcase:',func.__name__)
            pytestmark=[]
            py_skip_reason=''
            tapd_id=''
            tapd_proj=''
            cart_order_oprs=1
            if 'pytestmark' in func.__dict__:
                #print('    pytestmarks:',func.__dict__['pytestmark'])
                #print('    ',func.__dict__['pytestmark'])
                for item in func.__dict__['pytestmark']:
                    if item.__dict__['name']=='tapd':
                        if item.__dict__['args']:
                            tapd_str=str(item.__dict__['args'][0]).split('_')
                            if len(tapd_str)>1:
                                tapd_proj=tapd_str[0]
                                tapd_id=tapd_str[1]
                            else:
                                tapd_id=tapd_str[0]
                    else:
                        pytestmark.append(item.__dict__['name'])
                        if item.__dict__['name']=='skip':
                            #print('    py_skip_reason:',item.__dict__)
                            if item.__dict__['args']:
                                py_skip_reason=item.__dict__['args'][0]
                            
                        if '_nocart' in item.__dict__['name']:
                            cart_order_oprs=0
                    
                    
            #print('    ',func.__doc__)
            #testcases.append(func.__name__)
            
            py_name=file_path+" ::"+func.__name__
            
            print('    func content:')
            #print(inspect.getsource(func))
            assert_search=re.findall('assert ',inspect.getsource(func))
            assert_num=len(assert_search)
            print('    func assert_num:',assert_num)
            
            if conn:
                print('------------------------------')
                if module_id:
                    business_module=module_id
                else:
                    business_module=0
                sql0="""SELECT id FROM auto_ui_testcase
                    WHERE py_name='{0}'
                    AND collection={1}""".format(py_name,coll_id)
                res0=mysql_opr.select_from_mysql(conn, sql0, total=0, close=False)
                if res0['code']==0 and len(res0['data'])>0:
                    print('已有此用例，更新：',py_name)
                    sql1='''UPDATE auto_ui_testcase SET py_desc='{0}',cart_order_oprs='{1}',
                            py_marks='{2}',run_env='{3}',platform='{4}',py_skip_reason='{5}',
                            business_module='{6}',tapd_id='{7}',tapd_proj='{8}',update_version='{9}',
                            assert_num={12}
                            WHERE py_name='{10}' AND collection={11}
                            '''.format(func.__doc__.replace('\'','"'), cart_order_oprs,
                                       ';'.join(pytestmark), run_env, platform, py_skip_reason,
                                       business_module, tapd_id, tapd_proj, current_time,
                                       py_name,coll_id,assert_num)
                    mysql_opr.query_mysql2(conn,sql1)
                else:
                    print('无此用例，新增：',py_name)
                    sql2='''INSERT INTO auto_ui_testcase(py_name,py_desc,py_module,cart_order_oprs,
                            py_marks,py_file,run_env,platform,collection,py_skip_reason,
                            business_module,tapd_id,tapd_proj,update_version,assert_num)
                            VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}',{7},'{8}','{9}','{10}','{11}','{12}','{13}','{14}')
                            '''.format(py_name, func.__doc__.replace('\'','"'), module.__name__, cart_order_oprs,
                                       ';'.join(pytestmark), file_path, run_env, 
                                       platform, coll_id,py_skip_reason,
                                       business_module, tapd_id, tapd_proj, current_time,assert_num)
                    #print('sql2: ',sql2)
                    mysql_opr.query_mysql2(conn,sql2)
    
def get_pyfiles_in_packages(root_dir,package,run_env,platform,coll_id,conn=None,module_id=None,find_sub=True):
    '''
    @param root_dir: eg. E:\\test-autotest\\AutoTest
    @param package: eg. prdenv_case.b2b_pc
    '''
    except_dir=['__pycache__','Archive','archive','Archived','archived','.pytest_cache']
    except_file=['__init__.py']
    
    root_dir=root_dir.replace('/','\\') #windows
    #root_dir=root_dir.replace('/',os.sep) #通用
    print('package:',package)
    path_items=[root_dir]+package.split('.')
    pack_path=os.sep.join(path_items)
    print('pack_path: ',pack_path)
    all_files = []
    all_modules = []
    sub_list = os.listdir(pack_path)
    
    def sub_list_cases(sub_list,package,pack_path,find_sub):
        print('sub_list: ',sub_list)
        for item in sub_list:
            #print('-'*depth+'item: ',item)
            item_path=os.sep.join([pack_path,item])
            print('item_path: ',item_path)
            if os.path.isfile(item_path) and item not in except_file:
                #print('file path: ',item_path)
                filename=item.lower()
                if filename.startswith("test_"):
                    print('----------------')
                    print('filename: ',filename)
                    #all_files.append(filename)
                    get_module_testcase(package,item,run_env,platform,coll_id,conn=conn,module_id=module_id)
            elif os.path.isdir(item_path) and item not in except_dir:
                if find_sub==True:
                    sub_list1 = os.listdir(item_path)
                    sub_package = package+'.'+item
                    sub_list_cases(sub_list1,sub_package,item_path,False) 
    sub_list_cases(sub_list,package,pack_path,find_sub)            

def store_all_testcase_to_db(proj='AutoTest'):  
    datainfo=files.read_json('yyw-0345', 'mysql')
    conn=mysql_opr.get_connection(serverip = datainfo['host'],
        port = int(datainfo['port']),
        account = datainfo['user'],
        password = datainfo['password'],
        db_name='qateam')
    sql0="insert into auto_ui_case_updateversion(update_version,proj_name) VALUES('{0}','{1}')".format(current_time,proj)
    mysql_opr.query_mysql2(conn,sql0)
    
    sql1="""SELECT * FROM
            (SELECT a.id,a.py_package,a.run_env,a.platform,a.sub_package,c.root_dir,c.name from auto_ui_collection a
             LEFT JOIN auto_ui_project c ON a.py_project=c.id) b
             WHERE b.name='{}'""".format(proj)
    package_list=mysql_opr.select_from_mysql(conn, sql1, 0)['data'] 
    for pk in package_list:
        if pk['sub_package']==0:
            #get_pyfiles_in_packages('E:\\test-autotest\\AutoTest','prdenv_case.b2b_pc',conn)
            get_pyfiles_in_packages(pk['root_dir'],pk['py_package'],pk['run_env'],pk['platform'],pk['id'],conn=conn,find_sub=True)
        else:
            sql2="""SELECT * FROM
                    (SELECT a.id,a.run_env,a.platform,a.sub_package,c.root_dir,c.name,d.py_package,d.id AS moduleid
                     FROM auto_ui_collection a
                     LEFT JOIN auto_ui_project c ON a.py_project=c.id
                     LEFT JOIN auto_ui_businessmodule d ON a.id=d.collection
                    ) b
                     WHERE b.name='{}'
                     AND b.sub_package=1""".format(proj)
            package_list1=mysql_opr.select_from_mysql(conn, sql2, 0)['data'] 
            print('package_list1: ',package_list1)
            for sub_pk in package_list1:
                get_pyfiles_in_packages(sub_pk['root_dir'],sub_pk['py_package'],
                                        sub_pk['run_env'],sub_pk['platform'],sub_pk['id'],
                                        conn=conn,module_id=sub_pk['moduleid'],find_sub=False)


import pytest
@pytest.mark.collect_test
def test_update_testcases():
    store_all_testcase_to_db(proj='AutoTest')
        
if __name__ == '__main__':
    pass
    store_all_testcase_to_db(proj='AutoTest')
    
    #get_pyfiles_in_packages('E:/test-androidapp/yaoex_app_auto_android','prdenv_case',2,1,3,conn=None,module_id=None,find_sub=True)
    #get_module_testcase('prdenv_case.b2b_pc','test_check_order_invoice_info.py',1,1,1,conn=None)
    
#     datainfo=files.read_json('yyw-0345', 'mysql')
#     conn=mysql_opr.get_connection(serverip = datainfo['host'],
#         port = int(datainfo['port']),
#         account = datainfo['user'],
#         password = datainfo['password'],
#         db_name='qateam')
#     get_packages('E:\\test-androidapp','yaoex_app_auto_android','regressioncase',
#                  coll_id=9,py_project=3,platform=1,depth=1,conn=conn)
    
    