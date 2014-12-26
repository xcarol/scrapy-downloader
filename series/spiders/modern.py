# -*- coding: utf-8 -*-
import scrapy
import os
import json

# https://github.com/tranqil/utwhisper

class ModernSpider(scrapy.Spider):
    name = "modern"
    filename = "modern.json"
    allowed_domains = ["oldpiratebay.org"]
    start_urls = (
        'https://oldpiratebay.org/search.php?q=modern+family+temporada+6+[HDTV]+[Espa%C3%B1ol+Castellano]',
    )

    def parse(self, response):

        with open(self.filename, 'rwt') as file:
            marker = json.load(file)
            file.close()

        nchapter = marker['chapter']
        nchapter += 1

        schapter = ''
        if (nchapter < 10):
            schapter = '0'
        schapter += str(nchapter)

        smask = marker['mask']
        smask = smask.replace("#2", schapter)
        smask = smask.replace('#1', marker['season'])

        found = False
        for sel in response.xpath('//table/tbody/tr/td'):
            title = sel.xpath('a/span/text()').extract()

            if (len(title) == 0 or title[0].find(smask) == -1):
                continue

            link = sel.xpath('div/a/@href').extract()
            scommand = 'python utwhisper/utwhisper.py --add-url '+link[0]

            os.system(scommand)
            found = True

        if (found):
            marker['chapter'] = nchapter
            with open(self.filename, 'wt') as file:
                json.dump(marker, file)
                file.close()


