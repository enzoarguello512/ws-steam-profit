from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time
from numpy import argmin
import math


#Pandas
LAppID = []
LName = []
LGamePrice = []
LDiscount = []
LCheapestCardPrice = []
LPreciosArs = []
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

#Function for decimals
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier



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
                "PreciosArs" : [],
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

    def Pre_SaveData(self):
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

    def Post_SaveData (self):
        "Guardamos la info en un archivo .excel , gracias al modulo pandas"
        try:
            df = pd.read_excel ('logs/excel/log.xlsx')
            df ["Cheapest card price"] = LCheapestCardPrice
            df ["PreciosArs"] = LPreciosArs
            df ["Number of cards in total"] = LNumberOfCardsInTotal
            df ["Obtainable Cards"] = LObtainableCards
            df ["Steam commission"] = LSteamCommission
            df ["Value of the cards obtainable without the steam commission"] = LValueOfTheCardsObtainableWithoutTheSteamCommission
            df ["Approximate minimum profit (counting commission and value of the game)"] = LApproximateMinimumProfit
            df ["Price multiplied by number of accounts"] = LPriceMultipliedByNumberOfAccounts
            df ["Paid out"] = LPaidOut
        finally:
            # Problema es que sobreescribe el anterior
            df.to_excel ('logs/excel/log.xlsx', index = False)

    def Full_Savedata(self):
        "Guardamos la info en un archivo .excel , gracias al modulo pandas"
        try:
            df = pd.read_excel ('logs/excel/log.xlsx')
            df ["AppID"] = LAppID
            df ["Name"] = LName
            df ["Game price"] = LGamePrice
            df ["Discount"] = LDiscount
            df ["Cheapest card price"] = LCheapestCardPrice
            df ["PreciosArs"] = LPreciosArs
            df ["Number of cards in total"] = LNumberOfCardsInTotal
            df ["Obtainable Cards"] = LObtainableCards
            df ["Steam commission"] = LSteamCommission
            df ["Value of the cards obtainable without the steam commission"] = LValueOfTheCardsObtainableWithoutTheSteamCommission
            df ["Approximate minimum profit (counting commission and value of the game)"] = LApproximateMinimumProfit
            df ["Price multiplied by number of accounts"] = LPriceMultipliedByNumberOfAccounts
            df ["Paid out"] = LPaidOut
            # df ["Date of purchase"] = LDateOfPurchase
            df ["Offer type"] = LOfferType
            df ["New highest discount?"] = LNewHighestDiscount
            df ["Days since the offer started"] = LDaysSinceTheOfferStarted
            df ["Days for the offer to end"] = LDaysForTheOfferToEnd
        finally:
            # Problema es que sobreescribe el anterior
            df.to_excel ('logs/excel/log.xlsx', index = False)


    def converter(self):
        pass

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

            if len(List_Offer_type) == 0:   #If there are no tags to find
                LOfferType.append("X")
                LNewHighestDiscount.append("X")

            elif len (List_Offer_type) == 1:    #If are only 1 type of tag , the other will be filled automatily , this is for the module pandas
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

            else:   #If the element have more than 1 tag , it will append the tag to it respestive column , for pandas
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

