'''
Created on 15 May 2019

@author: apple
'''
from base64 import b64encode, b64decode
from collections import OrderedDict
from os.path import isfile
import datetime
import json
import os
import pkg_resources
import sys
import time
import bisect
import hashlib
import warnings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('BASE_DIR :',BASE_DIR)

try:
    from ansi2html import Ansi2HTMLConverter, style
    ANSI = True
except ImportError:
    # ansi2html is not installed
    ANSI = False

from py.xml import html, raw #此处的报错，忽略即可，运行正常

from localplugins import extras

PY3 = sys.version_info[0] == 3

# Python 2.X and 3.X compatibility
if PY3:
    basestring = str
    from html import escape
else:
    from codecs import open
    from cgi import escape

def data_uri(content, mime_type='text/plain', charset='utf-8'):
    data = b64encode(content.encode(charset)).decode('ascii')
    return 'data:{0};charset={1};base64,{2}'.format(mime_type, charset, data)

def store_run_collections(session):
    jkbuildid=session.config.getoption("--jkbuildid")
    jkjobname=session.config.getoption("--jkjobname")
    htmlhead=session.config.getoption("--htmlhead")
    if jkbuildid!=-1 and jkjobname:
        try:
            from localplugins.mysql_opr import query_pymysql
            #print('[session.fspath: {}]'.format(session.fspath))
            fspath=str(session.fspath).replace('\\','\\\\')
            fpath=os.path.join(BASE_DIR,'localplugins','resources', 'mysql_qa.json')
            f=open(fpath, 'r', encoding='utf-8')
            dbinfo = json.loads(f.read())
            sql='''
            INSERT INTO ui_autotest_collections(htmlhead,jk_jobname,jk_buildid,fpath,tests_count)
            VALUES('{0}','{1}','{2}','{3}','{4}')
            '''.format(htmlhead,jkjobname,jkbuildid,fspath,len(session.items))
            query_pymysql(dbinfo['host'],dbinfo['user'],dbinfo['password'],dbinfo['port'],'qateam',sql)
            #print('.......insert test collection to mysql<uitest_collect>......',time.strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            #print('[Exception<inserting to uitest_collect>]',end='')
            print('Exception when inserting test collection to mysql: ',e)
            #print('[Exception<inserting to uitest_collect>: {}]'.format(e),end='')

