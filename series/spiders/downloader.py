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

        print("*** url *** = ", self.series_data["url"])
        self.start_urls = [self.series_data["url"]]

    def parse(self, response):

        print("**** response **** = ", response)

        nchapter = self.series_data["chapter"]
        nchapter += 1

        schapter = ''
        if (nchapter < 10):
            schapter = '0'
        schapter += str(nchapter)

        found = False
        for sel in response.xpath(self.series_data["xpath"]):

            if (len(self.series_data["xpath_title"]) > 0):

                smask = self.series_data["title_mask"]
                smask = smask.replace("#2", schapter)
                smask = smask.replace('#1', self.series_data["season"])

                title = sel.xpath(self.series_data["xpath_title"]).extract()
                if (len(title) == 0 or title[0].find(smask) == -1):
                    continue

            smask = self.series_data["link_mask"]
            smask = smask.replace("#2", schapter)
            smask = smask.replace('#1', self.series_data["season"])

            link = sel.xpath(self.series_data["xpath_link"]).extract()
            if (len(link) == 0 or (len(smask) > 0 and link[0].find(smask) == -1)):
                continue

            scommand = 'python utwhisper/utwhisper.py --add-url '+link[0]
            os.system(scommand)
            found = True

        if (found):
            self.series_data['chapter'] = nchapter
            with open(self.jsonfile, 'wt') as file:
                json.dump(self.series_data, file)
                file.close()


