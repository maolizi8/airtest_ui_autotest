"""
Created on 12 Jun 2019

@author: geqiuli
"""
import json
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("files_opr - BASE_DIR :",BASE_DIR)

def read_txt(file_name, subdir=""):
    if subdir:
        fpath=os.sep.join([BASE_DIR,"files",subdir,file_name]) + ".txt"
    else:
        fpath=os.sep.join([BASE_DIR,"files",file_name]) + ".txt"
    arr = []
    with open(fpath, mode="r", encoding="UTF-8") as f:
        for line in f.readlines():
            arr.append(line.strip())
    return arr

def read_json(file_name, subdir=""):
    if subdir:
        fpath=os.sep.join([BASE_DIR,"files",subdir,file_name]) + ".json"
    else:
        fpath=os.sep.join([BASE_DIR,"files",file_name]) + ".json"
    listCookies={}    
    with open(fpath, "r", encoding="utf-8") as f:
        listCookies = json.loads(f.read())
    return listCookies

def read_csv(file_name, subdir=""):
    if subdir:
        fpath=os.sep.join([BASE_DIR,"files",subdir,file_name]) + ".csv"
    else:
        fpath=os.sep.join([BASE_DIR,"files",file_name]) +  ".csv"
    arr=[]
    with open(fpath,"r", encoding="UTF-8") as f:
        reader=csv.DictReader(f)
        for row in reader:
            arr.append(row)
    return arr

def write_to_txt(file_name, content, subdir=""):
    """写入文本内容
    @param file_name: 文件名
    @param content: 要写入的内容，目前支持字符串和列表
    """
    if subdir:
        fpath=os.sep.join([BASE_DIR,"files",subdir,file_name]) + ".txt"
    else:
        fpath=os.sep.join([BASE_DIR,"files",file_name]) +  ".txt"
    if isinstance(content, str):
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content)
    elif isinstance(content, list):
        with open(fpath, "w", encoding="utf-8") as f:
            f.write("\n".join(content))
    
def add_to_txt(file_name, content,  subdir=""):
    """追加到文本内容
    @param file_name: 文件名
    @param content: 要写入的内容，目前支持字符串和列表
    """
    if subdir:
        fpath=os.sep.join([BASE_DIR,"files",subdir,file_name]) + ".txt"
    else:
        fpath=os.sep.join([BASE_DIR,"files",file_name]) +  ".txt"
    if isinstance(content, str):
        with open(fpath, "a", encoding="utf-8") as f:
            f.write(content+"\n")
    elif isinstance(content, list):
        with open(fpath, "a", encoding="utf-8") as f:
            f.write("\n".join(content))

def write_to_json(file_name, content, subdir=""):
    if subdir:
        fpath=os.sep.join([BASE_DIR,"files",subdir,file_name]) + ".json"
    else:
        fpath=os.sep.join([BASE_DIR,"files",file_name]) + ".json"
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(json.dumps(content))


def md5(s):
    import hashlib
    m = hashlib.md5()
    m.update(s.encode("utf-8"))
    return m.hexdigest()
    
if __name__=="__main__":
    pass
    