def update_run_collections(item, call, report):
    jkbuildid=item.config.getoption("--jkbuildid")
    jkjobname=item.config.getoption("--jkjobname")
    if jkbuildid!=-1 and jkjobname:
        try:
            from html import escape
            from localplugins.mysql_opr import query_many_pymysql
            
            fpath=os.path.join(BASE_DIR,'localplugins','resources', 'mysql_qa.json')
            f=open(fpath, 'r', encoding='utf-8')
            dbinfo = json.loads(f.read())
            
            test_log=''
            error_png=''
            error_link=''
            error_html=''
            error_driverlog=''
            test_duration='%.4f' % report.duration
            
            if report.longrepr:
                log1=escape(report.longreprtext)
                log2=log1.replace('\\','\\\\')
                for line in log2.splitlines():
                    separator = line.startswith('_ ' * 10)
                    if separator:
                        test_log+=line[:80]
                    else:
                        exception = line.startswith("E   ")
                        if exception:
                            test_log+='<span class="error">{}</span><br>'.format(line)
                        else:
                            test_log+=line
                    test_log+='<br>'
    
            for section in report.sections:
                header = section[0]
                content = escape(section[1].replace("\\","\\\\"))
                test_log+=' {0} '.format(header).center(80, '-')
                test_log+='<br>'
                #if ANSI:
                #    converter = Ansi2HTMLConverter(inline=False, escaped=False)
                #    content = converter.convert(content, full=False)
                test_log+=content
                
            test_log=test_log.replace("'","\\'")
    
            if report.extra:
                for o in report.extra:
                    if o['name']=='Screenshot':
                        error_png=o['content']
                    #if o['name']=='HTML':
                    #    error_html=o['content'].replace("'","\\'")
                    if o['name']=='URL':
                        error_link=o['content']
                    #if o['name']=='Driver Log':
                    #    error_driverlog+=o['content']
            
            sql1=''
            sql2=''
            run_phase=getattr(report, 'when', 'call')
            #print('[run_phase:{}, status:{}]'.format(run_phase,report.outcome))
            testcase_name=(' ::').join(report.nodeid.split('::'))
            if run_phase == 'setup':
                if report.outcome=='failed' or report.outcome=='errors':
                    sql1='''
                    INSERT INTO ui_autotest_tests(jk_jobname,jk_buildid,test_name,
                    test_result,test_phase,test_desc,test_duration)
                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}')
                    '''.format(jkjobname, jkbuildid, testcase_name+' ::setup', 
                               report.outcome, report.when, report.description,test_duration)
                    sql2='''
                    INSERT INTO ui_autotest_tests_errors(jk_jobname,jk_buildid,test_name,test_log,error_png,error_link)
                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}')
                    '''.format(jkjobname,jkbuildid,testcase_name+' ::setup',test_log, error_png,error_link)
            elif run_phase == 'call':
                if report.outcome=='failed' or report.outcome=='errors':
                    sql1='''
                    INSERT INTO ui_autotest_tests(jk_jobname,jk_buildid,test_name,test_result,
                    test_phase,test_desc,test_duration)
                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}')
                    '''.format(jkjobname, jkbuildid, testcase_name, report.outcome,
                               report.when, report.description,test_duration)
                    sql2='''
                    INSERT INTO ui_autotest_tests_errors(jk_jobname,jk_buildid,test_name,test_log,error_png,error_link)
                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}')
                    '''.format(jkjobname,jkbuildid,testcase_name,test_log, error_png,error_link)
                else:
                    sql1='''
                    INSERT INTO ui_autotest_tests(jk_jobname,jk_buildid,test_name,test_result,
                    test_phase,test_desc,test_duration,test_log)
                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}')
                    '''.format(jkjobname, jkbuildid, testcase_name, report.outcome,
                               report.when, report.description,test_duration,test_log)
            elif run_phase == 'teardown':
                if report.outcome=='failed' or report.outcome=='errors':
                    sql1='''
                    INSERT INTO ui_autotest_tests(jk_jobname,jk_buildid,test_name,
                    test_result,test_phase,test_desc,test_duration)
                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}')
                    '''.format(jkjobname, jkbuildid, testcase_name+' ::tearDown', 
                               report.outcome, report.when, report.description, test_duration)
                    sql2='''
                    INSERT INTO ui_autotest_tests_errors(jk_jobname,jk_buildid,test_name,test_log,error_png,error_link)
                    VALUES('{0}','{1}','{2}','{3}','{4}','{5}')
                    '''.format(jkjobname,jkbuildid,testcase_name+' ::tearDown',test_log, error_png,error_link)
            query_many_pymysql(dbinfo['host'],dbinfo['user'],dbinfo['password'],dbinfo['port'],'qateam',sql1,sql2)
        except Exception as e:
            #print('[Exception<inserting to uitest_tests>]',end='')
            print('[Exception<inserting to uitest_tests>: {}]'.format(e),end='')    
            
            
