import subprocess
import sys
import os

# Some code here

for i in range (101,200, 1):
    tmp = "ping -c 5 192.168.10."+str(i)
    os.system(tmp)  
