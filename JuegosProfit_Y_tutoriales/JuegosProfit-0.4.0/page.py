from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os
# import time
# import re


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


class MainPage(BasePage, Backup):

    lista = []

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

    def new_tab (self):
        original_window = self.driver.current_window_handle


    def Gdata (self):
        LAppID = []
        LName = []
        LOfferType = []
        LNewHighestDiscount = []
        items = []  #No necesario
        amount = 1
        df = pd.read_excel('logs/excel/log.xlsx')
        #print(df.columns)
        for data in gamesStats:
            #AppID
            List_AppID = data.get_attribute ("data-appid")
            LAppID.append(List_AppID)

            #Name
            List_Name = data.find_element (By.CLASS_NAME, "b").text
            LName.append(List_Name)


            #New highest discount? and Offer type
            List_Offer_type = data.find_elements (By.XPATH, ('//*[@id="DataTables_Table_0"]/tbody/tr[' + str(amount) + ']/td[3]/span/span'))
            if len(List_Offer_type) == 0:
                LOfferType.append("X")
                LNewHighestDiscount.append("X")

            for i in List_Offer_type:
                Sub_Atrb = i.get_attribute ("class")
                if Sub_Atrb.startswith ("category sales"):
                    LOfferType.append(i.text)
                elif Sub_Atrb.startswith("highest"):
                    LNewHighestDiscount.append(i.text)
                else:
                    LOfferType.append(i.text)
            amount += 1
        # df["AppID"] = LAppID
        # df["Name"] = LName
        # df["Offer type"] = LOfferType
        # df["New highest discount?"] = LNewHighestDiscount
        print("###########################3")
        print(len(LAppID))
        print(len(LName))
        print (len(LNewHighestDiscount))
        print (len(LOfferType))
        print ("###########################3")
        print("###########################3")
        print(LAppID)
        print(LName)
        print (LNewHighestDiscount)
        print (LOfferType)
        print ("###########################3")
        # items = LAppID + LName + LNewHighestDiscount + LOfferType
        # print(items)
        # print(len(items))
        print(df)
