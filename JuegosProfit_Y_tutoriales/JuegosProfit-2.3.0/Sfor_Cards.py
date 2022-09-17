from numpy import argmin
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd
import time

df = pd.read_excel('./logs/excel/log.xlsx')
LFullAppidLinkPLUS = df["Full appid link"]

class CardsSpider(scrapy.Spider):

    name = "cards"
    start_urls = list(LFullAppidLinkPLUS)

    # def start_requests(self):
    #     urls = list(LFullAppidLinkPLUS)
    #     for url in urls:
    #         yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):

        List_Prices_WOtext = []
        print('Llegue')

        page = response.url.split("-")[-1]

        NumberOfCards = response.xpath(
            '//*[@id="content-area"]/div[2]/div[2]/div[3]/table/tr/th[1]/text()').get()

        current_container = 2
        current_card = 1
        try:
            for i in range(int(NumberOfCards)):
                card_price = response.xpath(
                    '//*[@id="content-area"]/div[2]/div[4]/div[' + str(current_container) + ']/div[' + str(
                        current_card) + ']/div/a/text()').get()
                if current_card % 6 == 0:  # Onda si es multiplo de 6
                    current_container += 1
                    current_card = 1
                else:
                    current_card += 1
                List_Prices_WOtext.append(float(card_price.replace("Price: $", "")))
        except TypeError:
            pass

        MinIndex = argmin(List_Prices_WOtext)

        print('##############')
        print(NumberOfCards)
        print(List_Prices_WOtext)
        print(MinIndex)
        print('##############')

        filename = 'card-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

process = CrawlerProcess()
process.crawl(CardsSpider)
process.start()





