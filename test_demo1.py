'''
Created on 2019年7月19日

@author: geqiuli
'''
from airtest_runner import AirtestCase, run_script
from argparse import *
from airtest.core.api import *
import airtest.report.report as report
import jinja2
import shutil
import os
import io

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print('conftest - BASE_DIR :',BASE_DIR)
 
class CustomAirtestCase(AirtestCase):
    def setUp(self):
        print("custom setup")
        # add var/function/class/.. to globals
        # self.scope["hunter"] = "i am hunter"
        # self.scope["add"] = lambda x: x+1
  
        # exec setup script
        # self.exec_other_script("setup.owl")
        super(CustomAirtestCase, self).setUp()
  
    def tearDown(self):
        print("custom tearDown")
        # exec teardown script
        # self.exec_other_script("teardown.owl")
        super(CustomAirtestCase, self).setUp()
  
    def run_air(self, root_dir, device):
        # 聚合结果
        results = []
        # 获取所有用例集
        root_log = root_dir + '\\' + 'log'
        if os.path.isdir(root_log):
            print('log folder is exist')
            #shutil.rmtree(root_log)
        else:
            os.makedirs(root_log)
            print(str(root_log) + 'is created')
         
        print('')
        for f in os.listdir(root_dir):
            print('root_dir > f:',f)
            if f.endswith(".air"):
                # f为.air案例名称：手机银行.air
                print('test file:',f)
                airName = f
                script = os.path.join(root_dir, f)
                # airName_path为.air的全路径：D:\tools\airtestCase\案例集\log\手机银行
                print('script:',script)
                # 日志存放路径和名称：D:\tools\airtestCase\案例集\log\手机银行1
                log = os.path.join(root_dir, 'log' + '\\' + airName.replace('.air', ''))
                print('log：',log)
                if os.path.isdir(log):
                    print('log： if exist ')
                    #shutil.rmtree(log)
                else:
                    os.makedirs(log)
                    print(str(log) + ' is created')
                log_file=log+'\\log.txt'
                if not os.path.exists(log_file):
                    ff = open(log_file,'w')
                    print('create log file: ',ff)
                    ff.close()
                else:
                    print(log_file + " already existed.")
                output_file = log + '\\' + 'log.html'
                args = Namespace(device=device, log=log, recording=None, script=script)
                try:
                    print('运行脚本开始')
                     
                    start_app("com.yiwang.fangkuaiyi")
                 
                    run_script(args, AirtestCase)
                     
                    print('运行脚本结束')
                except Exception as e:
                    print('运行失败，',e)
                finally:
                    stop_app("com.yiwang.fangkuaiyi")
                     
                    try:
                        print('生成报告')
                        rpt = report.LogToHtml(script_root=root_dir, log_root=log, script_name=script)
                        print('output_file:',output_file)
                        rpt.report("log_template.html", output_file=output_file)
                        result = {}
                        result["name"] = airName.replace('.air', '')
                        result["result"] = rpt.test_result
                        results.append(result)
                    except Exception as e:
                        print('运行失败，暂时不抛异常，',e)
                     
         
        print('生成聚合报告')
        # 生成聚合报告
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(root_dir),
            extensions=(),
            autoescape=True
        )
        template = env.get_template("summary_template.html", root_dir)
        html = template.render({"results": results})
        output_file = os.path.join(root_dir, "summary.html")
        with io.open(output_file, 'w', encoding="utf-8") as f:
            f.write(html)
        print('output_file:',output_file)
    
    def run_air_batch_mode(self, tc_folder, device):
        # 聚合结果
        report_dir = os.sep.join([BASE_DIR, 'reports'])
        case_dir = os.sep.join([BASE_DIR, tc_folder])
        
        results = []
        # 获取所有用例集
        if os.path.isdir(report_dir):
            print('report folder is exist')
            report_subs = os.listdir(report_dir) 
            print('report folder > files: ',report_subs)
            if len(report_subs):
                def is_dir(item):
                    item_path=os.sep.join([report_dir,item])
                    return os.path.isdir(item_path)
                
                folder_lists=list(filter(is_dir,report_subs))
                print('report folder > folders: ',folder_lists)
                folder_lists.sort(key=lambda fn:os.path.getctime(os.sep.join([report_dir,fn])))
                # getmtime ? getctime
                final_num=folder_lists[-1]
                report_num=int(final_num)+1
            else:
                report_num=0
        else:
            os.makedirs(report_dir)
            print('report folder is created')
            report_num=0
            
        report_dir_num = os.sep.join([BASE_DIR,'reports',str(report_num)])
        print('report_dir_num: ',report_dir_num)
        os.makedirs(report_dir_num)
        
        
        for f in os.listdir(case_dir):
            print('case_dir > f:',f)
            if f.endswith(".air"):
                # f为.air案例名称
                print('   (.air)test file:',f)
                airName = f
                script = os.path.join(case_dir, f)
                # airName_path为.air的全路径：BASE_DIR\案例集\testcase.air
                print('   script:',script)
                # 日志存放路径和名称：BASE_DIR\reports\案例集\testcase\
                tc_report_dir = os.path.join(report_dir_num, airName.replace('.air', ''))
                print('tc_report_dir：',tc_report_dir)
                if os.path.isdir(tc_report_dir):
                    print('tc_report_dir exist ')
                else:
                    os.makedirs(tc_report_dir)
                    print('tc_report_dir is created')
                
                log_file=os.path.join(tc_report_dir, 'log.txt')
                
                if not os.path.exists(log_file):
                    log_content = open(log_file,'w')
                    print('create log file: ',log_content)
                    log_content.close()
                else:
                    print(log_file + " already existed.")
                output_file = os.path.join(tc_report_dir, 'log.html')
                args = Namespace(device=device, log=log_file, recording=None, script=script)
                try:
                    print('运行脚本开始')
                    
                    #start_app("com.yiwang.fangkuaiyi")
                
                    run_script(args, AirtestCase)
                    
                    print('运行脚本结束')
                except Exception as e:
                    print('运行失败，',e)
                finally:
                    #stop_app("com.yiwang.fangkuaiyi")
                    
                    try:
                        print('生成报告')
                        rpt = report.LogToHtml(script_root=case_dir, log_root=tc_report_dir, script_name=script)
                        print('output_file:',output_file)
                        rpt.report("log_template.html", output_file=output_file)
                        result = {}
                        result["name"] = airName.replace('.air', '')
                        result["result"] = rpt.test_result
                        results.append(result)
                    except Exception as e:
                        print('运行失败，暂时不抛异常，',e)
                    
        
        print('生成聚合报告')
        # 生成聚合报告
        static_dir=os.sep.join([BASE_DIR,'statics'])
        print('static_dir: ',static_dir)
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(static_dir),
            extensions=(),
            autoescape=True
        )
        template = env.get_template("summary_template.html", static_dir)
        print('template: ',template)
        html = template.render({"results": results,"report_num":report_num})
        summary_file = os.path.join(report_dir_num, "summary.html")
        with io.open(summary_file, 'w', encoding="utf-8") as f:
            f.write(html)
        print('summary_file:',summary_file)

import pytest

@pytest.mark.run_case
def test_run_airtest_cases():
    test=CustomAirtestCase()
    device = ['android:///']
    #test.run_air(r'E:\test-androidapp\airtest_ui_autotest\business', device)
    test.run_air_batch_mode('business', device)
 
if __name__ == '__main__':
    args=[__file__,'-m run_case','-s']
    pytest.main(args)
