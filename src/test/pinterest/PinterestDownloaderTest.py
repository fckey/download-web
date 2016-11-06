# -*- coding: utf-8 -*-

import os, sys, unittest
from pinterest.PinterstDownloader import PinterstDownloader

class PinterestDownloaderTest(unittest.TestCase):
    def setUp(self):
        self.downloader = PinterstDownloader("key", "path")
        self.testdata = """
        {"data": [
            {"image": {"original": {"url": "https://s-media-cache-ak0.pinimg.com/originals/1f/94/12/test1.jpg", "width": 525, "height": 719}}, "id": "1"},
            {"image": {"original": {"url": "https://s-media-cache-ak0.pinimg.com/originals/67/00/0b/test2.jpg", "width": 1080, "height": 1350}}, "id": "2"},
            {"image": {"original": {"url": "https://s-media-cache-ak0.pinimg.com/originals/b3/20/0f/test3.jpg", "width": 1000, "height": 1003}}, "id": "3"}
            ],
        "page": {"cursor": "CURSOR",
                 "next": "https://api.pinterest.com/v1/boards/userId/boardName/pins/?access_token=ACCESS_TOKEN&fields=image&cursor=CURSOR"}
        }
        """

    def testProcessApiResponse(self):
        numImages, next = self.downloader.processApiResponse(self.testdata, "fckey/test")
        self.assertEqual(3, numImages)
        self.assertEqual("https://api.pinterest.com/v1/boards/userId/boardName/pins/?access_token=ACCESS_TOKEN&fields=image&cursor=CURSOR",next)
