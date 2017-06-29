#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: hiro086
@contact: wangzw@nuaa.edu.cn
@file: extract_msg.py
@time: 17/6/29 下午5:06
"""
import threading
import requests
import Queue
import sys
import re

def Threads():
    threadlist = []
    queue = Queue.Queue()
    for ip in open('result1.txt','r'):
        queue.put(ip.replace('\n',''))
    for x in range(0,10):
        th = threading.Thread(target=pri_lines,args=(queue,))
        threadlist.append(th)
    for t in threadlist:
        t.start()
    for t in threadlist:
        t.join()

def pri_lines(queue):
    while not queue.empty():
        lines = queue.get()
        try:
            lines = lines.strip()
            if lines.endswith(' 200'):
                print lines
        except:
            continue

if __name__ == '__main__':
    print "Extract message ..."
    Threads()
