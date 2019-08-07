'''
Created on 2019年4月22日

@author: geqiuli
'''
import time


def query_pymysql(host,user,password,port,database,sql):
    '''执行mysql语句'''
    rsp_data={}
    try:
        import pymysql
        #print('连接mysql',time.strftime('%Y-%m-%d %H:%M:%S'))
        conn=pymysql.connect(
            host=host,
            user=user,
            port=port,
            passwd=password,
            database=database,
            charset="utf8"
        )
    except Exception as e:
        msg=("获取数据库连接失败：%s" % e)
        print("[MySQL.ConnectionError]",end='')
        rsp_data["code"]=1
        rsp_data["msg"]=msg
        rsp_data["data"]=None
        rsp_data["rows"]=0
        return rsp_data
    try:
        #print('mysql游标：',time.strftime('%Y-%m-%d %H:%M:%S'))
        cursor=conn.cursor()
        if sql[:5].lower()=="insert":
            sql=pymysql.escape_string(sql)
        
        #print('start execute sql：',time.strftime('%Y-%m-%d %H:%M:%S')) 
        count=cursor.execute(sql)
        #result=cursor.fetchall()
        if sql[:6].lower()=="select":
            result=cursor.fetchall()
            #print(result)
            #print(type(result))
        elif sql[:4].lower()=="show":
            result=cursor.fetchall()
        elif sql[:4].lower()=="desc":
            result=cursor.fetchall()
        elif sql[:5].lower()=="insert":
            #print('插入{}条数据'.format(cursor.rowcount))
            result=cursor.fetchall()
        else:
            result=None
        conn.commit()
        #print('[MySQL-excute]',end='')
        #print('commit sql after execution: ',time.strftime('%Y-%m-%d %H:%M:%S'))
        rsp_data["code"]=0
        rsp_data["msg"]=None
        rsp_data["data"]=result
        rsp_data["rows"]=count
        #return rsp_data 
    except Exception as e:
        msg=("[MySQL.ExecutionError：%s]" % e)
        print(msg,end='')
        rsp_data["code"]=1
        rsp_data["msg"]=msg
        rsp_data["data"]=None
        rsp_data["rows"]=0
    finally:
        #print("close MySQL connection:",time.strftime('%Y-%m-%d %H:%M:%S'))
        conn.close()
        #print(rsp_data)
        return rsp_data    

def query_many_pymysql(host,user,password,port,database,*sql):
    '''执行mysql语句'''
    rsp_data={"msg":""}
    try:
        import pymysql
        #print('连接mysql',time.strftime('%Y-%m-%d %H:%M:%S'))
        conn=pymysql.connect(
            host=host,
            user=user,
            port=port,
            passwd=password,
            database=database,
            charset="utf8"
        )
    except Exception as e:
        msg=("获取数据库连接失败：%s" % e)
        print("[MySQL.ConnectionError]",end='')
        rsp_data["code"]=1
        rsp_data["msg"]=msg
        rsp_data["data"]=None
        rsp_data["rows"]=0
        return rsp_data
    try:
        cursor=conn.cursor()
        rsp_data["code"]=0
        rsp_data["msg"]=''
        rsp_data["data"]=[]
        rsp_data["rows"]=0
        for s in sql:
            if s[:5].lower()=="insert":
                s=pymysql.escape_string(s)
            if s:
                count=cursor.execute(s)
                result=cursor.fetchall()
                conn.commit()
                #print('[MySQL-excute]',end='')
                rsp_data["data"].append(result) 
                rsp_data["rows"]+=count
    except Exception as e:
        msg=("[MySQL.ExecutionError：%s]" % e)
        print(msg,end='')
        rsp_data["code"]=1
        rsp_data["msg"]=msg
        rsp_data["data"]=''
        rsp_data["rows"]=0
    finally:
        #print("close MySQL connection:",time.strftime('%Y-%m-%d %H:%M:%S'))
        conn.close()
        #print(rsp_data)
        return rsp_data 


