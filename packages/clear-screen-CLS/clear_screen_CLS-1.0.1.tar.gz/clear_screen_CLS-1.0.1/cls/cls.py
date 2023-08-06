'''
Clear Screen for all OS's - by don-batista!
CLS!
'''
#Modules
from __future__ import print_function
import sys
import os
import time

#Vars
system = sys.platform
python_version = sys.version[1]

def cls():
    if 'linux' in system:
        os.system("clear && printf '\e[3J'")
    elif 'windows' in system or 'Windows' in system:
        os.system("cls")
    else:
        n = '\n'*250
        print(n)

if __name__ == '__main__':
    print("Cleaning Screen!")
    time.sleep(0.5)
    cls()
