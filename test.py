from __future__ import print_function
import os, time
from lockFile import lockFile

def modif(args):
    fileName = args[0]
    try:
        fo = open(fileName,"r+")
    except:
        print(fileName, "does not exist")
    l = len(fo.readlines())
    lines = str(l + 1)    
    fo.write(lines + "\n")
    fo.close()
    print("pid {} write: {}".format(os.getpid(),lines))

#fileName = '1.txt'
#string = "my string"
#lock = lockFile(fileName)
#this writes and unlocks the file
#default timeout for waiting release lock is 5 sec
#success = lock.access(modif, fileName, string, 3)
#print(success)

def child(lock, t_sec):

    for n in range(10):
        success = lock.access(modif, "1.txt")
        if(not success):
            print("pid {} error: can't write file".format(os.getpid()))
            os._exit(1)
        time.sleep(t_sec + 1)

    print("child ", os.getpid(), "end")
    os._exit(0)

def parent():
    # creating new file
    f = open('1.txt','w')
    f.close()

    lock = lockFile("1.txt")

    children = []
    for n in range(3):
        pid = os.fork()
        if pid == 0:
            child(lock,n)
        else:
            print("parent:", os.getpid(), "has a child :", pid)
            children.append(pid)

    for p in children:
        os.waitpid(p,0)

    print("All children stops. Parent end.")

parent()
