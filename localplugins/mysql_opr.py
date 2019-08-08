'''
Created on 2019年4月22日

@author: geqiuli
'''
import pymysql as ms


def query_mysql(host,user,password,port,database,sql):
    '''执行mysql语句，执行完会关闭连接'''
    rsp_data={}
    try:
        conn=ms.connect(
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
        cursor=conn.cursor()
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
        else:
            result=None
        conn.commit()
        rsp_data["code"]=0
        rsp_data["msg"]=None
        rsp_data["data"]=result
        rsp_data["rows"]=count
        #return rsp_data 
    except Exception as e:
        msg=("SQL执行异常：%s" % e)
        rsp_data["code"]=1
        rsp_data["msg"]=msg
        rsp_data["data"]=None
        rsp_data["rows"]=0
        #return rsp_data 
              
    finally:
        print("关闭连接")
        conn.close()
        print(rsp_data)
        return rsp_data   
    
def get_connection(serverip, port, db_name, account, password):
    """
    @param flat: 0-使用脚本中的ip，1-使用数据库中的ip"""
    print("serverip: ",serverip)
    conn=ms.connect(
        host = serverip,
        port = int(port),
        user = account,
        password = password,
        database = db_name,
        charset = "utf8mb4",
        cursorclass=ms.cursors.DictCursor)       
    
    return conn 

def get_connection_qadb(db_name):
    """yyw-qa 的数据库"""
    from public import files
    datainfo=files.read_json('mysql-qa', 'mysql')
    #print("datainfo: ",datainfo)
    conn=ms.connect(
        host = datainfo['host'],
        port = int(datainfo['port']),
        user = datainfo['user'],
        password = datainfo['password'],
        database = db_name,
        charset = "utf8mb4",
        cursorclass=ms.cursors.DictCursor)       
    
    return conn 

def select_from_mysql(conn,sql,total=0,close=False):
    '''select语句
    @param total: 0：全部, 1：返回一条, >1:返回指定的多少条
    @return: rsp_data: code(0-成功，1-失败)'''
    rsp_data={}
    if sql[:6].lower()!="select":
        rsp_data["code"]=1
        rsp_data["msg"]="该方法只支持select语句"
        rsp_data["data"]=None
        rsp_data["rows"]=0
        return rsp_data
    
    cursor=conn.cursor() 
    try:
        count=cursor.execute(sql)
        if total==0:
            result=cursor.fetchall() #list - N条记录
        elif total==1:
            result=cursor.fetchone() #tuple - 1条记录
        else:
            result=cursor.fetchmany(total) #list - total条记录
        conn.commit()
        rsp_data["code"]=0
        rsp_data["msg"]=None
        rsp_data["data"]=result
        rsp_data["rows"]=count
        #return rsp_data 
    except Exception as e:
        msg=("SQL执行异常：%s" % e)
        rsp_data["code"]=1
        rsp_data["msg"]=msg
        rsp_data["data"]=None
        rsp_data["rows"]=0 
    finally:
        if close==True:
            print("关闭mysql连接")
            conn.close()
        print('excute mysql code:',rsp_data["code"])
        return rsp_data    

def query_mysql2(conn,sql,total=100,close=False):
    """
    @param total: 0：全部, 1：返回一条, >1:返回指定的多少条
    @return: rsp_data{code,msg,data}, code：0-正常，1-异常；
    """
    rsp_data={}
    try:
        cursor=conn.cursor()
        try:
            count=cursor.execute(sql)
            #result=cursor.fetchall()
            if sql[:6].lower()=="select":
                if total==0:
                    result=cursor.fetchall() #list - N条记录
                elif total==1:
                    result=cursor.fetchone() #tuple - 1条记录
                else:
                    result=cursor.fetchmany(total) #list - total条记录
            elif sql[:4].lower()=="show":
                result=cursor.fetchall()
            elif sql[:4].lower()=="desc":
                result=cursor.fetchall()
            else:
                result=None
            conn.commit()
            rsp_data["code"]=0
            rsp_data["msg"]=None
            rsp_data["data"]=result
            rsp_data["rows"]=count
            #return rsp_data 
        except Exception as e:
            msg=("SQL执行异常：%s" % e)
            rsp_data["code"]=1
            rsp_data["msg"]=msg
            rsp_data["data"]=None
            rsp_data["rows"]=0
            #return rsp_data 
              
    finally:
        if close==True:
            print("关闭mysql连接")
            conn.close()
        print('excute mysql code:',rsp_data["code"])
        if rsp_data["code"]==1:
            print('excute mysql error:',rsp_data["msg"])
        return rsp_data 

def query_mysql3(host,user,password,port,database,sql):
    '''执行mysql语句，执行完会关闭连接'''
    rsp_data={}
    try:
        conn=ms.connect(
            host=host,
            user=user,
            port=port,
            passwd=password,
            database=database,
            charset = "utf8mb4",
            cursorclass=ms.cursors.DictCursor
        )
    except Exception as e:
        msg=("获取数据库连接失败：%s" % e)
        rsp_data["code"]=1
        rsp_data["msg"]=msg
        rsp_data["data"]=None
        rsp_data["rows"]=0
        return rsp_data
    
    try:
        cursor=conn.cursor()
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
        else:
            result=None
        conn.commit()
        rsp_data["code"]=0
        rsp_data["msg"]=None
        rsp_data["data"]=result
        rsp_data["rows"]=count
        #return rsp_data 
    except Exception as e:
        msg=("SQL执行异常：%s" % e)
        rsp_data["code"]=1
        rsp_data["msg"]=msg
        rsp_data["data"]=None
        rsp_data["rows"]=0
        #return rsp_data 
              
    finally:
        print("关闭连接")
        conn.close()
        print(rsp_data)
        return rsp_data   

if __name__ == '__main__':
    pass