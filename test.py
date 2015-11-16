#coding:utf-8
import sys
from local_mutex import LocalMutex
import multiprocessing

def go():
    with LocalMutex('app.lock', wait = True):
        print 123
    
if __name__ == "__main__":
    task = []
    for i in xrange(5):
        t = multiprocessing.Process(target=go)
        t.start()
        task.append(t)
    for i in task:
        i.join()
    print 'end...'    
