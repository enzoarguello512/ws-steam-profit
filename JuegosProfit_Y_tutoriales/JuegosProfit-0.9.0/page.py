from locator import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import time

#For
DataValue = True

#Pandas
LAppID = []
LName = []
LGamePrice = []
LDiscount = []
LCheapestCardPrice = []#
LNumberOfCardsInTotal = []#
LObtainableCards = []#
LSteamCommission = []#
LValueOfTheCardsObtainableWithoutTheSteamCommission = []#
LApproximateMinimumProfit = []#
LPriceMultipliedByNumberOfAccounts = []#
LPaidOut = []#
LDateOfPurchase = []#
LOfferType = []
LNewHighestDiscount = []
LDaysSinceTheOfferStarted = []
LDaysForTheOfferToEnd = []




class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

class Backup(object):
    def CreateLogFolder(self):
        "Creamos las carpetas donde van a ir los logs , si es que no existen"
        try:
            os.makedirs ('logs/css (backup)')
            os.makedirs ('logs/excel')
            print ('Creating logs folder')
            print ("Directory's Created ")
        except FileExistsError:
            pass

    def DTFS(self):
        "Creamos el archivo log si es que no existe"
        try:
            print("reading log.xlsx")
            df = pd.read_excel('logs/excel/log.xlsx')
            del df
        except:
            print("file not found, creating it now")
            df = pd.DataFrame({
                "AppID" : [],
                "Name" : [],
                "Game price" : [],
                "Discount" : [],
                "Cheapest card price" : [],
                "Number of cards in total" : [],
                "Obtainable Cards" : [],
                "Steam commission" : [],
                "Value of the cards obtainable without the steam commission" : [],
                "Approximate minimum profit (counting commission and value of the game)" : [],
                "Price multiplied by number of accounts" : [],
                "Paid out" : [],
                "Date of purchase" : [],
                "Offer type" : [],
                "New highest discount?" : [],
                "Days since the offer started" : [],
                "Days for the offer to end" : []})
            df.to_excel('logs/excel/log.xlsx', index = False)

    def SaveData(self):
        "Guardamos la info en un archivo .excel , gracias al modulo pandas"
        try:
            df = pd.read_excel ('logs/excel/log.xlsx')
            df ["AppID"] = LAppID
            df ["Name"] = LName
            df ["Game price"] = LGamePrice
            df ["Discount"] = LDiscount
            df ["Offer type"] = LOfferType
            df ["New highest discount?"] = LNewHighestDiscount
            df ["Days since the offer started"] = LDaysSinceTheOfferStarted
            df ["Days for the offer to end"] = LDaysForTheOfferToEnd
        finally:
            #Problema es que sobreescribe el anterior
            df.to_excel ('logs/excel/log.xlsx', index = False)

