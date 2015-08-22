# -*- coding: utf-8 -*-
import scrapy
import os
import json
import logging
import glob

#Serie name in json series file MUST match directory in filesystem 
dwnldir = "/home/kodi/Movies/"
seriesdir = "/home/kodi/Series/"

# https://github.com/tranqil/utwhisper

class DownloaderSpider(scrapy.Spider):
    name = "downloader"
    jsonfile = ""
    series_data = ""

    def __init__(self, series=None, *args, **kwargs):
        super(DownloaderSpider, self).__init__(*args, **kwargs)

        if (os.path.isfile('series.log')):
            statinfo = os.stat('series.log')
            if (statinfo.st_size > 10000000):
                os.remove('series.log')

        if (os.path.isfile('authreuse')):
            os.remove("authreuse")

        logger = logging.getLogger('downloader')
        logger.debug("**********************************")
        logger.debug("***** DownloaderSpider Start *****")
        logger.debug("**********************************")

        self.jsonfile = series
        with open(self.jsonfile, 'rwt') as file:
            self.series_data = json.load(file)
            file.close()

        for serie in self.series_data:
            if (serie["enabled"] == True):
                self.start_urls.append(serie["url"])
                logger.debug("*** url %s added for processing ***", serie["url"])

    def parse(self, response):

        logger.debug("**********************************")
        logger.debug("**** Start processing %s", response.url)
        logger.debug("**********************************")

        seriedata = []
        for serie in self.series_data:
            print(serie["url"])
            if (serie["url"] == response.url):
                seriedata = serie
                break

        if not seriedata:
            return

        logger.debug("**** serie selected for processing %s", seriedata["name"])

        nchapter = seriedata["chapter"]
        nchapter += 1

        schapter = ''
        if (nchapter < 10):
            schapter = '0'
        schapter += str(nchapter)

        logger.debug("**** searching link for season %s chapter %d", seriedata["season"], nchapter)

        smask_title = seriedata["title_mask"]
        smask_title = smask_title.replace("#2", schapter)
        smask_title = smask_title.replace('#1', str(seriedata["season"]))
        logger.debug("****   using title_mask %s", smask_title)

        smask_link = seriedata["link_mask"]
        smask_link = smask_link.replace("#2", schapter)
        smask_link = smask_link.replace('#1', str(seriedata["season"]))
        logger.debug("****   using link_mask %s and xpath_link %s", smask_link, seriedata["xpath_link"])

        found = False
        for sel in response.xpath(seriedata["xpath"]):

            if ('xpath_title' in seriedata and len(seriedata["xpath_title"]) > 0):

                title = sel.xpath(seriedata["xpath_title"]).extract()
                if (len(title) == 0 or title[0].find(smask_title) == -1):
                    logger.debug("****     xpath_title %s not found", seriedata["xpath_title"])
                    continue

                logger.debug("****     xpath_title %s matching title %s found", seriedata["xpath_title"], title[0])

            link = sel.xpath(seriedata["xpath_link"]).extract()

            if (len(link) == 0 or (len(smask_link) > 0 and link[0].find(smask_link) == -1)):
                logger.debug("****     not found in %s", link)
                continue

            #Prison break has malformed url. Check for a / at first position
            if (link[0][0] == '/'):
                link[0] = link[0][1:]

            if ('link_prefix' in seriedata and len(seriedata["link_prefix"]) > 0 and link[0].find(seriedata["link_prefix"]) == -1):
                link[0] = seriedata["link_prefix"] + link[0]

            logger.debug("****** sending link %s to donwload", link)

            scommand = 'python utwhisper/utwhisper.py --add-url '+link[0]
            os.system(scommand)
            found = True
            break

        if (found):
            seriedata['chapter'] = nchapter
            with open(self.jsonfile, 'wt') as file:
                json.dump(self.series_data, file)
                file.close()

        if ('file_mask' in seriedata and len(seriedata['file_mask']) > 0):

            file_mask = seriedata['file_mask']
            logger.debug("**** searching for files to move using file_mask %s", file_mask)

            for nnchapter in range(1, nchapter):
                
                file_to_move = ""

                sschapter = ''
                if (nnchapter < 10):
                    sschapter = '0'
                sschapter += str(nnchapter)

                file_mask = dwnldir + "*" + seriedata['file_mask'] + "*"
                file_mask = file_mask.replace("#2", sschapter)
                file_mask = file_mask.replace('#1', str(seriedata["season"]))

                logger.debug("Searching for files like '%s'", file_mask)

                for globfile in glob.glob(file_mask):
                    if (os.path.isdir(globfile)):
                        for filename in os.listdir(globfile):
                            logger.debug("Found file %s", filename)
                            if (".avi" in filename):
                                logger.debug("Found video file %s", filename)
                                file_to_move = globfile + "/" + filename
                                break
                            logger.debug("File %s doesn't end with '.avi' won't be moved", filename)
                    elif (os.path.isfile(globfile)):
                        file_to_move = globfile

                if (len(file_to_move) > 0):
                    src = file_to_move
                    dst_path = seriesdir + seriedata['name'] + "/Season " + str(seriedata["season"])
                    dst = dst_path + "/" + seriedata['name'] + "-" + str(seriedata["season"]) + sschapter + ".avi"
                    logger.debug("Trying to move %s to %s",src , dst)
                    if (os.path.isfile(dst)):
                        logger.debug("Cannot move %s to %s. Destination already exists", src, dst)
                    else:
                        try:
                            if not os.path.exists(dst_path):
                                logger.debug("Destination dir %s doesn't exist. Let's create it.", dst_path)
                                os.makedirs(dst_path)
                            os.rename(src, dst)
                            logger.debug("Moved %s to %s", src, dst)
                        except OSError:
                            logger.debug("Cannot move %s to %s. Errno = %d", src, dst, os.strerror(errno.errcode))

        logger.debug("**********************************")
        logger.debug("**** End processing %s", response.url)
        logger.debug("**********************************")
        logger.debug(" ")
        logger.debug(" ")

