# -*- coding: utf-8 -*-

from  PinterstDownloader import PinterstDownloader
from optparse import OptionParser

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-a", "--auth", dest="authKey", type="string",
                      help="AuthKey of app")
    parser.add_option("-p", "--path", dest="path", type="string",
                      help="Path to download images", default="../../img")
    parser.add_option("-q", "--query", dest="query", type="string",
                      help="Keyword to search Dashboard")
    parser.add_option("-u", "--userId", dest="userId", type="string",
                      help="User id")
    parser.add_option("-d", "--dashboard", dest="dashboard", type="string",
                      help="Dashboard name")

    (options, args) = parser.parse_args()
    downloader = PinterstDownloader(options.authKey, options.path)
    if (options.query != None):
        downloader.downloadForKey(options.query)
    elif (options.userId != None and options.dashboard != None):
        downloader.downloadFromBoard(downloader.makeBoardKey(options.userId, options.dashboard))
    else:
        parser.print_help()