'''
Created on 2019年7月19日

@author: geqiuli
'''
from airtest.cli.runner import run_air_batch_mode
import os
import pytest

proj_root = os.path.dirname(os.path.abspath(__file__))
print('test_airtest_cases>proj_root :',proj_root)


@pytest.mark.run_case
def test_run_airtest_cases(): 
    #device = ['android:///'] #不指定则默认使用第一个
    device = ['Android://127.0.0.1:5055/46709b100104']
    #device = ['Android://127.0.0.1:5055/02157df271610a1b']
    run_air_batch_mode(device, proj_root, 'testcases1',f_type='.air')
 
if __name__ == '__main__':
    args=[__file__,'-m run_case','-s']
    pytest.main(args)
