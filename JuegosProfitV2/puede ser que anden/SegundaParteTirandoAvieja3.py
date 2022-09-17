from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from fake_useragent import UserAgent
from selenium import webdriver
import pandas as pd
from Utiles import *
import page
import os
import sys
import time


def resource_path (relative_path):
    "si no vas a hacer la vercion '.exe' borra esta funcion , porque sino genera error creo, o al menos si no importas"
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath (".")

    return os.path.join (base_path, relative_path)

driver = webdriver.Chrome(resource_path("chromedriver.exe"))
driver.get('https://steamdb.info/sales/')
driver.maximize_window()

class SecondMainPage(object):

    def __init__(self, driver):
        self.driver = driver

    def GdataExtra(self):
        df = pd.read_excel('logs/excel/log.xlsx')

        test_skip_items2 = list(df["Days since the offer started"].dropna())
        len_of_skip_items = len(test_skip_items2)

        if len_of_skip_items == 0:
            print('Lista de ofertas vacia , arrancando desde 0')

            LAppIDPLUS = list(df["AppID"].dropna())
            LNamePLUS = list(df["Name"].dropna())

            del df

        elif len_of_skip_items > 0:

            print('Lista de ofertas detectada, skipeando items hasta llegar al ultimo valor de esta, para poder completarla')

            LAppIDPLUS = list(df["AppID"].dropna())
            LAppIDPLUS = LAppIDPLUS[len_of_skip_items:]

            LNamePLUS = list(df["Name"].dropna())
            LNamePLUS = LNamePLUS[len_of_skip_items:]

            del df

        try:
            t = time.localtime()
            print(str(time.strftime("%Y-%m-%d %H:%M:%S",
                                    t))+'|JuegosProfit-2.5.0|INFO|SP|Intentando cargar la pagina , tiempo de expera maximo , 10 minutos')
            search_bar = WebDriverWait(self.driver, 600).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'input[type=search][aria-controls="DataTables_Table_0"]'))
            )
        except:
            t = time.localtime()
            print(str(time.strftime("%Y-%m-%d %H:%M:%S",
                                    t))+'|JuegosProfit-2.5.0|INFO|SP|Error y/o tiempo de espera excedido')
            self.driver.close()
        amount = 0

        t = time.localtime()
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'|JuegosProfit-2.5.0|INFO|SP|Cargando juegos en steamdb...')

        for name in LNamePLUS:

            try:
                name = Remove_unsoported_characters(name)
                search_bar.send_keys(name)
                new_results = WebDriverWait(self.driver, 600).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[.]')))

                amountPLUS = 1
                for item in new_results:

                    #Ya se que es medio al pedo la funcion esta , porque si no aparece el nombre en el buscador de steamdb igual agrega invalid data()
                    if LAppIDPLUS[amount] == 'Bundle/NoID':
                        invalid_data()
                        continue

                    try:

                        if float(item.get_attribute("data-appid")) == float(str(LAppIDPLUS[amount]).replace(',', '.')):

                            sub_info = item.find_elements(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr['+str(
                                amountPLUS)+']/td[3]/span/span')

                            List_Discount = item.find_element(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr['+str(
                                amountPLUS)+']/td[4]')

                            color = List_Discount.value_of_css_property("background-color")
                            # rgba(21, 102, 183, 1)  esoo es azul
                            # rgba(139, 195, 74, 1)  esoo es verde
                            # rgba(0, 0, 0, 0) es negro/gris

                            if len(sub_info) == 0:  # If there are no tags to find
                                LOfferType.append("X")
                                css_color(color)


                            elif len(
                                    sub_info) == 1:  # If are only 1 type of tag , the other will be filled automatily , this is for the module pandas
                                for i in sub_info:
                                    Sub_Atrb = i.get_attribute("class")
                                    if Sub_Atrb.startswith("category sales"):
                                        LOfferType.append(i.text)
                                        css_color(color)
                                    elif Sub_Atrb.startswith("highest"):
                                        LNewHighestDiscount.append(i.text)
                                        LOfferType.append("X")
                                    else:
                                        LOfferType.append(i.text)
                                        css_color(color)

                            else:  # If the element have more than 1 tag , it will append the tag to it respestive column , for pandas
                                for i in sub_info:
                                    Sub_Atrb = i.get_attribute("class")
                                    if Sub_Atrb.startswith("category sales"):
                                        LOfferType.append(i.text)
                                    elif Sub_Atrb.startswith("highest"):
                                        LNewHighestDiscount.append(i.text)
                                    else:
                                        LOfferType.append(i.text)

                            List_Offer_Started = item.find_element(By.XPATH,
                                                                   '//*[@id="DataTables_Table_0"]/tbody/tr['+str(
                                                                       amountPLUS)+']/td[8]').text
                            LDaysSinceTheOfferStarted.append(List_Offer_Started)

                            List_Offer_To_End = item.find_element(By.XPATH,
                                                                  '//*[@id="DataTables_Table_0"]/tbody/tr['+str(
                                                                      amountPLUS)+']/td[7]').text
                            LDaysForTheOfferToEnd.append(List_Offer_To_End)
                            break

                    except:
                        pass

                    if amountPLUS == len(new_results):  # Max loops
                        invalid_data()
                        search_bar.clear()

                    else:
                        amountPLUS += 1

                search_bar.clear()

                amount += 1

            except TypeError:
                invalid_data()
                search_bar.clear()
                amount += 1

            # print('######################')
            # print(name)
            # print(len(LNewHighestDiscount), LNewHighestDiscount)
            # print(len(LOfferType), LOfferType)
            # print(len(LDaysSinceTheOfferStarted), LDaysSinceTheOfferStarted)
            # print(len(LDaysForTheOfferToEnd), LDaysForTheOfferToEnd)
            t = time.localtime()
            print(str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'|JuegosProfit-2.5.0|DEBUG|SP', amount, '/',
                  len(LNamePLUS))

            if amount == 0:
                pass
            elif amount % 100 == 0:
                print('Guardando.')
                Backup().Page2_SaveData()

SecondMainPage(driver).GdataExtra()
Backup().Page2_SaveData()
driver.close()
