# -*- coding: utf-8 -*-

import urllib2
import urllib
from bs4 import BeautifulSoup
import os
import sys

class RequestHandler:
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2725.0 Safari/537.36'}

    def __init__(self, logger):
        self.logger = logger

    def makeSoup(self, url):
        res = self.getForUrl(url)
        soup = BeautifulSoup(res, "lxml")

        return soup

    def getForUrl(self, url):
        req = urllib2.Request(url, headers=self.HEADERS)
        res = urllib2.urlopen(req)
        return res

    def urlDownload(self, path, urls):
        self.logger.info("Download Start...")
        if os.path.exists(path) == False:
            os.makedirs(path)

        opener = urllib2.build_opener()
        count = 0
        for url in urls:
            try:
                # fn, ext = os.path.splitext(url)
                filename = url.split("/")[-1]
                req = urllib2.Request(url, headers=self.HEADERS)
                imgFile = open( "%s%s" % (path, filename), "wb")  # 画像データの保存
                imgFile.write(opener.open(req).read())
                imgFile.close()
                count += 1
                self.logger.debug("DL Image Link: %s" %url )
            except :
                self.logger.warn("Fail to download for %s" %url)
                self.logger.warn(sys.exc_info()[0])
                continue
        return count


                
                
if __name__ == '__main__':
    exit(0)