def query_mysql_transaction(host,user,password,port,database,sql):
    '''使用事务执行mysql语句'''
    rsp_data={}
    
    try:
        import mysql.connector
        print('连接mysql',time.strftime('%Y-%m-%d %H:%M:%S'))
        conn=mysql.connector.connect(
            host=host,
            user=user,
            port=port,
            passwd=password,
            database=database
        )
    except Exception as e:
        msg=("获取数据库连接失败：%s" % e)
        rsp_data["code"]=1
        rsp_data["msg"]=msg
        rsp_data["data"]=None
        rsp_data["rows"]=0
        return rsp_data
    try:
        print('mysql事务：',time.strftime('%Y-%m-%d %H:%M:%S'))
        conn.start_transaction()
        cursor=conn.cursor()
        print('开始执行sql语句：',time.strftime('%Y-%m-%d %H:%M:%S'))
        count=cursor.execute(sql)
        #result=cursor.fetchall()
        if sql[:6].lower()=="select":
            result=cursor.fetchall()
            #print(result)
            #print(type(result))
        elif sql[:4].lower()=="show":
            result=cursor.fetchall()
        elif sql[:4].lower()=="desc":
            result=cursor.fetchall()
        elif sql[:5].lower()=="insert":
            print('插入{}条数据'.format(cursor.rowcount))
        else:
            result=None
        conn.commit()
        print('执行并commit sql语句',time.strftime('%Y-%m-%d %H:%M:%S'))
        rsp_data["code"]=0
        rsp_data["msg"]=None
        rsp_data["data"]=result
        rsp_data["rows"]=count
    except Exception as e:
        msg=("SQL执行异常：%s" % e)
        rsp_data["code"]=1
        rsp_data["msg"]=msg
        rsp_data["data"]=None
        rsp_data["rows"]=0
    finally:
        print("关闭MySQL连接")
        conn.close()
        print(rsp_data)
        return rsp_data  
    

def query_mysql(host,user,password,port,database,sql):
    '''执行mysql语句'''
    rsp_data={}
    try:
        import mysql.connector
        conn=mysql.connector.connect(
            host=host,
            user=user,
            port=port,
            passwd=password,
            database=database
        )
    except Exception as e:
        msg=("获取数据库连接失败：%s" % e)
        rsp_data["code"]=1
        rsp_data["msg"]=msg
        rsp_data["data"]=None
        rsp_data["rows"]=0
        return rsp_data
    
    if sql.count(";")>1:
        rsp_data["code"]=0
        rsp_data["msg"]="暂时只支持单条sql语句"
        rsp_data["data"]=None
        rsp_data["rows"]=0
        return rsp_data
     
    try:
        cursor=conn.cursor()
        print('开始执行sql语句：',time.time())
        count=cursor.execute(sql)
        #result=cursor.fetchall()
        if sql[:6].lower()=="select":
            result=cursor.fetchall()
            #print(result)
            #print(type(result))
        elif sql[:4].lower()=="show":
            result=cursor.fetchall()
        elif sql[:4].lower()=="desc":
            result=cursor.fetchall()
        elif sql[:5].lower()=="insert":
            print('插入{}条数据'.format(cursor.rowcount))
        else:
            result=None
        conn.commit()
        print('执行并commit sql语句',time.time())
        rsp_data["code"]=0
        rsp_data["msg"]=None
        rsp_data["data"]=result
        rsp_data["rows"]=count
    except Exception as e:
        msg=("SQL执行异常：%s" % e)
        rsp_data["code"]=1
        rsp_data["msg"]=msg
        rsp_data["data"]=None
        rsp_data["rows"]=0
    finally:
        print("关闭MySQL连接")
        conn.close()
        print(rsp_data)
        return rsp_data   


   
 
if __name__ == '__main__':
    sql1='''INSERT INTO uitest_collect_copy(htmlhead,jk_jobname,jk_buildid,fpath,tests_count)
            VALUES('{0}','{1}','{2}','{3}','{4}')
            '''.format('htmlhead','jkjobname',2,'fspath',2)
    sql2='''INSERT INTO uitest_collect_copy(htmlhead,jk_jobname,jk_buildid,fpath,tests_count)
            VALUES('{0}','{1}','{2}','{3}','{4}')
            '''.format('htmlhead','jkjobname',3,'fspath',3)
    sql3=''
    r=query_many_pymysql("yyw-0345","qauser","qa_123456",3306,'qateam',sql1,sql2,sql3)
    print(r)