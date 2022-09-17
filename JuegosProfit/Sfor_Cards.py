from scrapy.crawler import CrawlerProcess
from fake_useragent import UserAgent
from numpy import argmin
from page import *
import scrapy
import math
import time



df = pd.read_excel('./logs/excel/log.xlsx')

LFullAppidLinkPLUS = list(df["Steamcardexchange link"].dropna())
LGamePricePLUS = list(df["Game price (ARS)"].dropna())

list_of_card_price = list(df["Cheapest card price (USD)"].dropna())

if len(list_of_card_price) == 0:
    confirmation = False
elif len(list_of_card_price) > 0:
    confirmation = True
    LFullAppidLinkPLUS = LFullAppidLinkPLUS[len(list_of_card_price):]
    LGamePricePLUS = LGamePricePLUS[len(list_of_card_price):]

del df

ua = UserAgent ()
amountPLUS = 0

class CardsSpider(scrapy.Spider):

    name = "cards"

    start_urls = LFullAppidLinkPLUS

    custom_settings = {
        'DOWNLOAD_DELAY': 1.2,  #Lo ideal para mi seria entre 2 o 3 , hay veces que capas tira error el programa , porque se seba con las peticiones por minuto , no es error del el programa en si , es culpa de la pagina que nos limita
        'CONCURRENT_REQUESTS': 1,
        'USER_AGENT': str(ua.random),   #Para evitar un posible van de 'navegador' , pero no evitariamos uno de ip , para eso esta TOR browser
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 5,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
        'AUTOTHROTTLE_DEBUG': True,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': False,
    }

    # def start_requests(self):
    #     urls = list(LFullAppidLinkPLUS)
    #     for url in urls:
    #         yield scrapy.Request(url = url, callback = self.parse)

    def parse(self, response):
        global amountPLUS

        if confirmation:

            # print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            # print(len(LCheapestCardPrice), "$ en USD", LCheapestCardPrice)
            # print(len(LPreciosArs), "$ en ARS", LPreciosArs)
            # print(len(LNumberOfCardsInTotal), "Number of cards in total", LNumberOfCardsInTotal)
            # print(len(LObtainableCards), "Cartas Obtenibles", LObtainableCards)
            # print(len(LSteamCommission), "Comicion de steam", LSteamCommission)
            # print(len(LValueOfTheCardsObtainableWithoutTheSteamCommission), "Valor de las cartas sin la comicion", LValueOfTheCardsObtainableWithoutTheSteamCommission)
            # print(len(LApproximateMinimumProfit), "Profit Aproximado", LApproximateMinimumProfit)
            # print(len(LPriceMultipliedByNumberOfAccounts), "Precio Multi x Cuentas", LPriceMultipliedByNumberOfAccounts)
            # #print("Pagado", LPaidOut)
            # print ("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            # print("##################################################################################################################")
            # print("Progreso: ", amountPLUS, "/", len(LFullAppidLinkPLUS))
            # print("##################################################################################################################")
            t = time.localtime()
            print(str(time.strftime("%Y-%m-%d %H:%M:%S", t)) + '|JuegosProfit-2.5.0|INFO|TP|', amountPLUS, '/', len(LFullAppidLinkPLUS))

            List_Prices_Wtext = []

            NumberOfCards = response.xpath(
                '//*[@id="content-area"]/div[2]/div[2]/div[3]/table/tr/th[1]/text()').get()

            current_container = 2
            current_card = 1

            if NumberOfCards == None:
                LCheapestCardPrice.append('-')
                LPreciosArs.append('-')
                LNumberOfCardsInTotal.append('-')
                LObtainableCards.append('-')
                LSteamCommission.append('-')
                LValueOfTheCardsObtainableWithoutTheSteamCommission.append('-')
                LApproximateMinimumProfit.append('-')
                LPriceMultipliedByNumberOfAccounts.append('-')

                if amountPLUS == 0:
                    pass

                elif amountPLUS % 100 == 0:
                    Backup().Post_SaveData()

                amountPLUS += 1

            else:
                for i in range(int(NumberOfCards)):
                    card_price = response.xpath(
                        '//*[@id="content-area"]/div[2]/div[4]/div[' + str(current_container) + ']/div[' + str(
                            current_card) + ']/div/a/text()').get()
                    if current_card % 6 == 0:  # Onda si es multiplo de 6
                        current_container += 1
                        current_card = 1
                    else:
                        current_card += 1
                    List_Prices_Wtext.append(card_price)

                Refined_Prices_of_cards = []
                convert_price(List_Prices_Wtext, Refined_Prices_of_cards)

                MinIndex = argmin(Refined_Prices_of_cards)

                # Y bueno aca son formulas para calcular aproximadamente los valores
                LCheapestCardPrice.append(truncate(Refined_Prices_of_cards[MinIndex], 2))  # Price in Usd manager        #Tabien
                LPreciosArs.append(truncate(Refined_Prices_of_cards[MinIndex] * 55, 2))  # Price in Ars manager   #Tabien   #40 de juegos muy probable profit , 55 te añade alguno capas que de resultado negativos , a mayor el numero
                LNumberOfCardsInTotal.append(int(NumberOfCards))
                LObtainableCards.append(math.ceil(int(NumberOfCards) / 2))  # Half + 1 cards obtanaible      #Tabien########################
                LSteamCommission.append(truncate((LPreciosArs[amountPLUS] * LObtainableCards[amountPLUS]) * 15 / 100, 2))  # Tabien
                LValueOfTheCardsObtainableWithoutTheSteamCommission.append(truncate(LPreciosArs[amountPLUS] * LObtainableCards[amountPLUS], 2))  # 8.25  #Tabien
                LApproximateMinimumProfit.append(truncate(LValueOfTheCardsObtainableWithoutTheSteamCommission[amountPLUS] - LSteamCommission[amountPLUS] - LGamePricePLUS[amountPLUS], 2))
                LPriceMultipliedByNumberOfAccounts.append(truncate(LApproximateMinimumProfit[amountPLUS] * 11, 2))
                # LPaidOut.append(truncate(LGamePricePLUS[amountPLUS], 2))

                if amountPLUS == 0:
                    pass

                elif amountPLUS % 100 == 0:
                    Backup().Post_SaveData()

                amountPLUS += 1

        elif not confirmation:


            # print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            # print(len(LCheapestCardPrice), "$ en USD", LCheapestCardPrice)
            # print(len(LPreciosArs), "$ en ARS", LPreciosArs)
            # print(len(LNumberOfCardsInTotal), "Number of cards in total", LNumberOfCardsInTotal)
            # print(len(LObtainableCards), "Cartas Obtenibles", LObtainableCards)
            # print(len(LSteamCommission), "Comicion de steam", LSteamCommission)
            # print(len(LValueOfTheCardsObtainableWithoutTheSteamCommission), "Valor de las cartas sin la comicion", LValueOfTheCardsObtainableWithoutTheSteamCommission)
            # print(len(LApproximateMinimumProfit), "Profit Aproximado", LApproximateMinimumProfit)
            # print(len(LPriceMultipliedByNumberOfAccounts), "Precio Multi x Cuentas", LPriceMultipliedByNumberOfAccounts)
            # #print("Pagado", LPaidOut)
            # print ("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            # print("##################################################################################################################")
            # print("Progreso: ", amountPLUS, "/", len(LFullAppidLinkPLUS))
            # print("##################################################################################################################")
            t = time.localtime()
            print(str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'|JuegosProfit-2.5.0|INFO|TP|', amountPLUS, '/',
                  len(LFullAppidLinkPLUS))

            List_Prices_Wtext = []

            NumberOfCards = response.xpath(
                '//*[@id="content-area"]/div[2]/div[2]/div[3]/table/tr/th[1]/text()').get()

            current_container = 2
            current_card = 1

            if NumberOfCards == None:
                LCheapestCardPrice.append('-')
                LPreciosArs.append('-')
                LNumberOfCardsInTotal.append('-')
                LObtainableCards.append('-')
                LSteamCommission.append('-')
                LValueOfTheCardsObtainableWithoutTheSteamCommission.append('-')
                LApproximateMinimumProfit.append('-')
                LPriceMultipliedByNumberOfAccounts.append('-')

                if amountPLUS == 0:
                    pass

                elif amountPLUS % 100 == 0:
                    Backup().Post_SaveData()

                amountPLUS += 1

            else:
                for i in range(int(NumberOfCards)):
                    card_price = response.xpath(
                        '//*[@id="content-area"]/div[2]/div[4]/div['+str(current_container)+']/div['+str(
                            current_card)+']/div/a/text()').get()
                    if current_card % 6 == 0:  # Onda si es multiplo de 6
                        current_container += 1
                        current_card = 1
                    else:
                        current_card += 1
                    List_Prices_Wtext.append(card_price)

                Refined_Prices_of_cards = []
                convert_price(List_Prices_Wtext, Refined_Prices_of_cards)

                MinIndex = argmin(Refined_Prices_of_cards)

                # Y bueno aca son formulas para calcular aproximadamente los valores
                LCheapestCardPrice.append(
                    truncate(Refined_Prices_of_cards[MinIndex], 2))  # Price in Usd manager        #Tabien
                LPreciosArs.append(truncate(Refined_Prices_of_cards[MinIndex] * 55,
                                            2))  # Price in Ars manager   #Tabien   #40 de juegos muy probable profit , 55 te añade alguno capas que de resultado negativos , a mayor el numero

                LNumberOfCardsInTotal.append(int(NumberOfCards))
                LObtainableCards.append(
                    math.ceil(int(NumberOfCards) / 2))  # Half + 1 cards obtanaible      #Tabien########################
                LSteamCommission.append(
                    truncate((LPreciosArs[amountPLUS] * LObtainableCards[amountPLUS]) * 15 / 100, 2))  # Tabien
                LValueOfTheCardsObtainableWithoutTheSteamCommission.append(
                    truncate(LPreciosArs[amountPLUS] * LObtainableCards[amountPLUS], 2))  # 8.25  #Tabien
                LApproximateMinimumProfit.append(truncate(
                    LValueOfTheCardsObtainableWithoutTheSteamCommission[amountPLUS]-LSteamCommission[amountPLUS]-
                    LGamePricePLUS[amountPLUS], 2))
                LPriceMultipliedByNumberOfAccounts.append(truncate(LApproximateMinimumProfit[amountPLUS] * 11, 2))
                # LPaidOut.append(truncate(LGamePricePLUS[amountPLUS], 2))

                if amountPLUS == 0:
                    pass

                elif amountPLUS % 100 == 0:
                    Backup().Post_SaveData()

                amountPLUS += 1




process = CrawlerProcess()
process.crawl(CardsSpider)
process.start()
Backup().Post_SaveData()

t = time.localtime()

os.rename('logs/excel/log.xlsx',
          (('logs/excel/log-'+str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'.xlsx').replace(":", ".")).replace(
              " ", "_"))

os.rename('logs/css-(backup)/log.csv', (
    ('logs/css-(backup)/log-'+str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'.csv').replace(":", ".")).replace(" ",
                                                                                                            "_"))




