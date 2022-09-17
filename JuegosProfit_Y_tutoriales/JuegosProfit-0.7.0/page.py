from locator import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

class Backup(object):
    def CreateLogFolder(self):
        try:
            os.makedirs ('logs/css (backup)')
            os.makedirs ('logs/excel')
            print ('Creating logs folder')
            print ("Directory's Created ")
        except FileExistsError:
            pass

    def DTFS(self):
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
        try:
            df = pd.read_excel ('logs/excel/log.xlsx')
            df ["AppID"] = LAppID
            df ["Name"] = LName
            df ["Game price"] = LGamePrice
            df ["Offer type"] = LOfferType
            df ["New highest discount?"] = LNewHighestDiscount
            df ["Days since the offer started"] = LDaysSinceTheOfferStarted
            df ["Days for the offer to end"] = LDaysForTheOfferToEnd
        finally:
            #Problema es que sobreescribe el anterior
            df.to_excel ('logs/excel/log.xlsx', index = False)

class MainPage(BasePage):

    def Gwait (self):

        global gamesStats

        try:
            print("Tratando de cargar la pagina (tiempo maximo de espera , 10 minutos).")
            gamesStats = WebDriverWait(self.driver, 600).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[.]'))
            )
            print (len (gamesStats), " elementos encontrados")
        except:
            print("Error y/o tiempo de espera excedido")

    def Gdata (self):
        amount = 1

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

class Navigation(BasePage):

    def new_tab(self):
        original_window = self.driver.current_window_handle


