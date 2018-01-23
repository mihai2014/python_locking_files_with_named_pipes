Python locking files using named pipes

Testing:
    python lockFile.py
    python test.py

Example usage:

from __future__ import print_function
import os
from lockFile import lockFile

def modif(fileName,string):
    try:
        fo = open(fileName,"a")
        fo.write(string)
        fo.close()
    except:
        print(fileName, "does not exist")

# creating new file
f = open('1.txt','w')
f.close()

fileName = '1.txt'
string = "my string\n"
lock = lockFile(fileName)
#this writes and unlocks the file
#default timeout for waiting release lock is 5 sec
success = lock.access(modif, fileName, string)
print(success)

