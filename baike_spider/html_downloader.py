#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import urllib2
class HtmlDownloader(object):
    def download(self,url):
        if url is None:
            return None

        respon = urllib2.urlopen(url)

        if respon.getcode() != 200:
            return None
        return respon.read()