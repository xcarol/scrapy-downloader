# -*- coding: utf-8 -*-
import scrapy
import os
import json

# https://github.com/tranqil/utwhisper

class CastleSpider(scrapy.Spider):
    name = "castle"
    filename = "castle.json"
    allowed_domains = ["oldpiratebay.org"]
    start_urls = (
#        'https://oldpiratebay.org/search.php?q=castle+temporada+7+[HDTV]+[Espa%C3%B1ol+Castellano]',
        'http://kickass.so/usearch/castle%20temporada%207%20%5BHDTV%5D%20%5BEspa%C3%B1ol%20Castellano%5D/',
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
        for sel in response.xpath('//a[@class="imagnet icon16"]'):

            link = sel.xpath('@href').extract()
            print (" Link: "+link[0])

            if (len(link) == 0 or link[0].find(smask) == -1):
                continue

            scommand = 'python utwhisper/utwhisper.py --add-url '+link[0]
            os.system(scommand)
            found = True

        if (found):
            marker['chapter'] = nchapter
            with open(self.filename, 'wt') as file:
                json.dump(marker, file)
                file.close()


