# -*- coding: utf-8 -*-
import scrapy
import os
import json

# https://github.com/tranqil/utwhisper

class DownloaderSpider(scrapy.Spider):
    name = "downloader"
    jsonfile = ""
    series_data = ""

    def __init__(self, series=None, *args, **kwargs):
        super(DownloaderSpider, self).__init__(*args, **kwargs)

        self.jsonfile = series
        with open(self.jsonfile, 'rwt') as file:
            self.series_data = json.load(file)
            file.close()

        for serie in self.series_data:
            self.start_urls.append(serie["url"])
            print "*** added url = ", serie["url"]

    def parse(self, response):

        nserie = self.start_urls.index(response.url)
        seriedata = self.series_data[nserie]

        print "**** response from = ", response.url
        print "**** using serie = ", seriedata["name"]
        print "**** searching for season = ", seriedata["season"], " chapter = ", seriedata["chapter"] + 1

        nchapter = seriedata["chapter"]
        nchapter += 1

        schapter = ''
        if (nchapter < 10):
            schapter = '0'
        schapter += str(nchapter)

        found = False
        for sel in response.xpath(seriedata["xpath"]):

            if (len(seriedata["xpath_title"]) > 0):

                smask = seriedata["title_mask"]
                smask = smask.replace("#2", schapter)
                smask = smask.replace('#1', str(seriedata["season"]))

                title = sel.xpath(seriedata["xpath_title"]).extract()
                if (len(title) == 0 or title[0].find(smask) == -1):
                    continue

            smask = seriedata["link_mask"]
            smask = smask.replace("#2", schapter)
            smask = smask.replace('#1', str(seriedata["season"]))

            link = sel.xpath(seriedata["xpath_link"]).extract()
            if (len(link) == 0 or (len(smask) > 0 and link[0].find(smask) == -1)):
                continue

            scommand = 'python utwhisper/utwhisper.py --add-url '+link[0]
            os.system(scommand)
            found = True

        if (found):
            seriedata['chapter'] = nchapter
            with open(self.jsonfile, 'wt') as file:
                json.dump(self.series_data, file)
                file.close()

