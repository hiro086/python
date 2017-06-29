#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2,re
import requests
from bs4 import BeautifulSoup

def get_ip_address(ip):
    if ip is None:
        return u'未知'

    def extract(content):
        """从网页内容中提取地理位置
        :Parameters:
          --content：过滤后的网页内容
        """
        try:
            return content[content.find("：") + 1:len(content)].split(" ")[0]
        except:
            print("No area by given address")
            return "China"

    query = requests.get("http://www.ip138.com/ips138.asp", {"ip": ip})
    #solution1
    #print(query.url,eval(query.content))
    result = BeautifulSoup(query.content,'lxml').find("ul", {"class": "ul1"})
    print(result,"\n===\n",BeautifulSoup(query.content,'lxml'))
    return extract(result.find("li").text)

    #solution2
    # query.encoding='GB2312'
    # if query.status_code==200:
    #     print("SUCCESSFUL")
    #     print(query.text[7000:-1600])
    # else:
    #     print("ERROR! ERROR CODE IS"+str(query.status_code))

    # solution3
    content = query.content.decode("utf-8")
    # myMatch = re.search(r'<td align="center"><ul class="ul1"><li>(.*?)</li></ul></td>', html, re.S)
    myMatch = re.search(r'<td align="center"><ul class="ul1"><li>(.*?)</li>', content, re.S)
    tmp_str = myMatch.group(1)
    tmp_str = tmp_str.replace(u'本站主数据：', '')
    tmp_str = line.strip('\r\n') + " , " + tmp_str
    print tmp_str
if __name__ == "__main__":
    f = open('ip_list.txt', 'r')
    line = f.readline()
    while line:
        ip = line.strip()
        print ip
        print get_ip_address(ip)
    f.close()