class HTMLReport(object):
    
    '''***********************************gql***************************************
    def __init__(self, logfile, config):
    '''

    def __init__(self, logfile, config, htmlhead='测试报告'):
        
        '''***********************************gql***************************************'''
        #print('gql-add: logfile: ',logfile)
        self.htmlhead = htmlhead
        
        logfile = os.path.expanduser(os.path.expandvars(logfile))
        self.logfile = os.path.abspath(logfile)
        self.test_logs = []
        self.results = []
        self.errors = self.failed = 0
        self.passed = self.skipped = 0
        self.xfailed = self.xpassed = 0
        has_rerun = config.pluginmanager.hasplugin('rerunfailures')
        self.rerun = 0 if has_rerun else None
        self.self_contained = config.getoption('self_contained_html')
        self.config = config
        

    class TestResult:

        def __init__(self, outcome, report, logfile, config):
        
            #self.test_id = report.nodeid
            self.test_id = (' ::').join(report.nodeid.split('::'))
            if getattr(report, 'when', 'call') != 'call':
                self.test_id = ' ::'.join([report.nodeid, report.when])
            self.time = getattr(report, 'duration', 0.00)
            self.outcome = outcome
            self.additional_html = []
            self.links_html = []
            self.self_contained = config.getoption('self_contained_html')
            self.logfile = logfile
            self.config = config
            self.row_table = self.row_extra = None

            test_index = hasattr(report, 'rerun') and report.rerun + 1 or 0

            for extra_index, extra in enumerate(getattr(report, 'extra', [])):
                self.append_extra_html(extra, extra_index, test_index)

            self.append_log_html(report, self.additional_html)
            
            #add description
            if hasattr(report,"description"):
                des=report.description
            else:
                des="无"
                
            cells = [
                html.td(self.outcome, class_='col-result'),
                html.td(des, class_='col-description'), #des
                html.td(self.test_id, class_='col-name'),
                html.td('{0:.2f}'.format(self.time), class_='col-duration')
                #,html.td(self.links_html, class_='col-links')
                ]

            self.config.hook.pytest_html_results_table_row(
                report=report, cells=cells)

            self.config.hook.pytest_html_results_table_html(
                report=report, data=self.additional_html)

            if len(cells) > 0:
                self.row_table = html.tr(cells)
                self.row_extra = html.tr(html.td(self.additional_html,
                                                 class_='extra',
                                                 colspan=len(cells)))
            
            

        def __lt__(self, other):
            order = ('Error', 'Failed', 'Rerun', 'XFailed',
                     'XPassed', 'Skipped', 'Passed')
            return order.index(self.outcome) < order.index(other.outcome)

        def create_asset(self, content, extra_index,
                         test_index, file_extension, mode='w'):
            hash_key = ''.join([self.test_id, str(extra_index),
                                str(test_index)]).encode('utf-8')
            hash_generator = hashlib.md5()
            hash_generator.update(hash_key)
            asset_file_name = '{0}.{1}'.format(hash_generator.hexdigest(),
                                               file_extension)
            asset_path = os.path.join(os.path.dirname(self.logfile),
                                      'assets', asset_file_name)
            if not os.path.exists(os.path.dirname(asset_path)):
                os.makedirs(os.path.dirname(asset_path))

            relative_path = '{0}/{1}'.format('assets', asset_file_name)

            kwargs = {'encoding': 'utf-8'} if 'b' not in mode else {}
            with open(asset_path, mode, **kwargs) as f:
                f.write(content)
            return relative_path

        def append_extra_html(self, extra, extra_index, test_index):
            href = None
            #print()
            #print('-------append_extra_html----------')
            #print(extra)
            if extra.get('format') == extras.FORMAT_IMAGE:
                content = extra.get('content')
                try:
                    is_uri_or_path = (content.startswith(('file', 'http')) or
                                      isfile(content))
                except ValueError:
                    # On Windows, os.path.isfile throws this exception when
                    # passed a b64 encoded image.
                    is_uri_or_path = False
                if is_uri_or_path:
                    if self.self_contained:
                        warnings.warn('Self-contained HTML report '
                                      'includes link to external '
                                      'resource: {}'.format(content))
                    html_div = html.a(html.img(src=content), href=content)
                elif self.self_contained:
                    src = 'data:{0};base64,{1}'.format(
                        extra.get('mime_type'),
                        content)
                    html_div = html.img(src=src)
                    #print('extra  content len: ',len(content))
                else:
                    if PY3:
                        content = b64decode(content.encode('utf-8'))
                    else:
                        content = b64decode(content)
                    href = src = self.create_asset(
                        content, extra_index, test_index,
                        extra.get('extension'), 'wb')
                    html_div = html.a(html.img(src=src), href=href)
                self.additional_html.append(html.div(html_div, class_='image'))
 
            elif extra.get('format') == extras.FORMAT_HTML:
                self.additional_html.append(html.div(
                                            raw(extra.get('content'))))
 
            elif extra.get('format') == extras.FORMAT_JSON:
                content = json.dumps(extra.get('content'))
                if self.self_contained:
                    href = data_uri(content,
                                    mime_type=extra.get('mime_type'))
                else:
                    href = self.create_asset(content, extra_index,
                                             test_index,
                                             extra.get('extension'))
 
            elif extra.get('format') == extras.FORMAT_TEXT:
                content = extra.get('content')
                if isinstance(content, bytes):
                    content = content.decode('utf-8')
                if self.self_contained:
                    href = data_uri(content)
                else:
                    href = self.create_asset(content, extra_index,
                                             test_index,
                                             extra.get('extension'))
 
            elif extra.get('format') == extras.FORMAT_URL:
                href = extra.get('content')
 
            if href is not None:
                self.links_html.append(html.a(
                    extra.get('name'),
                    class_=extra.get('format'),
                    href=href,
                    target='_blank'))
                self.links_html.append(' ')
  
            

        def append_log_html(self, report, additional_html):
            log = html.div(class_='log')
            if report.longrepr:
                for line in report.longreprtext.splitlines():
                    separator = line.startswith('_ ' * 10)
                    if separator:
                        log.append(line[:80])
                    else:
                        exception = line.startswith("E   ")
                        if exception:
                            log.append(html.span(raw(escape(line)),
                                                 class_='error'))
                        else:
                            log.append(raw(escape(line)))
                    log.append(html.br())

            for section in report.sections:
                #header, content = map(escape, section)
                header = section[0]
                content = escape(section[1].replace("\\","\\\\"))
                #print('header1 : ',header)
                #print('content1 : ',content)
                log.append(' {0} '.format(header).center(80, '-'))
                log.append(html.br())
                if ANSI:
                    converter = Ansi2HTMLConverter(inline=False, escaped=False)
                    content = converter.convert(content, full=False)
                log.append(raw(content))

            if len(log) == 0:
                log = html.div(class_='empty log')
                log.append('No log output captured.')
            additional_html.append(log)

    def _appendrow(self, outcome, report):
        result = self.TestResult(outcome, report, self.logfile, self.config)
        if result.row_table is not None:
            index = bisect.bisect_right(self.results, result)
            self.results.insert(index, result)
            tbody = html.tbody(
                result.row_table,
                class_='{0} results-table-row'.format(result.outcome.lower()))
            '''
            if result.row_extra is not None:
                tbody.append(result.row_extra)
            '''
            #print('self.test_logs.insert(index, tbody) tbody:',tbody)
            self.test_logs.insert(index, tbody)

    def append_passed(self, report):
        if report.when == 'call':
            if hasattr(report, "wasxfail"):
                self.xpassed += 1
                self._appendrow('XPassed', report)
            else:
                self.passed += 1
                self._appendrow('Passed', report)

    def append_failed(self, report):
        if getattr(report, 'when', None) == "call":
            if hasattr(report, "wasxfail"):
                # pytest < 3.0 marked xpasses as failures
                self.xpassed += 1
                self._appendrow('XPassed', report)
            else:
                self.failed += 1
                self._appendrow('Failed', report)
        else:
            self.errors += 1
            self._appendrow('Error', report)

    def append_skipped(self, report):
        if hasattr(report, "wasxfail"):
            self.xfailed += 1
            self._appendrow('XFailed', report)
        else:
            self.skipped += 1
            self._appendrow('Skipped', report)

    def append_other(self, report):
        # For now, the only "other" the plugin give support is rerun
        self.rerun += 1
        self._appendrow('Rerun', report)

    def _generate_report(self, session):
        suite_stop_time = time.time()
        suite_time_delta = suite_stop_time - self.suite_start_time
        test_duration = '%.4f' %(suite_time_delta)
        numtests = self.passed + self.failed + self.xpassed + self.xfailed
        generated = datetime.datetime.now()
        
        jkbuildid=session.config.getoption("--jkbuildid")
        jkjobname=session.config.getoption("--jkjobname")
        if jkbuildid!=-1 and jkjobname:
            #print('update test collection to mysql, jobname: {}, buildid: {}'.format(jkjobname,jkbuildid))
            try:
                from localplugins.mysql_opr import query_pymysql
                
                fpath=os.path.join(BASE_DIR,'localplugins','resources', 'mysql_qa.json')
                
                #print('fpath :',fpath)
                f=open(fpath, 'r', encoding='utf-8')
                dbinfo = json.loads(f.read())
                
                sql='''
                UPDATE ui_autotest_collections SET fail_total={},pass_total={},skip_total={},error_total={},run_total={},
                duration='{}',is_end=1
                WHERE jk_jobname='{}' AND jk_buildid='{}'
                '''.format(self.failed,self.passed,self.skipped,self.errors,numtests,test_duration,jkjobname,jkbuildid)
                #print('update uitest_collect: ',sql)
                query_pymysql(dbinfo['host'],dbinfo['user'],dbinfo['password'],dbinfo['port'],'qateam',sql)
                #print('.......update test collection to mysql <uitest_collect>......',time.strftime('%Y-%m-%d %H:%M:%S'))
            except Exception as e:
                print('[Exception<updating to uitest_collect>]',end='')
                #print('Exception when updating test collection to mysql: ',e)

        self.style_css = pkg_resources.resource_string(
            __name__, os.path.join('resources', 'style.css'))
        #print()
        #print('sytle_css path: ',os.path.join('resources', 'style.css'))
        if PY3:
            self.style_css = self.style_css.decode('utf-8')

        if ANSI:
            ansi_css = [
                '\n/******************************',
                ' * ANSI2HTML STYLES',
                ' ******************************/\n']
            ansi_css.extend([str(r) for r in style.get_styles()])
            self.style_css += '\n'.join(ansi_css)

        # <DF> Add user-provided CSS
        for path in self.config.getoption('css') or []:
            self.style_css += '\n/******************************'
            self.style_css += '\n * CUSTOM CSS'
            self.style_css += '\n * {}'.format(path)
            self.style_css += '\n ******************************/\n\n'
            with open(path, 'r') as f:
                self.style_css += f.read()

        css_href = '{0}/{1}'.format('assets', 'style.css')
        html_css = html.link(href=css_href, rel='stylesheet',
                             type='text/css')
        if self.self_contained:
            html_css = html.style(raw(self.style_css))

        head = html.head(
            html.meta(charset='utf-8'),
            html.title('Test Report'),
            html_css)

        class Outcome:

            def __init__(self, outcome, total=0, label=None,
                         test_result=None, class_html=None):
                self.outcome = outcome
                self.label = label or outcome
                self.class_html = class_html or outcome
                self.total = total
                self.test_result = test_result or outcome

                self.generate_checkbox()
                self.generate_summary_item()

            def generate_checkbox(self):
                checkbox_kwargs = {'data-test-result':
                                   self.test_result.lower()}
                if self.total == 0:
                    checkbox_kwargs['disabled'] = 'true'

                self.checkbox = html.input(type='checkbox',
                                           checked='true',
                                           onChange='filter_table(this)',
                                           name='filter_checkbox',
                                           class_='filter',
                                           hidden='true',
                                           **checkbox_kwargs)

            def generate_summary_item(self):
                self.summary_item = html.span('{0} {1}'.
                                              format(self.total, self.label),
                                              class_=self.class_html)
        '''
        outcomes = [Outcome('passed', self.passed),
                    Outcome('skipped', self.skipped),
                    Outcome('failed', self.failed),
                    Outcome('error', self.errors, label='errors'),
                    Outcome('xfailed', self.xfailed,
                            label='expected failures'),
                    Outcome('xpassed', self.xpassed,
                            label='unexpected passes')]
        '''
        outcomes = [Outcome('passed', self.passed, label='成功'),
            Outcome('skipped', self.skipped, label='过滤掉'),
            Outcome('failed', self.failed, label='失败'),
            Outcome('error', self.errors, label='报错'),
            #Outcome('xfailed', self.xfailed,label='预期为失败'),
            #Outcome('xpassed', self.xpassed,label='预期为成功')
            ]
        if self.rerun is not None:
            outcomes.append(Outcome('rerun', self.rerun,label='再次执行'))
        
        '''
        summary = [html.p(
            '{0} tests ran in {1:.2f} seconds. '.format(
                numtests, suite_time_delta)),
            html.p('(Un)check the boxes to filter the results.',
                   class_='filter',
                   hidden='true')]
        '''
        summary_thead = [
            html.th('失败'),
            html.th('总共'),
            html.th('成功'),
            html.th('过滤'),
            html.th('报错')]
        
        summary_tbody = [
            html.td(self.failed,class_='red'),
            html.td(numtests),
            html.td(self.passed),
            html.td(self.skipped),
            html.td(self.errors,style='color:red;')]
        
