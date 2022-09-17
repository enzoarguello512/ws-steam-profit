from selenium import webdriver
from locator import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
import pandas as pd
from numpy import argmin
import os
import time

#driver = webdriver.Chrome("chromedriver.exe")
#driver.get("https://www.google.com/")

LAppID = ['423230', '433340', '310560', '421020', '440900', '644560', '435150', '548430', '418240', '1250', '639790', '35720', '844930', '35700', '813630', '1018850', '351920', '1038740', '248610', '743390', '712840', '686200', '35450', '395170', '41000', '263980', '1104660', '630060', '491040', '668630', '644570', '476240', '711990', '373420', '625980', '613100', '598700', '415420', '576770', '220740', '1070580', '328080', '1293230', '248330', '546080', '465200', '41070', '1067540', '232090', '214340']
LCheapestCardPrice = []
LNumberOfCardsInTotal = []
LPreciosArs = []
# ua = UserAgent()
# print(ua.random, "Soy useragent")
# opts = Options ()
# opts.add_argument ('user-agent=' + str(ua.random))
# driver2 = webdriver.Chrome ("chromedriver.exe", chrome_options = opts)
#driver = webdriver.Chrome ("chromedriver.exe")
# agent = driver2.execute_script("return navigator.userAgent")
# print(agent,"Soy Agente actual")
class pato(object):
    def __init__(self):
        ua = UserAgent ()
        opts = Options ()
        opts.add_argument ('user-agent=' + str (ua.random))
        self.driver = webdriver.Chrome("chromedriver.exe", chrome_options = opts)

    def Multiplo(self,a,b):
        return True if a % b == 0 else False

    def IngresaCuenta(self,usuario,contrasena):
        self.usuario = usuario
        self.contrasena = contrasena
        self.driver.get("https://store.steampowered.com/")
        time.sleep(10)
        LoginButton = self.driver.find_element(By.XPATH, '//*[@id="global_action_menu"]/a').click()
        LOGName = self.driver.find_element(By.XPATH, '//*[@id="input_username"]').send_keys(self.usuario)
        time.sleep(3)
        LOGPass = self.driver.find_element(By.XPATH, '//*[@id="input_password"]').send_keys(self.contrasena)
        time.sleep (3)
        SendEnter = s91elf.driver.find_element(By.XPATH, '//*[@id="login_btn_signin"]/button').click()
        time.sleep(35)
        self.driver.close()

    def BuscaPreciosSteam(self):
        pass

    def LoadContents(self):

        for i in LAppID:  # Lista de appid's

            if (len(LNumberOfCardsInTotal) % 25) == 0:  #Porque steam te limita sino , cada 25 items hay que tirar un stop de 5 o 4 minutos
                time.sleep(240)

            ContainerCount = 1
            amount = 1
            match_class = []
            SubElemofCard = []
            CardsInXContainer = []
            List_Prices_Wtext = []
            List_Cards_Elem_Index = []

            self.driver.get ('https://www.steamcardexchange.net/index.php?gamepage-appid-' + str(i))    #steamexchanxe + appid por cada vuelta del bucle
            try:
                print ("Intentando cargar la pagina , tiempo de expera maximo , 10 minutos")
                List_principal_container = WebDriverWait (self.driver, 600).until (
                    EC.presence_of_all_elements_located ((By.XPATH, '//*[@id="content-area"]/div[2]/div[4]/div[.]'))
                )
                print (len (List_principal_container), " elementos encontrados")
            except:
                print ("Error y/o tiempo de espera excedido")
                self.driver.close ()

            NumberOfCards = self.driver.find_element(By.XPATH, '//*[@id="content-area"]/div[2]/div[2]/div[3]/table/tbody/tr/th[1]').text
            LNumberOfCardsInTotal.append(NumberOfCards)     #Busca el numero total de cartas
            

            for elem in List_principal_container:   #Del principal container saca unicamente los que posiblemente tengan cartas
                Container = elem.get_attribute ("class")
                if Container.startswith ("showcase-element-container"):
                    print("Soy clase buena")
                    match_class.append(elem)    #Agrega los contenedores de cromos nada mas

            for container in match_class:
                ContainerCount += 1
                print("container ",ContainerCount)
                CardsInXContainer = WebDriverWait(container, 600).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="content-area"]/div[2]/div[4]/div[' + str(ContainerCount) + ']/div[.]')))
                print("Baje")

            for card in CardsInXContainer:    #6 cartas poneles
                SubElemofCard.append(card)  #Anadimos las cartas a una lista para hacerlas iterables
                print("aca estoy")
                containsprice = []
                for i in SubElemofCard: #por cada carta , agremas sus contenidos
                    containsprice.append(i)
                print(len(containsprice))
                if len(containsprice) >= 2:
                    cardPrice = WebDriverWait(elem, 600).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="content-area"]/div[2]/div[4]/div[' + str(ContainerCount) + ']/div[' + str(amount) + ']/div/a')))
                    List_Prices_Wtext.append(float(cardPrice.text.replace("Price: $","")))  #Agrega todos de todos los cromos de la pagina precios sin las letras
                    List_Cards_Elem_Index.append (cardPrice)     #Los elementos de los precios
                    amount += 1
                    print("aca sali")
                else:
                    continue
                amount = 1
            print(List_Prices_Wtext)
            print(List_Cards_Elem_Index)
            MinIndex = argmin (List_Prices_Wtext)
            WEElment = List_Cards_Elem_Index [MinIndex].get_attribute("href")
            self.driver.get (WEElment)
            print ("Hice click")
            ArsPrice = WebDriverWait (self.driver, 600).until (
                EC.presence_of_element_located ((By.XPATH, '//*[@id="market_commodity_forsale"]/span[2]'))).text
            LPreciosArs.append (ArsPrice)
            print(LPreciosArs)
            print(LNumberOfCardsInTotal)