class SecondMainPage(MainPage):

    def LoadContents(self):
        df = pd.read_excel ('logs/excel/log.xlsx')
        LAppIDPLUS = df ["AppID"]
        LGamePricePLUS = df ["Game price"]
        Refined_Prices = []
        Amt = 1
        for price in LGamePricePLUS:
            Amt += 1
            word = []
            for i in price:
                if i == "," or i == ".":
                    word.append (".")
                elif i.isdigit ():
                    word.append (i)
                else:
                    continue
            Refined_Prices.append ("".join (word))
        amountPLUS = 0

        for item in LAppIDPLUS:  # Lista de appid's

            ContainerCount = 1
            amount = 1
            match_class = []
            List_Prices_WOtext = []
            List_Cards_Elem_Index = []

            self.driver.get ('https://www.steamcardexchange.net/index.php?gamepage-appid-' + str (item))  # steamexchanxe + appid por cada vuelta del bucle
            print ("##################################################################################################################")

            try:
                print ("Intentando cargar la pagina , tiempo de expera maximo , 10 minutos")
                List_principal_container = WebDriverWait (self.driver, 600).until (
                    EC.presence_of_all_elements_located ((By.XPATH, '//*[@id="content-area"]/div[2]/div[4]/div[.]'))
                )
                print (len (List_principal_container), " elementos encontrados")
            except:
                print ("Error y/o tiempo de espera excedido")
                self.driver.close ()

            NumberOfCards = self.driver.find_element (By.XPATH,'//*[@id="content-area"]/div[2]/div[2]/div[3]/table/tbody/tr/th[1]').text
            LNumberOfCardsInTotal.append (NumberOfCards)  # Busca el numero total de cartas

            for elem in List_principal_container:   #Del principal container saca unicamente los que posiblemente tengan cartas
                Container = elem.get_attribute ("class")
                if Container.startswith ("showcase-element-container"):
                    match_class.append(elem)    #Agrega los contenedores de cromos nada mas

            print ("De los", len (List_principal_container), "cotainers que detecto el elemento padre , solamante ",len (match_class), " cumplen los requisitos")

            for container in match_class:
                ContainerCount += 1
                print ("container ", ContainerCount)
                CardsInXContainer = WebDriverWait (container, 600).until (
                    EC.presence_of_all_elements_located ((By.XPATH, '//*[@id="content-area"]/div[2]/div[4]/div[' + str (ContainerCount) + ']/div[.]')))
                print (len (CardsInXContainer), "Hay esta cantidad de cartas en este determinado container")
                for card in CardsInXContainer:  # 6 cartas poneles
                    try:
                        cardPrice = WebDriverWait (card, 1.5).until (
                            EC.presence_of_element_located ((By.XPATH, '//*[@id="content-area"]/div[2]/div[4]/div[' + str (ContainerCount) + ']/div[' + str (amount) + ']/div/a')))
                        List_Prices_WOtext.append (float (cardPrice.text.replace ("Price: $", "")))  # Agrega todos de todos los cromos de la pagina precios sin las letras
                        List_Cards_Elem_Index.append (cardPrice)  # Los elementos de los precios
                        amount += 1
                        print ("Carta agregada")
                    except:
                        print ("Carta skipeada")
                amount = 1
            print (List_Prices_WOtext)
            print (List_Cards_Elem_Index)
            MinIndex = argmin (List_Prices_WOtext)
            print("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            LCheapestCardPrice.append(truncate(List_Prices_WOtext[MinIndex], 2)) #Price in Usd manager        #Tabien
            print("$ en USD",LCheapestCardPrice)
            LPreciosArs.append(truncate(List_Prices_WOtext[MinIndex]*55, 2))   #Price in Ars manager   #Tabien   #40 de juegos muy probable profit , 55 te añade alguno capas que de resultado negativos , a mayor el numero
            print("$ en ARS",LPreciosArs)
            LObtainableCards.append(math.ceil(int(NumberOfCards)/2)) #Half + 1 cards obtanaible      #Tabien########################
            print("Cartas Obtenibles", LObtainableCards)
            LSteamCommission.append(truncate((LPreciosArs[amountPLUS]*LObtainableCards[amountPLUS])*15/100, 2))#Tabien
            print("Comicion de steam", LSteamCommission)
            LValueOfTheCardsObtainableWithoutTheSteamCommission.append(truncate(LPreciosArs[amountPLUS]*LObtainableCards[amountPLUS], 2))#8.25  #Tabien
            print("Valor de las cartas sin la comicion", LValueOfTheCardsObtainableWithoutTheSteamCommission)
            LApproximateMinimumProfit.append(truncate(LValueOfTheCardsObtainableWithoutTheSteamCommission[amountPLUS]-LSteamCommission[amountPLUS]-float(Refined_Prices[amountPLUS]), 2))
            print("Profit Aproximado", LApproximateMinimumProfit)
            LPriceMultipliedByNumberOfAccounts.append(truncate(LApproximateMinimumProfit[amountPLUS]*11, 2))
            print("Precio Multi x Cuentas", LPriceMultipliedByNumberOfAccounts)
            LPaidOut.append(truncate(float(Refined_Prices[amountPLUS]), 2))
            print("Pagado", LPaidOut)
            print ("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
            print (LPreciosArs)
            print (LNumberOfCardsInTotal)
            amountPLUS += 1
            print ("##################################################################################################################")