#         summary_table = [
#             html.table([
#                 html.thead(
#                     html.tr(summary_thead),
#                     id='results-table-head'
#                 ),
#                 html.tbody(html.tr(summary_tbody))
#             ], 
#             class_='table-50')
#         ]
        summary = [
            html.p('总共 {0} 个用例，总耗时： {1:.2f} 秒. '.format(
                numtests, suite_time_delta)),
            html.table([
                html.thead(
                    html.tr(summary_thead),
                    id='results-summary'
                ),
                html.tbody(html.tr(summary_tbody))
                ], 
                class_='table-350')
            ]    
        '''
        summary = [
            html.p('总共 {0} 个用例，总耗时： {1:.2f} 秒. '.format(
                numtests, suite_time_delta)),
            html.table([
                html.thead(
                    html.tr(summary_thead),
                    id='results-summary'
                ),
                html.tbody(html.tr(summary_tbody))
                ], 
                class_='table-50'),
            html.p('勾选/取消勾选 复选框来过滤测试结果.',
                   class_='filter',
                   hidden='true')
            ]    
        for i, outcome in enumerate(outcomes, start=1):
            summary.append(outcome.checkbox)
            summary.append(outcome.summary_item)
            if i < len(outcomes):
                summary.append(', ')
        
        cells = [
            html.th('Result',
                    class_='sortable result initial-sort',
                    col='result'),
            html.th('Test', class_='sortable', col='name'),
            html.th('Duration', class_='sortable numeric', col='duration'),
            html.th('Links')
            ]
        '''
        cells = [
            html.th('用例状态',
                    class_='sortable result initial-sort',
                    col='result'),
            html.th('用例功能描述', col='description'),
            html.th('测试用例', class_='sortable', col='name'),
            html.th('运行耗时', class_='sortable numeric', col='duration')
            #,html.th('链接')
            ]
        
        session.config.hook.pytest_html_results_table_header(cells=cells)
        
        '''
        results = [html.h2('Results'), html.table([html.thead(
            html.tr(cells),
            html.tr([
                html.th('No results found. Try to check the filters',
                        colspan=len(cells))],
                    id='not-found-message', hidden='true'),
            id='results-table-head'),
            self.test_logs], id='results-table')]
        '''
        results = [
            html.h2('测试结果'), 
            html.table([html.thead(
                html.tr(cells),
                html.tr([html.th('没有用例，请检查过滤条件',colspan=len(cells))],
                    id='not-found-message', hidden='true'),
                id='results-table-head'),
                self.test_logs
                ], id='results-table',class_='table')
        ]
        
        #print('self.test_logs: ',self.test_logs)
        
        main_js = pkg_resources.resource_string(
            __name__, os.path.join('resources', 'main.js'))
        if PY3:
            main_js = main_js.decode('utf-8')
        
        
        '''***********************************gql***************************************
            html.h1(os.path.basename(session.config.option.htmlpath)),
            html.p('Report generated on {0} at {1} by '.format(
                generated.strftime('%d-%b-%Y'),
                generated.strftime('%H:%M:%S')),
                html.a('pytest-html', href=__pypi_url__),
                ' v{0}'.format(__version__)),
            # html 标题
        
        '''
        body = html.body(
            html.script(raw(main_js)),
            
            #html.h1(os.path.basename(session.config.option.htmlpath)),
            html.h1(self.htmlhead),
            
            html.p('测试报告运行于： {0} {1}'.format(
                    generated.strftime('%Y-%m-%d'),
                    generated.strftime('%H:%M:%S'))
                #,html.a('pytest-html', href='http://www.baidu.com/'),' v{0}'.format('2.11')
            ),
            onLoad='init()')
        
        '''***********************************gql***************************************
         body.extend(self._generate_environment(session.config))
        '''
        #body.extend(self._generate_environment(session.config))

        summary_prefix, summary_postfix = [], []
        session.config.hook.pytest_html_results_summary(
            prefix=summary_prefix, summary=summary, postfix=summary_postfix)
        
        '''***********************************gql***************************************
         body.extend([html.h2('Summary')] + summary_prefix
                    + summary + summary_postfix)
        '''
        #print('html-body-extend--summary: ',summary)
        
        body.extend(summary)
        body.extend(results)

        doc = html.html(head, body)

        unicode_doc = u'<!DOCTYPE html>\n{0}'.format(doc.unicode(indent=2))
        if PY3:
            # Fix encoding issues, e.g. with surrogates
            unicode_doc = unicode_doc.encode('utf-8',
                                             errors='xmlcharrefreplace')
            unicode_doc = unicode_doc.decode('utf-8')
        return unicode_doc

    def _generate_environment(self, config):
        if not hasattr(config, '_metadata') or config._metadata is None:
            return []

        metadata = config._metadata
        environment = [html.h2('Environment')]
        rows = []

        keys = [k for k in metadata.keys()]
        if not isinstance(metadata, OrderedDict):
            keys.sort()

        for key in keys:
            value = metadata[key]
            if isinstance(value, basestring) and value.startswith('http'):
                value = html.a(value, href=value, target='_blank')
            elif isinstance(value, (list, tuple, set)):
                value = ', '.join((str(i) for i in value))
            rows.append(html.tr(html.td(key), html.td(value)))

        environment.append(html.table(rows, id='environment'))
        return environment

    def _save_report(self, report_content):
        dir_name = os.path.dirname(self.logfile)
        assets_dir = os.path.join(dir_name, 'assets')

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        if not self.self_contained and not os.path.exists(assets_dir):
            os.makedirs(assets_dir)

        with open(self.logfile, 'w', encoding='utf-8') as f:
            f.write(report_content)
        if not self.self_contained:
            style_path = os.path.join(assets_dir, 'style.css')
            with open(style_path, 'w', encoding='utf-8') as f:
                f.write(self.style_css)

    def pytest_runtest_logreport(self, report):
        if report.passed:
            self.append_passed(report)
        elif report.failed:
            self.append_failed(report)
        elif report.skipped:
            self.append_skipped(report)
        else:
            self.append_other(report)

    def pytest_collectreport(self, report):
        if report.failed:
            self.append_failed(report)

    def pytest_sessionstart(self, session):
        self.suite_start_time = time.time()

    def pytest_sessionfinish(self, session):
        self.suite_finish_time = time.time()
        report_content = self._generate_report(session)
        self._save_report(report_content)

    def pytest_terminal_summary(self, terminalreporter):
        pass
        #terminalreporter.write_sep('-', 'generated html file: {0}'.format(self.logfile))