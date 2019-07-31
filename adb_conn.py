'''
Created on 2019年7月30日

@author: geqiuli
'''
import subprocess
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print('BASE_DIR :',BASE_DIR)


def init_cmdrun_adb(device, port='5555'):
    adb_path=os.path.join(BASE_DIR,'airtest','core','android','static','adb','windows','adb.exe')
    print('adb_path :',adb_path)
    cmd_str=adb_path +' -P ' + port +' -s '+device
    print('command: ',cmd_str)
    subprocess.run(cmd_str)

def init_AirtestIDE_adb(device, ide_dir, port='5037'):
    '''
    @param ide_dir: AirtestIDE的目录，
    【注意】windows下，目录分隔符：两个斜杠 \\ 或者反斜杠/ 或者r转义的单个斜杠，
    即：E:\\AirtestIDE  或 E:/AirtestIDE
    但是，不能是单个斜杠
    '''
    ide_dir = ide_dir.replace('/', '\\')
    adb_path=os.path.join(ide_dir,'airtest','core','android','static','adb','windows','adb.exe')
    print('adb_path :',adb_path)
    cmd_str=adb_path +' -P ' + port +' -s '+device
    print('command: ',cmd_str)
    subprocess.run(cmd_str)
    #subprocess.run(cmd_str, shell=True, check=True)
     
if __name__ == '__main__':
    #init_cmdrun_adb('46709b100104')
    #init_AirtestIDE_adb('02157df271610a1b', 'E:\\AirtestIDE')
    init_AirtestIDE_adb('46709b100104', 'E:\\AirtestIDE')
