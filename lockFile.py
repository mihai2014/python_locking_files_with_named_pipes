from __future__ import print_function

import os, time, signal

class lockFile(object):
    """ locking file mechanism using named pipe"""

    def __init__(self, path):
        path = path + "-lock"

        if not os.path.exists(path):
            os.mkfifo(path)

        self.state = os.open(path, os.O_RDWR | os.O_NONBLOCK)

        #init: 0 : unlocked state
        os.write(self.state, '0'.encode())

    def lock(self):
        try:
            # empty the pipe => locked state
            os.read(self.state, 1)
            return True
        except OSError:
            # pipe is empty : resource temporarily unavailable
            return False

    def unlock(self):
        # write to the pipe => unlocked state
        os.write(self.state, '0'.encode())

    def handler(self, signum, frame):
        # timeout signal handler
        self.stop = True

    def access(self, code , *args):
        # writing file using code and unlocks the file

        # setting a timeout for waiting the release of locking
        self.time = 5
        self.stop = False
        signal.signal(signal.SIGALRM, self.handler)
        signal.alarm(self.time)

        while True:
            # waiting for unlock
            if (self.lock()):
                break
            # timeout elapsed
            if self.stop:
                return False

        # access file
        code(args)

        self.unlock()
        return True

if __name__ == "__main__":
    print("This is a test")

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



