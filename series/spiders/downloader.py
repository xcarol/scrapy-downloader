# -*- coding: utf-8 -*-
import scrapy
import os
import json
import logging

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

        FORMAT = '%(asctime)-15s %(message)s'
        logging.basicConfig(filename='series.log',level=logging.DEBUG,format=FORMAT)
        logging.debug("*****")
        logging.debug("*****")
        logging.debug("*****")

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

        nserie = self.start_urls.index(response.url)
        seriedata = self.series_data[nserie]

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

            if (len(seriedata["xpath_title"]) > 0):

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

            logging.debug("****** link = %s", link)

            scommand = 'python utwhisper/utwhisper.py --add-url '+link[0]
            os.system(scommand)
            found = True

        if (found):
            seriedata['chapter'] = nchapter
            with open(self.jsonfile, 'wt') as file:
                json.dump(self.series_data, file)
                file.close()