if __name__ == '__main__':
    #pato ().IngresaCuenta ('', '')
    pato().LoadContents()























#-----------------------------------------------------------------------------------------------
# from selenium import webdriver
# from locator import *
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from fake_useragent import UserAgent
# from selenium.webdriver.chrome.options import Options
# import pandas as pd
# import os
# import time
#
# #driver = webdriver.Chrome("chromedriver.exe")
# #driver.get("https://www.google.com/")
#
# LAppID = ['423230', '433340', '310560', '421020', '440900', '644560', '435150', '548430', '418240', '1250', '639790', '35720', '844930', '35700', '813630', '1018850', '351920', '1038740', '248610', '743390', '712840', '686200', '35450', '395170', '41000', '263980', '1104660', '630060', '491040', '668630', '644570', '476240', '711990', '373420', '625980', '613100', '598700', '415420', '576770', '220740', '1070580', '328080', '1293230', '248330', '546080', '465200', '41070', '1067540', '232090', '214340']
# LCheapestCardPrice = []
# LNumberOfCardsInTotal = []
#
# # ua = UserAgent()
# # print(ua.random, "Soy useragent")
# # opts = Options ()
# # opts.add_argument ('user-agent=' + str(ua.random))
# # driver2 = webdriver.Chrome ("chromedriver.exe", chrome_options = opts)
# driver = webdriver.Chrome ("chromedriver.exe")
# # agent = driver2.execute_script("return navigator.userAgent")
# # print(agent,"Soy Agente actual")
#
# def Multiplo(a, b):
#     return True if a % b == 0 else False
#
#
# def LoadContents():
#     amount = 0
#     cardCount = 0
#     for i in LAppID:  # Lista de appid's
#         print(LCheapestCardPrice)
#         print(LNumberOfCardsInTotal)
#         #if (amount2%2) == 0:
#
#         driver2.get ('https://steamcommunity.com/market/search?appid=753&category_753_Game%5B%5D=tag_app_' + str (i) + '&q=Cromo#p1_price_asc')
#         time.sleep(5)
#         List_Items = driver2.find_elements (By.CLASS_NAME, 'market_listing_row_link')  # Listado de todos los cromos comunes y reflactantes si tiene
#         for i in List_Items:  # Por cromo dentro de la pagina
#             CardLowPrice = i.find_element (By.XPATH, '//*[@id="result_0"]/div[1]/div[2]/span[1]/span[1]').text  #Primere cromo de la lista osea el mas barato
#             NormalCardsCount = i.find_elements(By.CLASS_NAME, 'market_listing_game_name')  #todas las cartas las metemos en una lista
#             for i in NormalCardsCount:
#                 Card = i.text
#                 if Card.startswith ("Cromo de"):
#                     cardCount += 1
#         LCheapestCardPrice.append (CardLowPrice)
#         LNumberOfCardsInTotal.append (cardCount)
#         cardCount = 0
#         amount += 1
#         # if Multiplo(amount , 10):
#         #     print ("Llegue")
#         #     time.sleep(240)
#
#
# # time.sleep(6)
#
# # new_tab ()
# LoadContents ()

#################################################################################################################################
# for elem in List_Items:  # Por elemento dentro de nuestro contenedor
#     print ("Buscando div's que contengan nuestros cromos")
#     OnlyClassElements = WebDriverWait (driver, 600).until (EC.presence_of_all_elements_located ((By.XPATH,
#                                                                                                  '//*[@id="content-area"]/div[2]/div[4]/div[.]')))  # Ahora tendriamos en una lista los elementos que son clases nada mas
#     for klassWithElem in OnlyClassElements:  # ITERamos sobre las clases que tenemos que por lo general son 2
#         print ("Encontramos un/una clase contenedora de cromos , iterando en busca de cartas")
#         CardsContainer = klassWithElem.get_attribute ("class")  # Buscamos a ver que nos dice la etiqueta clase
#         if CardsContainer.startswith ("showcase-element-container"):  # Y buscamos la que nos interesa
#             GoodContainer.append (klassWithElem)
#             for card in GoodContainer:
#                 print (
#                     "Adquiriendo los precios de todas las cartas 'normales' que aparecen en la pagina y buscando las menores")
#                 cardPrice = card.
#                 amount += 1
#                 IntListOnly = [int (i) for i in cardPrice.split () if i.isdigit ()]
#                 List_Card_Prices.append (IntListOnly)
#                 List_Cards_Elem_Index.append (card)
#             amount = 0
# # Aca sacariamos cuantas cartas hay maximas
# MinIndex = np.argmin (List_Card_Prices)
# WEElment = List_Cards_Elem_Index [MinIndex]
# WEElment.click ()
# print ("Hice click")
# print ("Aca iria la parte de steam")

