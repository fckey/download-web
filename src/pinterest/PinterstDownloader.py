# -*- coding: utf-8 -*-

import json
import logging
import time, sys, os
import pickle

from common.RequestHandler import *
import datetime

PROCESSED_DUMP = "../../data/processed.dump"

PINTEREST_API_BASE_URL = "https://api.pinterest.com"


class PinterstDownloader():
    """Class to download Pinterest pictures"""

    def __init__(self, authKey, path):
        self.authKey = authKey
        self.basePath = path
        logger = logging.getLogger(u"PinterstDownloader")
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        self.logger = logger
        self.requestHandler = RequestHandler(logger)
        if(os.path.exists(PROCESSED_DUMP)):
            f = open(PROCESSED_DUMP, "r")
            self.processed = pickle.load(f)
            f.close()
        else:
            self.processed = {}

    def processApiResponse(self, response, path, func=(lambda x, y: sys.stdout.write("%s, %s ]\n" % (x, y)))):
        data = json.loads(response.read())
        images = data["data"]
        numImages = len(images)
        filepath = "%s%s" % (self.basePath, path)
        filepath = filepath.decode('utf-8')
        for content in images:
            pictureUrl = content["image"]["original"]["url"]
            func(filepath, [pictureUrl])
            time.sleep(1)
        return numImages, data["page"]["next"]

    def downloadFromBoard(self, boardkey):
        url = "%s/v1/boards%spins/?access_token=%s&fields=image" % (PINTEREST_API_BASE_URL, boardkey, self.authKey)

        num = 0
        while (True):
            self.logger.debug("Getting data from: %s" % url)
            apiResponse = self.requestHandler.getForUrl(url)
            numImages, nextPage = self.processApiResponse(apiResponse, boardkey, func=self.requestHandler.urlDownload)
            num += numImages
            if (nextPage == None):
                break
            url = nextPage
        self.logger.info("Downloaded %d images for %s" % (num, boardkey))
        return num

    def downloadForKey(self, keyword):
        url = "https://www.pinterest.com/search/boards/?q=%s" % keyword
        soup = self.requestHandler.makeSoup(url)
        boards = soup.find_all(attrs={"class": "boardLinkWrapper"})
        self.logger.info("Found %d boards for %s" % (len(boards), keyword))
        try:
            for node in boards:
                boardKey = node.get("href")
                if (self.processed.has_key(boardKey)):
                    self.logger.info("%s was already processed. Skipping." %boardKey)
                    continue
                self.downloadFromBoard(boardKey)
                self.processed[boardKey] = datetime.date.today()
        finally:
            f = open(PROCESSED_DUMP, "w")
            pickle.dump(self.processed, f)
            f.close()

        return

    def makeBoardKey(self, userId, boardName):
        return "/%s/%s/" % (userId, boardName)


if __name__ == '__main__':
    exit(0)
