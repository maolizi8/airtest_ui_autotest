'''
Created on 2019年8月7日

@author: geqiuli
'''
import os

import pytest

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("tests - root_dir :",root_dir)

def get_latest_file(dirname,*subdirs,**kw):
    '''此处以项目名AutoTest为根目录开始查找
    @param dirname: 一级目录
    @param subdirs: 子目录，可多个
    @param kw:  指定参数名 tclevel : 针对dirname=report时，按用例级别选择report下的目录
    '''
    if dirname=='report':
        if kw['tclevel']==None:
            raise Exception('tclevel is required!')
        #subdir='AllPcTest-'+kw['tclevel']
        # tc_plat=kw['tclevel'].split('_')[0].title()
        #subdir='All'+tc_plat+'Test-'+kw['tclevel']
        subdir=kw['tclevel']
        #absdir=root_dir+dirname+os.sep+subdir+os.sep
        absdir=os.sep.join([root_dir,dirname,subdir])
    else:
        #absdir=root_dir+dirname+os.sep
        #for sub in subdirs:
        #    absdir+=sub+os.sep
        absdir=os.sep.join([root_dir,dirname]+subdirs)
        
    print('report dir:',absdir)
    file_new=''
    if os.path.isdir(absdir):
        lists_all = os.listdir(absdir)
    else:
        return file_new
    list_file=[]
    for f in lists_all:
        if os.path.isfile(absdir+f):
            list_file.append(f)
    list_file.sort(key=lambda fn:os.path.getmtime(absdir+fn))
    
    list_file2=[]
    if 'file_name' in kw:
        for lf in list_file:
            if kw['file_name'] in lf:
                list_file2.append(lf)
        if list_file2:
            file_new = absdir+ list_file2[-1]
            print('file_new: ',file_new)
            return file_new
        else:
            return file_new
    
    if list_file:
        file_new = os.sep.join(absdir,list_file[-1])
        print('file_new: ',file_new)
        return file_new
    else:
        return file_new
       
def runtc(tcname,tclevel,driver='Chrome',options=[]):
    '''运行测试用例
    @param tcname: 可以是文件名（名字含.py）、文件夹
    @param tclever: mark标记，筛选用例
    @param driver: 浏览器，不支持Remote'''
    
    #tc_plat=tclevel.split('_')[0].title()
    #subdir='All'+tc_plat+'Test-'+tclevel
    subdir=tclevel
    #subdir='AllPcTest-'+tclevel
    latest_report=get_latest_file('report',tclevel=tclevel)
    if latest_report:
        report_name=latest_report.split(subdir+'-')[1]
        fname=subdir+'-'+str(int(report_name[:-5])+1)+'.html'
    else:
        fname=subdir+'-1.html'
    
    #report_name=root_dir+'report'+os.sep+subdir+os.sep+fname
    report_name=os.sep.join([root_dir,'report',subdir,fname])
    print('report_name:',report_name)
    args=[tcname,'-m '+tclevel,'--driver='+driver]
    
    for opt in options:
        args.append(opt)
    args.append('--html=' + report_name)
    args.append('--self-contained-html')
    pytest.main(args)

def run_case(tcname,tclevel,driver='Chrome',env='prd',options=[]):
    '''运行测试用例
    @param tcname: 可以是文件名（名字含.py）、文件夹
    @param driver: 浏览器，不支持Remote'''
    subdir=tclevel
    latest_report=get_latest_file('report',tclevel=tclevel)
    if latest_report:
        report_name=latest_report.split(subdir+'-')[1]
        fname=subdir+'-'+str(int(report_name[:-5])+1)+'.html'
    else:
        fname=subdir+'-1.html'
    
    #report_name=root_dir+'report'+os.sep+subdir+os.sep+fname
    report_name=os.sep.join([root_dir,'report',subdir,fname])
    print('report_name:',report_name)
    args=[tcname,'-m '+tclevel,'--exc_env='+env,'--driver='+driver]
    
    for opt in options:
        args.append(opt)
    args.append('--html=' + report_name)
    args.append('--self-contained-html')
    pytest.main(args)

def run_case_newreport(tcname,tclevel,jkbuildid,jkjobname,driver='Chrome',env='prd',
                       htmlhead='UI Test Report',options=[]):
    '''运行测试用例
    @param tcname: 可以是文件名（名字含.py）、文件夹
    @param driver: 浏览器，不支持Remote'''
    subdir=tclevel
    latest_report=get_latest_file('report',tclevel=tclevel)
    if latest_report:
        report_name=latest_report.split(subdir+'-')[1]
        fname=subdir+'-'+str(int(report_name[:-5])+1)+'.html'
    else:
        fname=subdir+'-1.html'
    
    #report_name=root_dir+'report'+os.sep+subdir+os.sep+fname
    report_name=os.sep.join([root_dir,'report',subdir,fname])
    print('report_name:',report_name)
    args=[tcname,'-m '+tclevel,
          '--jkbuildid='+str(jkbuildid),'--jkjobname='+str(jkjobname),
          '--htmlhead='+htmlhead,
          '--exc_env='+env,'--driver='+driver]
    
    for opt in options:
        args.append(opt)
    args.append('--html=' + report_name)
    args.append('--self-contained-html')
    args.append('--simple-html')
    pytest.main(args)
    
      
if __name__=='__main__':
    pass