from sre_constants import SUCCESS
import pymysql
import os
import sys

def cur():
    for i in range(5):
        print(i)
        if i==3:
            sys.exit()

if __name__=='__main__':
    cur()
    print('SUCCESS')