class MainPage(BasePage):

    def Gwait (self):
        "Esperamos que cargue todos los juegos asi les podemos sacar la info"
        global gamesStats

        try:
            print("Intentando cargar la pagina , tiempo de expera maximo , 10 minutos")
            gamesStats = WebDriverWait(self.driver, 600).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[.]'))
            )
            print (len (gamesStats), " elementos encontrados")
        except:
            print("Error y/o tiempo de espera excedido")
            self.driver.close()

    def Gdata (self):
        amount = 1

        time.sleep(1)   #Sino nos come el primer item por el while que dejamos en la main.py , y nos come las fecha , por eso le puse un cooldown

        for data in gamesStats:

            #Autoscroll for loading contents
            self.driver.execute_script ('window.scrollTo(0, ' + str(amount*50) + ')')

            #AppID
            List_AppID = data.get_attribute ("data-appid")
            LAppID.append(List_AppID)

            #Name
            List_Name = data.find_element (By.CLASS_NAME, "b").text
            LName.append(List_Name)

            #GamePrice
            List_Game_Price = data.find_element (By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[' + str(amount) + ']/td[5]').text
            LGamePrice.append(List_Game_Price)

            #Discount
            List_Discount = data.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[' + str(amount) + ']/td[4]').text
            LDiscount.append(List_Discount)

            #New highest discount? and Offer type
            List_Offer_type = data.find_elements (By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[' + str(amount) + ']/td[3]/span/span')

            if len(List_Offer_type) == 0:
                LOfferType.append("X")
                LNewHighestDiscount.append("X")

            elif len (List_Offer_type) == 1:
                for i in List_Offer_type:
                    Sub_Atrb = i.get_attribute ("class")
                    if Sub_Atrb.startswith ("category sales"):
                        LOfferType.append (i.text)
                        LNewHighestDiscount.append ("X")
                    elif Sub_Atrb.startswith ("highest"):
                        LNewHighestDiscount.append (i.text)
                        LOfferType.append ("X")
                    else:
                        LOfferType.append (i.text)
                        LNewHighestDiscount.append ("X")

            else:
                for i in List_Offer_type:
                    Sub_Atrb = i.get_attribute ("class")
                    if Sub_Atrb.startswith ("category sales"):
                        LOfferType.append (i.text)
                    elif Sub_Atrb.startswith ("highest"):
                        LNewHighestDiscount.append (i.text)
                    else:
                        LOfferType.append (i.text)

            #DaysSinceTheOfferStarted
            List_Offer_Started = data.find_element (By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[' + str (amount) + ']/td[8]').text
            LDaysSinceTheOfferStarted.append (List_Offer_Started)

            #DaysForTheOfferToEnd
            List_Offer_To_End = data.find_element (By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[' + str (amount) + ']/td[7]').text
            LDaysForTheOfferToEnd.append (List_Offer_To_End)

            amount += 1
        print("###########################")
        print(len(LAppID)," ",LAppID)
        print(len(LName)," ",LName)
        print(len(LGamePrice)," ",LGamePrice)
        print(len(LNewHighestDiscount)," ",LNewHighestDiscount)
        print(len(LOfferType)," ",LOfferType)
        print (len (LDaysSinceTheOfferStarted), " ", LDaysSinceTheOfferStarted)
        print (len (LDaysForTheOfferToEnd), " ", LDaysForTheOfferToEnd)
        print ("###########################")

    def LoadContents(self):
        amount = 0
        cardCount = 0
        for i in LAppID:    #Lista de appid's
            self.driver.get('https://steamcommunity.com/market/search?appid=753&category_753_Game%5B%5D=tag_app_' + str(i) + '&q=Cromo#p1_price_asc')
            List_Items = self.driver.find_elements(By.XPATH, '//*[@id="resultlink_."]')     #Listado de todos los cromos comunes y reflactantes si tiene
            for i in List_Items:    #Por cromo dentro de la pagina
                CardLowPrice = i.find_element(By.XPATH, '//*[@id="result_0"]/div[1]/div[2]/span[1]/span[1]').text
                NormalCardsCount = i.find_element('//*[@id="result_'+ str(amount) + '"]/div[2]/span[2]').text
                if NormalCardsCount.startswith("Cromo de"):
                    cardCount += 1
        LCheapestCardPrice.append(CardLowPrice)
        LNumberOfCardsInTotal.append(cardCount)
        cardCount = 0


class Navigation(BasePage):

    def new_tab(self):
        self.driver.switch_to.new_window('tab')

    def ClickTagPrice(self):
        "FilterByLowPrice"
        time.sleep(0.5)
        WebDriverWait (self.driver, 600).until (EC.element_to_be_clickable ((By.XPATH, '//*[@id="DataTables_Table_0"]/thead/tr/th[5]'))).click()

    def ShowEntries(self):
        "250 default"
        time.sleep (0.5)
        WebDriverWait (self.driver, 600).until (EC.element_to_be_clickable ((By.XPATH, '//*[@id="DataTables_Table_0_length"]/label/select'))).click ()
        time.sleep (0.5)
        WebDriverWait (self.driver, 600).until (EC.element_to_be_clickable ((By.XPATH, '//*[@id="DataTables_Table_0_length"]/label/select/option[4]'))).click ()

    def ClickNext(self):
        self.driver.find_element(By.CSS_SELECTOR, "a[class='paginate_button next']").click()