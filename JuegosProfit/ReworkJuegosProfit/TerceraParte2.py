from scrapy.crawler import CrawlerProcess
from fake_useragent import UserAgent
from numpy import argmin
from Utiles import *
import scrapy
import math
import time


#-------------------------------------------------
sql = 'SELECT `Steamcardexchange link` FROM jp_sin_refinar'
c.execute(sql)
LFullAppidLinkPLUS = c.fetchall()
j = 0
for name in LFullAppidLinkPLUS:
    LFullAppidLinkPLUS[j] = name[0] # Siendo name una tupla creo
    j += 1

#-------------------------------------------------
sql = 'SELECT `Game price (ARS)` FROM jp_sin_refinar'
c.execute(sql)
LGamePricePLUS = c.fetchall()
j = 0
for name in LGamePricePLUS:
    LGamePricePLUS[j] = name[0]
    j += 1

#-------------------------------------------------
#Lista de nombres de juegos
sql = 'SELECT Name FROM jp_sin_refinar'
c.execute(sql)
LNamePLUS = c.fetchall()
j = 0
for name in LNamePLUS:
    LNamePLUS[j] = name[0]
    j += 1

#-------------------------------------------------
#Para saber si podemos adelantar la lista
sql = 'SELECT `Cheapest card price (USD)` FROM jp_sin_refinar'
c.execute(sql)
list_of_card_price = c.fetchall()
j = 0
for card in list_of_card_price:
    list_of_card_price[j] = card[0]
    j += 1


if len(list_of_card_price) == 0:
    superId = 0

#nos fijamos si podemos adelantar algun item ,en la base de datos los items none son los incompletos
else:
    o = 0
    for card in list_of_card_price:
        if card is None:
            superId = o  # es aproposito , tiene que ser una 'o' porque fijate que representa nuestro contador
            break
        elif card == list_of_card_price[-1]:    #Si es el ultimo elemento , directamente que no ejecute el programa
            superId = len(LFullAppidLinkPLUS[o:])  #Quedaria algo asi como 33/33, osea un solo item en la lista, esto por si ya esta llena la lista
        else:
            o += 1

LFullAppidLinkPLUS = LFullAppidLinkPLUS[superId:]
LGamePricePLUS = LGamePricePLUS[superId:]

print(f'Arrancando en {superId}')



ua = UserAgent()
amountPLUS = 0


class CardsSpider(scrapy.Spider):
    name = "cards"

    start_urls = LFullAppidLinkPLUS

    custom_settings = {
        'DOWNLOAD_DELAY': 1.0,  # Lo ideal para mi seria entre 2 o 3
        'CONCURRENT_REQUESTS': 1,
        'USER_AGENT': str(ua.random),
        # Para evitar un posible van de 'navegador' , pero no evitariamos uno de ip , para eso esta TOR browser
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

        name_str = LNamePLUS[superId + amountPLUS]

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
            LCheapestCardPrice = 0
            LPreciosArs = 0
            LNumberOfCardsInTotal = 0
            LObtainableCards = 0
            LSteamCommission = 0
            LValueOfTheCardsObtainableWithoutTheSteamCommission = 0
            LApproximateMinimumProfit = 0
            LPriceMultipliedByNumberOfAccounts = 0
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
            LCheapestCardPrice = truncate(Refined_Prices_of_cards[MinIndex], 2)  # Price in Usd manager        #Tabien
            LPreciosArs = truncate(Refined_Prices_of_cards[MinIndex] * 55, 2)  # Price in Ars manager   #Tabien
            # #40 de juegos muy probable profit , 55 te añade alguno capas que de resultado negativos , a mayor el numero
            LNumberOfCardsInTotal = int(NumberOfCards)
            LObtainableCards = math.ceil(int(NumberOfCards) / 2)  # Half + 1 cards obtanaible
            LSteamCommission = truncate((LPreciosArs * LObtainableCards) * 15 / 100, 2)  # Tabien
            LValueOfTheCardsObtainableWithoutTheSteamCommission = truncate(LPreciosArs * LObtainableCards,
                                                                           2)  # 8.25  #Tabien
            LApproximateMinimumProfit = truncate(
                LValueOfTheCardsObtainableWithoutTheSteamCommission-LSteamCommission-LGamePricePLUS[amountPLUS], 2)
            LPriceMultipliedByNumberOfAccounts = truncate(LApproximateMinimumProfit * 15, 2)
            # LPaidOut.append(truncate(LGamePricePLUS[amountPLUS], 2))

            amountPLUS += 1

        if amountPLUS == 0:
            pass
        elif amountPLUS % 100 == 0:
            print('Guardando.')
            db.commit()


        sql = 'update jp_sin_refinar set `Cheapest card price (USD)` = %s,' \
              ' `Cheapest card price (ARS)` = %s,' \
              ' `Number of cards in total` = %s,' \
              ' `Obtainable cards` = %s,' \
              ' `Steam commission (ARS)` = %s,' \
              ' `Value of the cards obtainable without the steam commission (ARS)` = %s,' \
              ' `Approximate minimum profit (ARS)` = %s,' \
              ' `Price multiplied by number of accounts (ARS)` = %s where Name = %s '
        values = (LCheapestCardPrice, LPreciosArs, LNumberOfCardsInTotal, LObtainableCards, LSteamCommission,
                  LValueOfTheCardsObtainableWithoutTheSteamCommission, LApproximateMinimumProfit,
                  LPriceMultipliedByNumberOfAccounts, name_str)

        c.execute(sql, values)

        sql = 'update jp_refinados set `Cheapest card price (USD)` = %s,' \
              ' `Cheapest card price (ARS)` = %s,' \
              ' `Number of cards in total` = %s,' \
              ' `Obtainable cards` = %s,' \
              ' `Steam commission (ARS)` = %s,' \
              ' `Value of the cards obtainable without the steam commission (ARS)` = %s,' \
              ' `Approximate minimum profit (ARS)` = %s,' \
              ' `Price multiplied by number of accounts (ARS)` = %s where Name = %s '
        values = (LCheapestCardPrice, LPreciosArs, LNumberOfCardsInTotal, LObtainableCards, LSteamCommission,
                  LValueOfTheCardsObtainableWithoutTheSteamCommission, LApproximateMinimumProfit,
                  LPriceMultipliedByNumberOfAccounts, name_str)

        c.execute(sql, values)

pregunta = int(input('Queres guardar (presiona 2) o queres arrancar el spider (presiona 1)?: '))
if pregunta == 1:
    process = CrawlerProcess()
    process.crawl(CardsSpider)
    process.start()
    db.commit()
    Backup().Del_Prev_Files()  # Borramos los excels viejos
    Backup().create_dataframe_and_save()
    Backup().convert_data_sql()
elif pregunta == 2:
    Backup().Del_Prev_Files()   #Borramos los excels viejos
    Backup().create_dataframe_and_save()
    Backup().convert_data_sql()

