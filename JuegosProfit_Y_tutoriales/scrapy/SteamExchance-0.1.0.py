import scrapy
from scrapy.crawler import CrawlerProcess
from numpy import argmin
import pandas as pd


df = pd.read_excel ('log.xlsx')
LFullAppidLinkPLUS = df ["Full appid link"]
print(type(LFullAppidLinkPLUS))
lapp_index = 1
class CardsSpider(scrapy.Spider):
    name = "cards"

    start_urls = list(LFullAppidLinkPLUS)

    def parse(self, response):
        global lapp_index
        List_Prices_WOtext = []

        page = response.url.split("-")[-1]

        NumberOfCards = response.xpath('//*[@id="content-area"]/div[2]/div[2]/div[3]/table/tr/th[1]/text()').get()

        current_container = 2
        current_card = 1
        try:
            for i in range(int(NumberOfCards)):
                card_price = response.xpath('//*[@id="content-area"]/div[2]/div[4]/div[' + str(current_container) + ']/div[' + str(current_card) + ']/div/a/text()').get()
                if current_card % 6 == 0:   #Onda si es multiplo de 6
                    current_container += 1
                    current_card = 1
                else:
                    current_card += 1
                List_Prices_WOtext.append (float (card_price.replace ("Price: $", "")))
        except TypeError:
            pass

        MinIndex = argmin(List_Prices_WOtext)


        print('##############')
        print(NumberOfCards)
        print(List_Prices_WOtext)
        print(MinIndex)
        print('##############')
        # if lapp_index <= len(LAppIDPLUS):
        #     next_appid = 'https://www.steamcardexchange.net/index.php?gamepage-appid-' + str(LAppIDPLUS[lapp_index])
        #     lapp_index += 1
        #     yield scrapy.Request(next_appid, callback = self.parse)


        # filename = 'card-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)



process = CrawlerProcess()
process.crawl(CardsSpider)
process.start()
