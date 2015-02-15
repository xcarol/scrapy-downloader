# -*- coding: utf-8 -*-
import scrapy
import os
import json
import logging

#Serie name in json series file MUST match directory in filesystem 
dwnldir = "/home/xavi/Movies/"
seriesdir = "/home/xavi/Series/"

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

        FORMAT = '%(asctime)-15s %(message)s'
        logging.basicConfig(filename='series.log',level=logging.DEBUG,format=FORMAT)
        logging.debug("")
        logging.debug("**")
        logging.debug("****")
        logging.debug("******")

        self.jsonfile = series
        with open(self.jsonfile, 'rwt') as file:
            self.series_data = json.load(file)
            file.close()

        for serie in self.series_data:
            if (serie["enabled"] == "True"):
                self.start_urls.append(serie["url"])
                logging.debug("*** added url = %s", serie["url"])

    def parse(self, response):

        logging.debug("**** response from = %s", response.url)

        seriedata = []
        for serie in self.series_data:
            print(serie["url"])
            if (serie["url"] == response.url):
                seriedata = serie
                break

        if not seriedata:
            return

        logging.debug("**** using serie = %s", seriedata["name"])

        nchapter = seriedata["chapter"]
        nchapter += 1

        schapter = ''
        if (nchapter < 10):
            schapter = '0'
        schapter += str(nchapter)

        logging.debug("**** searching for season = %s chapter = %d", seriedata["season"], nchapter)

        found = False
        for sel in response.xpath(seriedata["xpath"]):

            if ('xpath_title' in seriedata and len(seriedata["xpath_title"]) > 0):

                smask = seriedata["title_mask"]
                smask = smask.replace("#2", schapter)
                smask = smask.replace('#1', str(seriedata["season"]))

                title = sel.xpath(seriedata["xpath_title"]).extract()
                if (len(title) == 0 or title[0].find(smask) == -1):
                    continue

                logging.debug("**** title = %s", title[0])

            smask = seriedata["link_mask"]
            smask = smask.replace("#2", schapter)
            smask = smask.replace('#1', str(seriedata["season"]))

            link = sel.xpath(seriedata["xpath_link"]).extract()

            if (len(link) == 0 or (len(smask) > 0 and link[0].find(smask) == -1)):
                continue

            if ('link_prefix' in seriedata and len(seriedata["link_prefix"]) > 0):
                link[0] = seriedata["link_prefix"] + link[0]

            logging.debug("****** link = %s", link)

            scommand = 'python utwhisper/utwhisper.py --add-url '+link[0]
            os.system(scommand)
            found = True

        if (found):
            seriedata['chapter'] = nchapter
            with open(self.jsonfile, 'wt') as file:
                json.dump(self.series_data, file)
                file.close()

        if ('file_mask' in seriedata):
            file_mask = seriedata['file_mask']
            for nnchapter in range(1, nchapter):
                
                file_to_move = ""

                sschapter = ''
                if (nnchapter < 10):
                    sschapter = '0'
                sschapter += str(nnchapter)

                file_mask = dwnldir + seriedata['file_mask']
                file_mask = file_mask.replace("#2", sschapter)
                file_mask = file_mask.replace('#1', str(seriedata["season"]))

                logging.debug("Searching for %s", file_mask)

                if (os.path.isdir(file_mask)):
                    for filename in os.listdir(file_mask):
                        logging.debug("Found %s", filename)
                        if (".avi" in filename):
                            logging.debug("Found video %s", filename)
                            file_to_move = file_mask + "/" + filename
                            break
                elif (os.path.isfile(file_mask)):
                    file_to_move = file_mask

                if (len(file_to_move) > 0):
                    src = file_to_move
                    dst = seriesdir + seriedata['name'] + "/Season " + str(seriedata["season"]) + "/" + seriedata['name'] + "-" + str(seriedata["season"]) + sschapter + ".avi"
                    try:
                        os.rename(src, dst)
                        logging.debug("Moved %s to %s", src, dst)
                    except OSError:
                        logging.debug("Cannot move %s to %s. Errno = %d", src, dst, os.strerror(errno.errcode))

