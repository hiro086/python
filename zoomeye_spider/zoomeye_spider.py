#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: ??
@author: hiro086
@contact: wangzw@nuaa.edu.cn
@file: spider_main.py
@time: 17/6/28 下午4:07
"""

import os
import requests
import json
import sys

access_token = ''
ip_list = []

def login():
    user = raw_input('[username]:')#email
    passwd = raw_input('[password]:')
    data = {
        'username':user,
        'password':passwd,
    }
    data_encoded = json.dumps(data)#dumps是将dict转化成str格式，loads是将str转化成dict格式。
    try:
        r = requests.post(url = 'https://api.zoomeye.org/user/login',data = data_encoded)
        r_decoded = json.loads(r.text)
        global  access_token
        access_token = r_decoded['access_token']

    except Exception:
        print '[info]:username or password is wrong'
        exit()

def savaStrToFile(file,str):
    with open(file,'w') as output:
        output.write(str)

def savaListToFile(file,list):
    s = '\n'.join(list)
    with open(file,'w') as output:
        output.write(s)

def apiTest():
    page = 1
    global access_token
    with open('access_token.txt','r') as input:
        access_token = input.read()
    headers = {'Authorization': unicode('JWT ' + access_token, "UTF-8"),} # 请求头以此来说明你有调用api的权限
    print headers
    while True:
        try:
            r = requests.get(url='https://api.zoomeye.org/host/search?query=app:"Hikvision IP camera httpd" country:"China"&page=' + str(page),headers = headers)
            r_decoded = json.loads(r.text)
            for x in r_decoded['matches']:
                resStr = x['ip']+ ':' + str(x['portinfo']['port'])+ '\t' + '[geoinfo]:'  +\
                 x['geoinfo']['city']['names']['en'] + ' ' + x['geoinfo']['country']['names']['en']+'\t' +\
                 '[lat-lon]:' + str(x['geoinfo']['location']['lat']) +' '+ str(x['geoinfo']['location']['lon'])

                # 我在此保存的信息有点多，仅供参考,注意字典中键值的类型，json格式参考下图
                print resStr
                ip_list.append(resStr)
            print '[info]count' + str(page * 10) #每页10ip
        except Exception,e:
            if str(e.message) == 'matches':
                print '[info]:' + 'account was break, exceeding the max limitations'
                break
            else:
                print '[info]:' + str(e.message)
        else:
            if page == 2:
                break
            page += 1

def main():
    if not os.path.isfile('access_token.txt'):
        print '[info]:access_token file is not exist, please login'
        login()
        savaStrToFile('access_token.txt',access_token)
    apiTest()
    savaListToFile('ip_list.txt',ip_list)

if __name__ == '__main__':
    main()

