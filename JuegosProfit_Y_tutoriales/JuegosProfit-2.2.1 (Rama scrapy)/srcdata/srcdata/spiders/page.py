from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
import time

#import xlrd as necesario para pandas / excel


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
LSteamStoreLink = []
LFullAppidLink = []

#Function for decimals
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier



class BasePage(object):     #Para importar el driver desde main
    def __init__(self, driver):
        self.driver = driver

class Backup(object):
    "Funciones para guardar nuestros datos / y crear los que hagan falta"
    def CreateLogFolder(self):
        "Creamos las carpetas donde van a ir los logs , si es que no existen , cuidado que se borra el contenido previo de estas"
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
                "Game price (ARS)" : [],
                "Discount" : [],
                "Cheapest card price (USD)" : [],
                "Cheapest card price (ARS)" : [],
                "Number of cards in total" : [],
                "Obtainable cards" : [],
                "Steam commission (ARS)" : [],
                "Value of the cards obtainable without the steam commission (ARS)" : [],
                "Approximate minimum profit (counting commission and value of the game) (ARS)" : [],
                "Price multiplied by number of accounts (ARS)" : [],
                "Paid out (ARS)" : [],
                "Date of purchase" : [],
                "Offer type" : [],
                "New highest discount?" : [],
                "Days since the offer started" : [],
                "Days for the offer to end" : [],
                "Full appid link" : [],
                "Steam store link" : [],
            })
            df.to_excel('logs/excel/log.xlsx', index = False)

    def Pre_SaveData(self):
        "Guardamos la info en un archivo .excel , gracias al modulo pandas , o al menos la primera parte de steamdb"
        try:
            df = pd.read_excel ('logs/excel/log.xlsx')
            df ["AppID"] = LAppID
            df ["Name"] = LName
            df ["Game price (ARS)"] = LGamePrice
            df ["Discount"] = LDiscount
            # df ["Offer type"] = LOfferType
            # df ["New highest discount?"] = LNewHighestDiscount
            # df ["Days since the offer started"] = LDaysSinceTheOfferStarted
            # df ["Days for the offer to end"] = LDaysForTheOfferToEnd
            df ["Full appid link"] = LFullAppidLink
            df ["Steam store link"] = LSteamStoreLink
        finally:
            #Problema es que sobreescribe el anterior
            df.to_excel ('logs/excel/log.xlsx', index = False)

    def Post_SaveData (self):
        "Guardamos la info que sale de LoadContents() por separado , por si queremos hacer 2 pasadas separadas"
        try:
            df = pd.read_excel ('logs/excel/log.xlsx')
            df ["Cheapest card price (USD)"] = LCheapestCardPrice
            df ["Cheapest card price (ARS)"] = LPreciosArs
            df ["Number of cards in total"] = LNumberOfCardsInTotal
            df ["Obtainable cards"] = LObtainableCards
            df ["Steam commission (ARS)"] = LSteamCommission
            df ["Value of the cards obtainable without the steam commission (ARS)"] = LValueOfTheCardsObtainableWithoutTheSteamCommission
            df ["Approximate minimum profit (counting commission and value of the game) (ARS)"] = LApproximateMinimumProfit
            df ["Price multiplied by number of accounts (ARS)"] = LPriceMultipliedByNumberOfAccounts
            df ["Paid out (ARS)"] = LPaidOut
        finally:
            # Problema es que sobreescribe el anterior
            df.to_excel ('logs/excel/log.xlsx', index = False)

    def Full_Savedata(self):
        "Guardamos toda la info de golpe , si es que hacemos una sola pasada con el bot , pero estan los otros metodos recortados por si este no te gusta , ya que la info se va guardando en la memoria durante la ejecucion del programa"
        try:
            df = pd.read_excel ('logs/excel/log.xlsx')
            df ["AppID"] = LAppID
            df ["Name"] = LName
            df ["Game price (ARS)"] = LGamePrice
            df ["Discount"] = LDiscount
            df ["Cheapest card price (USD)"] = LCheapestCardPrice
            df ["Cheapest card price (ARS)"] = LPreciosArs
            df ["Number of cards in total"] = LNumberOfCardsInTotal
            df ["Obtainable cards"] = LObtainableCards
            df ["Steam commission (ARS)"] = LSteamCommission
            df ["Value of the cards obtainable without the steam commission (ARS)"] = LValueOfTheCardsObtainableWithoutTheSteamCommission
            df ["Approximate minimum profit (counting commission and value of the game) (ARS)"] = LApproximateMinimumProfit
            df ["Price multiplied by number of accounts (ARS)"] = LPriceMultipliedByNumberOfAccounts
            df ["Paid out (ARS)"] = LPaidOut
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

        try:
            print("Intentando cargar la pagina , tiempo de expera maximo , 10 minutos")
            gamesStats = WebDriverWait(self.driver, 600).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="search_resultsRows"]/a[.]'))
            )
            print (len (gamesStats), " elementos encontrados")
        except:
            print("Error y/o tiempo de espera excedido")
            self.driver.close()

    def Gdata (self):

        amount = 1

        time.sleep(1)   #Sino nos come el primer item por el while que dejamos en la main.py , y nos come las fecha , por eso le puse un cooldown

        while True:

            try:
                # de ahi scamos los juegos
                # de steam exchange los precios
                # de https://steamdb.info/sales/
                # sacamos los fechas y lowest recorded

                #Autoscroll for loading contents
                #Porque steamdb necesita hacer scroll para que carguen ciertos datos
                self.driver.execute_script ('window.scrollTo(0, ' + str(amount*50) + ')')

                #Pick 1 item from the list for further examination
                data = self.driver.find_element(By.XPATH, '//*[@id="search_resultsRows"]/a[' + str(amount) + ']')

                #AppID
                List_AppID = data.get_attribute ("data-ds-appid")
                LAppID.append(List_AppID)

                #Name
                List_Name = data.find_element (By.CSS_SELECTOR, 'span[class="title"]').get_attribute("innerHTML")
                LName.append(List_Name)

                #GamePrice
                List_Game_Price = data.find_element (By.CSS_SELECTOR, 'div[class="col search_price discounted responsive_secondrow"]').get_attribute("innerHTML").replace ("ARS$ ", "")
                LGamePrice.append((List_Game_Price.split("<br>")[1]).replace(" ", ""))

                #Discount
                List_Discount = data.find_element(By.CSS_SELECTOR, 'div[class="col search_discount responsive_secondrow"]').get_attribute("innerHTML")
                LDiscount.append((List_Discount.split(">")[1]).split('<')[0])

                # #New highest discount? and Offer type
                # List_Offer_type = data.find_elements (By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[' + str(amount) + ']/td[3]/span/span')

                # if len(List_Offer_type) == 0:   #If there are no tags to find
                #     LOfferType.append("X")
                #     LNewHighestDiscount.append("No")
                #
                # elif len (List_Offer_type) == 1:    #If are only 1 type of tag , the other will be filled automatily , this is for the module pandas
                #     for i in List_Offer_type:
                #         Sub_Atrb = i.get_attribute ("class")
                #         if Sub_Atrb.startswith ("category sales"):
                #             LOfferType.append (i.text)
                #             LNewHighestDiscount.append ("No")
                #         elif Sub_Atrb.startswith ("highest"):
                #             LNewHighestDiscount.append (i.text)
                #             LOfferType.append ("X")
                #         else:
                #             LOfferType.append (i.text)
                #             LNewHighestDiscount.append ("No")
                #
                # else:   #If the element have more than 1 tag , it will append the tag to it respestive column , for pandas
                #     for i in List_Offer_type:
                #         Sub_Atrb = i.get_attribute ("class")
                #         if Sub_Atrb.startswith ("category sales"):
                #             LOfferType.append (i.text)
                #         elif Sub_Atrb.startswith ("highest"):
                #             LNewHighestDiscount.append (i.text)
                #         else:
                #             LOfferType.append (i.text)

                # #DaysSinceTheOfferStarted
                # List_Offer_Started = data.find_element (By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[' + str (amount) + ']/td[8]').text
                # LDaysSinceTheOfferStarted.append (List_Offer_Started)
                #
                # #DaysForTheOfferToEnd
                # List_Offer_To_End = data.find_element (By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[' + str (amount) + ']/td[7]').text
                # LDaysForTheOfferToEnd.append (List_Offer_To_End)

                #FullAppidLink
                LFullAppidLink.append('https://www.steamcardexchange.net/index.php?gamepage-appid-' + str(List_AppID))

                #SteamStoreLink
                LSteamStoreLink.append('https://store.steampowered.com/app/' + str(List_AppID))

                amount += 1

            except NoSuchElementException:
                break

            # finally:
            #     pass

            print("###########################")
            print(len(LAppID)," ",LAppID)
            print(len(LName)," ",LName)
            print(len(LGamePrice)," ",LGamePrice)
            print(len(LDiscount), " ", LDiscount)
            print(len(LNewHighestDiscount)," ",LNewHighestDiscount)
            print(len(LOfferType)," ",LOfferType)
            print (len (LDaysSinceTheOfferStarted), " ", LDaysSinceTheOfferStarted)
            print (len (LDaysForTheOfferToEnd), " ", LDaysForTheOfferToEnd)
            print(len(LFullAppidLink), " ", LFullAppidLink)
            print(len(LSteamStoreLink), " ", LSteamStoreLink)
            print ("###########################")





class SecondMainPage(MainPage):
    pass



