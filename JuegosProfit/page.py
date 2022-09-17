from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

# Todo lo recomendable para optimizacion seria que cada nose ponele 100 resultados , pongas los datos en el excel y despues
# hagas un del LISTAESPECIFICA o un remove o algo para liberar memoria y despues podes ir haciendo .appends gracias a pandas

# Todo , Hacer que copie el excel bueno y use ese , asi no tenes que modificarlo vos manualmente despues

# import xlrd as necesario para pandas / excel       #Para leerlos
# import openpyxl para guardar los excel


# Pandas
LAppID = []
LName = []
LGamePrice = []
LDiscount = []
LCheapestCardPrice = []
LPreciosArs = []
LNumberOfCardsInTotal = []  #
LObtainableCards = []  #
LSteamCommission = []  #
LValueOfTheCardsObtainableWithoutTheSteamCommission = []  #
LApproximateMinimumProfit = []  #
LPriceMultipliedByNumberOfAccounts = []  #
LPaidOut = []  #
LDateOfPurchase = []  #
LOfferType = []
LNewHighestDiscount = []
LDaysSinceTheOfferStarted = []
LDaysForTheOfferToEnd = []
LSteamStoreLink = []
LSteamcardexchangeLink = []


# Function for decimals
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


# Funtion for convert prices
def convert_price(list_to_convert, list_for_results):
    Amt = 1
    for string in list_to_convert:
        # Agaraamos cada precio y lo convertimos a solamente numeros y comas , asi despues si queremos lo podemos pasar a entero o manipular mas facil
        Amt += 1
        word = []
        for letter in string:
            if letter == "," or letter == ".":
                word.append(".")
            elif letter.isdigit():
                word.append(letter)
            else:
                continue
        try:
            list_for_results.append(float("".join(word)))
        except ValueError:
            list_for_results.append(float(999))


def css_color(item):
    if str(item) == 'rgba(21, 102, 183, 1)':  # onda si es azul
        LNewHighestDiscount.append("Product has not been this cheap before")
    elif str(item) == 'rgba(139, 195, 74, 1)':  # onda si es azul
        LNewHighestDiscount.append("Product is priced on par with lowest recorded price")
    else:
        LNewHighestDiscount.append("No")


def invalid_data():
    LNewHighestDiscount.append('-')
    LOfferType.append('-')
    LDaysSinceTheOfferStarted.append('-')
    LDaysForTheOfferToEnd.append('-')


def Remove_unsoported_characters(string):
    list_letters = []
    for letter in string:
        if letter.isalpha():
            list_letters.append(letter)
        elif letter == " ":
            list_letters.append(letter)
        else:
            pass
    new_string = "".join(list_letters)
    return new_string


def LimpiaConsola(): os.system('cls')


class BasePage(object):  # Para importar el driver desde main
    def __init__(self, driver):
        self.driver = driver


class Backup(object):
    "Funciones para guardar nuestros datos / y crear los que hagan falta"

    def CreateLogFolder(self):
        "Creamos las carpetas donde van a ir los logs , si es que no existen , cuidado que se borra el contenido previo de estas"
        try:
            os.makedirs('logs/css-(backup)')
            os.makedirs('logs/excel')
            print('Creating logs folder')
            print("Directory's Created ")
        except FileExistsError:
            pass

    def DTFS(self):
        "Creamos el archivo log si es que no existe"
        try:
            print("reading log.xlsx")
            df = pd.read_excel('logs/excel/log.xlsx')
            del df
        except:
            print("file not found('log.xlsx'), creating it now")
            df = pd.DataFrame({
                "AppID": [],
                "Name": [],
                "Game price (ARS)": [],
                "Discount": [],
                "Cheapest card price (USD)": [],
                "Cheapest card price (ARS)": [],
                "Number of cards in total": [],
                "Obtainable cards": [],
                "Steam commission (ARS)": [],
                "Value of the cards obtainable without the steam commission (ARS)": [],
                "Approximate minimum profit (counting commission and value of the game) (ARS)": [],
                "Price multiplied by number of accounts (ARS)": [],
                # "Paid out (ARS)" : [],
                "Date of purchase": [],
                "Offer type": [],
                "New highest discount?": [],
                "Days since the offer started": [],
                "Days for the offer to end": [],
                "Steamcardexchange link": [],
                "Steam store link": [],
            })
            df.to_excel('logs/excel/log.xlsx', index=False)
            del df

        ##---------------------------------------

        try:
            print("reading log.csv")
            df = pd.read_csv('logs/css-(backup)/log.csv')
            del df
        except:
            print("file not found('log.csv'), creating it now")
            df = pd.DataFrame({
                "AppID": [],
                "Name": [],
                "Game price (ARS)": [],
                "Discount": [],
                "Cheapest card price (USD)": [],
                "Cheapest card price (ARS)": [],
                "Number of cards in total": [],
                "Obtainable cards": [],
                "Steam commission (ARS)": [],
                "Value of the cards obtainable without the steam commission (ARS)": [],
                "Approximate minimum profit (counting commission and value of the game) (ARS)": [],
                "Price multiplied by number of accounts (ARS)": [],
                # "Paid out (ARS)" : [],
                "Date of purchase": [],
                "Offer type": [],
                "New highest discount?": [],
                "Days since the offer started": [],
                "Days for the offer to end": [],
                "Steamcardexchange link": [],
                "Steam store link": [],
                "SI": [],
            })
            df.to_csv('logs/css-(backup)/log.csv', index=False)
            del df



    def creating_table_PreSaveData(self, itemsToDuplicate):
        empty_list = [']'] * itemsToDuplicate

        try:
            df = pd.read_excel('logs/excel/log.xlsx')
            df["SI"] = pd.Series(empty_list)
        finally:
            # Problema es que sobreescribe el anterior
            df.to_excel('logs/excel/log.xlsx', index=False)

        try:
            df = pd.read_csv('logs/css-(backup)/log.csv')
            df["SI"] = pd.Series(empty_list)
        finally:
            # Problema es que sobreescribe el anterior
            df.to_csv('logs/css-(backup)/log.csv', index=False)
        del df

    def Page1_SaveData(self):
        "Guardamos la info en un archivo .excel , gracias al modulo pandas , o al menos la primera parte de steamdb"
        global LAppID
        global LName
        global LGamePrice
        global LDiscount
        global LSteamcardexchangeLink
        global LSteamStoreLink

        try:
            df = pd.read_excel('logs/excel/log.xlsx')

            LAppID = list(df["AppID"].dropna()) + LAppID
            LName = list(df["Name"].dropna()) + LName
            LGamePrice = list(df["Game price (ARS)"].dropna()) + LGamePrice
            LDiscount = list(df["Discount"].dropna()) + LDiscount
            LSteamcardexchangeLink = list(df["Steamcardexchange link"].dropna()) + LSteamcardexchangeLink
            LSteamStoreLink = list(df["Steam store link"].dropna()) + LSteamStoreLink

            df["AppID"] = pd.Series(LAppID)
            df["Name"] = pd.Series(LName)
            df["Game price (ARS)"] = pd.Series(LGamePrice)
            df["Discount"] = pd.Series(LDiscount)
            df["Steamcardexchange link"] = pd.Series(LSteamcardexchangeLink)
            df["Steam store link"] = pd.Series(LSteamStoreLink)
        finally:
            # Problema es que sobreescribe el anterior
            df.to_excel('logs/excel/log.xlsx', index=False)

        ##---------------------------------------
        try:
            df = pd.read_csv('logs/css-(backup)/log.csv')

            df["AppID"] = pd.Series(LAppID)
            df["Name"] = pd.Series(LName)
            df["Game price (ARS)"] = pd.Series(LGamePrice)
            df["Discount"] = pd.Series(LDiscount)
            df["Steamcardexchange link"] = pd.Series(LSteamcardexchangeLink)
            df["Steam store link"] = pd.Series(LSteamStoreLink)
        finally:
            # Problema es que sobreescribe el anterior
            df.to_csv('logs/css-(backup)/log.csv', index=False)

        LAppID.clear()
        LName.clear()
        LGamePrice.clear()
        LDiscount.clear()
        LSteamcardexchangeLink.clear()
        LSteamStoreLink.clear()

        del df

        # del LAppID
        # del LName
        # del LGamePrice
        # del LDiscount
        # del LSteamcardexchangeLink
        # del LSteamStoreLink
        ##---------------------------------------





    def Page2_SaveData(self):
        "Para guardar los precios de steamdb"
        global LOfferType
        global LNewHighestDiscount
        global LDaysSinceTheOfferStarted
        global LDaysForTheOfferToEnd

        try:
            df = pd.read_excel('logs/excel/log.xlsx')

            LOfferType = list(df["Offer type"].dropna()) + LOfferType
            LNewHighestDiscount = list(df["New highest discount?"].dropna()) + LNewHighestDiscount
            LDaysSinceTheOfferStarted = list(df["Days since the offer started"].dropna()) + LDaysSinceTheOfferStarted
            LDaysForTheOfferToEnd = list(df["Days for the offer to end"].dropna()) + LDaysForTheOfferToEnd

            df["Offer type"] = pd.Series(LOfferType)
            df["New highest discount?"] = pd.Series(LNewHighestDiscount)
            df["Days since the offer started"] = pd.Series(LDaysSinceTheOfferStarted)
            df["Days for the offer to end"] = pd.Series(LDaysForTheOfferToEnd)
        finally:
            df.to_excel('logs/excel/log.xlsx', index=False)

        ##---------------------------------------
        try:
            df = pd.read_csv('logs/css-(backup)/log.csv')

            df["Offer type"] = pd.Series(LOfferType)
            df["New highest discount?"] = pd.Series(LNewHighestDiscount)
            df["Days since the offer started"] = pd.Series(LDaysSinceTheOfferStarted)
            df["Days for the offer to end"] = pd.Series(LDaysForTheOfferToEnd)
        finally:
            df.to_csv('logs/css-(backup)/log.csv', index=False)

        LOfferType.clear()
        LNewHighestDiscount.clear()
        LDaysSinceTheOfferStarted.clear()
        LDaysForTheOfferToEnd.clear()

        del df

        # del LOfferType
        # del LNewHighestDiscount
        # del LDaysSinceTheOfferStarted
        # del LDaysForTheOfferToEnd
        ##---------------------------------------





    def Post_SaveData(self):
        "Guardamos la info que sale de LoadContents() por separado , por si queremos hacer 2 pasadas separadas"
        global LCheapestCardPrice
        global LPreciosArs
        global LNumberOfCardsInTotal
        global LObtainableCards
        global LSteamCommission
        global LValueOfTheCardsObtainableWithoutTheSteamCommission
        global LApproximateMinimumProfit
        global LPriceMultipliedByNumberOfAccounts

        try:
            df = pd.read_excel('logs/excel/log.xlsx')

            LCheapestCardPrice = list(df["Cheapest card price (USD)"].dropna()) + LCheapestCardPrice
            LPreciosArs = list(df["Cheapest card price (ARS)"].dropna()) + LPreciosArs
            LNumberOfCardsInTotal = list(df["Number of cards in total"].dropna()) + LNumberOfCardsInTotal
            LObtainableCards = list(df["Obtainable cards"].dropna()) + LObtainableCards
            LSteamCommission = list(df["Steam commission (ARS)"].dropna()) + LSteamCommission
            LValueOfTheCardsObtainableWithoutTheSteamCommission = list(df["Value of the cards obtainable without the steam commission (ARS)"].dropna()) + LValueOfTheCardsObtainableWithoutTheSteamCommission
            LApproximateMinimumProfit = list(df["Approximate minimum profit (counting commission and value of the game) (ARS)"].dropna()) + LApproximateMinimumProfit
            LPriceMultipliedByNumberOfAccounts = list(df["Price multiplied by number of accounts (ARS)"].dropna()) + LPriceMultipliedByNumberOfAccounts

            df["Cheapest card price (USD)"] = pd.Series(LCheapestCardPrice)
            df["Cheapest card price (ARS)"] = pd.Series(LPreciosArs)
            df["Number of cards in total"] = pd.Series(LNumberOfCardsInTotal)
            df["Obtainable cards"] = pd.Series(LObtainableCards)
            df["Steam commission (ARS)"] = pd.Series(LSteamCommission)
            df["Value of the cards obtainable without the steam commission (ARS)"] = pd.Series(LValueOfTheCardsObtainableWithoutTheSteamCommission)
            df["Approximate minimum profit (counting commission and value of the game) (ARS)"] = pd.Series(LApproximateMinimumProfit)
            df["Price multiplied by number of accounts (ARS)"] = pd.Series(LPriceMultipliedByNumberOfAccounts)
            # df ["Paid out (ARS)"] = LPaidOut
        finally:
            # Problema es que sobreescribe el anterior
            df.to_excel('logs/excel/log.xlsx', index=False)

        ##---------------------------------------
        try:
            df = pd.read_csv('logs/css-(backup)/log.csv')

            df["Cheapest card price (USD)"] = pd.Series(LCheapestCardPrice)
            df["Cheapest card price (ARS)"] = pd.Series(LPreciosArs)
            df["Number of cards in total"] = pd.Series(LNumberOfCardsInTotal)
            df["Obtainable cards"] = pd.Series(LObtainableCards)
            df["Steam commission (ARS)"] = pd.Series(LSteamCommission)
            df["Value of the cards obtainable without the steam commission (ARS)"] = pd.Series(LValueOfTheCardsObtainableWithoutTheSteamCommission)
            df["Approximate minimum profit (counting commission and value of the game) (ARS)"] = pd.Series(LApproximateMinimumProfit)
            df["Price multiplied by number of accounts (ARS)"] = pd.Series(LPriceMultipliedByNumberOfAccounts)
            # df ["Paid out (ARS)"] = LPaidOut
        finally:
            # Problema es que sobreescribe el anterior
            df.to_csv('logs/css-(backup)/log.csv', index=False)
        ##---------------------------------------


        LCheapestCardPrice.clear()
        LPreciosArs.clear()
        LNumberOfCardsInTotal.clear()
        LObtainableCards.clear()
        LSteamCommission.clear()
        LValueOfTheCardsObtainableWithoutTheSteamCommission.clear()
        LApproximateMinimumProfit.clear()
        LPriceMultipliedByNumberOfAccounts.clear()

        del df

        # del LCheapestCardPrice
        # del LPreciosArs
        # del LNumberOfCardsInTotal
        # del LObtainableCards
        # del LSteamCommission
        # del LValueOfTheCardsObtainableWithoutTheSteamCommission
        # del LApproximateMinimumProfit
        # del LPriceMultipliedByNumberOfAccounts


        # t = time.localtime()
        #
        # os.rename('logs/excel/log.xlsx',
        #           (('logs/excel/log-'+str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'.xlsx').replace(":", ".")).replace(
        #               " ", "_"))
        #
        # os.rename('logs/css-(backup)/log.csv', (
        #     ('logs/css-(backup)/log-'+str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'.csv').replace(":", ".")).replace(" ",
        #                                                                                                             "_"))

    def Full_Savedata(self):
        "Guardamos toda la info de golpe , si es que hacemos una sola pasada con el bot , pero estan los otros metodos recortados por si este no te gusta , ya que la info se va guardando en la memoria durante la ejecucion del programa"
        # SIN USO
        try:
            df = pd.read_excel('logs/excel/log.xlsx')
            df["AppID"] = LAppID
            df["Name"] = LName
            df["Game price (ARS)"] = LGamePrice
            df["Discount"] = LDiscount
            df["Cheapest card price (USD)"] = LCheapestCardPrice
            df["Cheapest card price (ARS)"] = LPreciosArs
            df["Number of cards in total"] = LNumberOfCardsInTotal
            df["Obtainable cards"] = LObtainableCards
            df["Steam commission (ARS)"] = LSteamCommission
            df[
                "Value of the cards obtainable without the steam commission (ARS)"] = LValueOfTheCardsObtainableWithoutTheSteamCommission
            df[
                "Approximate minimum profit (counting commission and value of the game) (ARS)"] = LApproximateMinimumProfit
            df["Price multiplied by number of accounts (ARS)"] = LPriceMultipliedByNumberOfAccounts
            df["Paid out (ARS)"] = LPaidOut
            # df ["Date of purchase"] = LDateOfPurchase
            df["Offer type"] = LOfferType
            df["New highest discount?"] = LNewHighestDiscount
            df["Days since the offer started"] = LDaysSinceTheOfferStarted
            df["Days for the offer to end"] = LDaysForTheOfferToEnd
        finally:
            # Problema es que sobreescribe el anterior
            df.to_excel('logs/excel/log.xlsx', index=False)

        del df

    def converter(self):
        pass


class MainPage(BasePage, Backup):

    def Gwait(self):
        "Esperamos que cargue todos los juegos asi les podemos sacar la info"

        try:
            t = time.localtime()
            print(str(time.strftime("%Y-%m-%d %H:%M:%S",
                                    t))+'|JuegosProfit-2.5.0|INFO|PP|Intentando cargar la pagina , tiempo de expera maximo , 10 minutos')
            gamesStats = WebDriverWait(self.driver, 150).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@id="search_resultsRows"]/a[.]')))
        except:
            t = time.localtime()
            print(str(time.strftime("%Y-%m-%d %H:%M:%S",
                                    t))+'|JuegosProfit-2.5.0|INFO|PP|Error y/o tiempo de espera excedido')
            self.driver.close()

    def Gdata(self):

        amount = 1

        max_items = WebDriverWait(self.driver, 150).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="search_results_filtered_warning_persistent"]/div'))).text.split(" ")[0]

        int_of_max_items = int(max_items.replace(",", ""))

        df = pd.read_excel('logs/excel/log.xlsx')

        test_skip_items = list(df["Name"].dropna())

        del df


        t = time.localtime()
        print(str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'|JuegosProfit-2.5.0|INFO|PP|', max_items,
              'juegos encontrados')

        if len(test_skip_items) == 0:
            print('Excel creado con exito, empezando la recoleccion de juegos')

            self.creating_table_PreSaveData(int_of_max_items)


            while amount <= int_of_max_items:

                # Autoscroll for loading contents
                # Porque steamdb necesita hacer scroll para que carguen ciertos datos
                self.driver.execute_script('window.scrollTo(0, '+str(amount * 150)+')')

                # Pick 1 item from the list for further examination
                data = WebDriverWait(self.driver, 150).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="search_resultsRows"]/a['+str(amount)+']')))

                # AppID
                try:
                    List_AppID = data.get_attribute("data-ds-appid")
                    LAppID.append(List_AppID)
                    # FullAppidLink
                    LSteamcardexchangeLink.append(
                        'https://www.steamcardexchange.net/index.php?gamepage-appid-'+str(List_AppID))

                    # SteamStoreLink
                    LSteamStoreLink.append('https://store.steampowered.com/app/'+str(List_AppID))
                except:
                    LAppID.append("999999")
                    # FullAppidLink
                    LSteamcardexchangeLink.append('https://www.steamcardexchange.net/index.php?gamepage-appid-999999')

                    # SteamStoreLink
                    LSteamStoreLink.append('https://store.steampowered.com/app/-999999')

                # Name
                try:
                    List_Name = data.find_element(By.CSS_SELECTOR, 'span[class="title"]').get_attribute("innerHTML")
                    LName.append(List_Name)
                except:
                    LName.append("Not found")

                # GamePrice
                try:
                    List_Game_Price = data.find_element(By.CSS_SELECTOR,
                                                        'div[class="col search_price discounted responsive_secondrow"]').get_attribute(
                        "innerHTML").replace("ARS$ ", "")
                    LGamePrice.append(float(((List_Game_Price.split("<br>")[1]).replace(" ", "")).replace(",", ".")))
                except:
                    LGamePrice.append(float(999))

                # Discount
                try:
                    List_Discount = data.find_element(By.CSS_SELECTOR,
                                                      'div[class="col search_discount responsive_secondrow"]').get_attribute(
                        "innerHTML")
                    LDiscount.append((List_Discount.split(">")[1]).split('<')[0])
                except:
                    LDiscount.append("Without discount")

                if amount == 0:
                    pass

                elif amount % 100 == 0:
                    self.Page1_SaveData()

                amount += 1

                # print("###########################")
                # print(len(LAppID)," ",LAppID)
                # print(len(LName)," ",LName)
                # print(len(LGamePrice)," ",LGamePrice)
                # print(len(LDiscount), " ", LDiscount)
                # print(len(LSteamcardexchangeLink), " ", LSteamcardexchangeLink)
                # print(len(LSteamStoreLink), " ", LSteamStoreLink)
                # print ("###########################")
                t = time.localtime()
                print(str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'|JuegosProfit-2.5.0|DEBUG|PP', amount, '/', max_items)
            Backup().Page1_SaveData()
            LimpiaConsola()

        elif len(test_skip_items) > 0:

            print('Detectado excel con juegos, avanzando en la busqueda para completarlo')

            last_name = test_skip_items[-1]

            print(last_name,type(last_name))

            amount = 1

            while amount <= int_of_max_items:

                # Autoscroll for loading contents
                # Porque steamdb necesita hacer scroll para que carguen ciertos datos
                self.driver.execute_script('window.scrollTo(0, ' + str(amount * 150) + ')')
                print('Scrolleando', amount, '/', int_of_max_items)

                amount += 1

            while True:
                amount = int_of_max_items
                try:
                    WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="search_resultsRows"]/a['+str(amount)+']')))
                    break
                except:
                    while True:
                        print('Volviendo a scrollear , item no encontrado', amount, '/ 1000')
                        amount += 1
                        self.driver.execute_script('window.scrollTo(0, '+str(amount * 150)+')')
                        if amount % 1000 == 0:
                            break


            #_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#_*#


            print('Llegamos al ultimo resultado de la lista, agregando los juegos que faltaban')

            amount = len(test_skip_items)

            confirmacion = True

            while amount <= int_of_max_items:

                if confirmacion:
                    confirmacion = False
                    amount += 1
                    continue
                else:
                    pass

                # Autoscroll for loading contents
                # Porque steamdb necesita hacer scroll para que carguen ciertos datos
                self.driver.execute_script('window.scrollTo(0, '+str(amount * 150)+')')

                # Pick 1 item from the list for further examination
                data = WebDriverWait(self.driver, 150).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="search_resultsRows"]/a['+str(amount)+']')))

                # AppID
                try:
                    List_AppID = data.get_attribute("data-ds-appid")
                    LAppID.append(List_AppID)
                    # FullAppidLink
                    LSteamcardexchangeLink.append(
                        'https://www.steamcardexchange.net/index.php?gamepage-appid-'+str(List_AppID))

                    # SteamStoreLink
                    LSteamStoreLink.append('https://store.steampowered.com/app/'+str(List_AppID))
                except:
                    LAppID.append("999999")
                    # FullAppidLink
                    LSteamcardexchangeLink.append(
                        'https://www.steamcardexchange.net/index.php?gamepage-appid-999999')

                    # SteamStoreLink
                    LSteamStoreLink.append('https://store.steampowered.com/app/-999999')

                # Name
                try:
                    List_Name = data.find_element(By.CSS_SELECTOR, 'span[class="title"]').get_attribute("innerHTML")
                    LName.append(List_Name)
                except:
                    LName.append("Not found")

                # GamePrice
                try:
                    List_Game_Price = data.find_element(By.CSS_SELECTOR,
                                                        'div[class="col search_price discounted responsive_secondrow"]').get_attribute(
                        "innerHTML").replace("ARS$ ", "")
                    LGamePrice.append(
                        float(((List_Game_Price.split("<br>")[1]).replace(" ", "")).replace(",", ".")))
                except:
                    LGamePrice.append(float(999))

                # Discount
                try:
                    List_Discount = data.find_element(By.CSS_SELECTOR,
                                                      'div[class="col search_discount responsive_secondrow"]').get_attribute(
                        "innerHTML")
                    LDiscount.append((List_Discount.split(">")[1]).split('<')[0])
                except:
                    LDiscount.append("Without discount")

                if amount == 0:
                    pass

                elif amount % 100 == 0:
                    self.Page1_SaveData()

                amount += 1

                # print("###########################")
                # print(len(LAppID)," ",LAppID)
                # print(len(LName)," ",LName)
                # print(len(LGamePrice)," ",LGamePrice)
                # print(len(LDiscount), " ", LDiscount)
                # print(len(LSteamcardexchangeLink), " ", LSteamcardexchangeLink)
                # print(len(LSteamStoreLink), " ", LSteamStoreLink)
                # print ("###########################")
                t = time.localtime()
                print(str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'|JuegosProfit-2.5.0|DEBUG|PP', amount, '/',
                      max_items)
            Backup().Page1_SaveData()
            LimpiaConsola()

        elif len(test_skip_items) == int_of_max_items:
            print('Primera parte completada por la visto, avanzando a la segunda.')
            pass



class SecondMainPage(MainPage):

    def GdataExtra(self):
        df = pd.read_excel('logs/excel/log.xlsx')

        test_skip_items2 = list(df["Days since the offer started"].dropna())

        len_of_skip_items = len(test_skip_items2)

        if len_of_skip_items == 0:

            print('Lista de ofertas vacia , arrancando desde 0')

            LAppIDPLUS = list(df["AppID"].dropna())
            LNamePLUS = list(df["Name"].dropna())

            del df

            try:
                t = time.localtime()
                print(str(time.strftime("%Y-%m-%d %H:%M:%S",
                                        t))+'|JuegosProfit-2.5.0|INFO|SP|Intentando cargar la pagina , tiempo de expera maximo , 10 minutos')
                search_bar = WebDriverWait(self.driver, 150).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'input[type=search][aria-controls="DataTables_Table_0"]')))
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
                    new_results = WebDriverWait(self.driver, 150).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[.]')))

                    amountPLUS = 1
                    for item in new_results:

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

                    if amount == 0:
                        pass

                    elif amount % 100 == 0:
                        self.Page2_SaveData()

                    search_bar.clear()

                    amount += 1

                except TypeError:
                    invalid_data()
                    search_bar.clear()
                    if amount == 0:
                        pass

                    elif amount % 100 == 0:
                        self.Page2_SaveData()
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
                search_bar = WebDriverWait(self.driver, 150).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'input[type=search][aria-controls="DataTables_Table_0"]')))
            except:
                t = time.localtime()
                print(str(time.strftime("%Y-%m-%d %H:%M:%S",
                                        t))+'|JuegosProfit-2.5.0|INFO|SP|Error y/o tiempo de espera excedido')
                self.driver.close()
            amount = 0

            t = time.localtime()
            print(
                str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'|JuegosProfit-2.5.0|INFO|SP|Cargando juegos en steamdb...')

            for name in LNamePLUS:

                try:
                    name = Remove_unsoported_characters(name)
                    search_bar.send_keys(name)
                    new_results = WebDriverWait(self.driver, 150).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr[.]')))

                    amountPLUS = 1
                    for item in new_results:

                        try:

                            if float(item.get_attribute("data-appid")) == float(
                                    str(LAppIDPLUS[amount]).replace(',', '.')):

                                sub_info = item.find_elements(By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr['+str(
                                    amountPLUS)+']/td[3]/span/span')

                                List_Discount = item.find_element(By.XPATH,
                                                                  '//*[@id="DataTables_Table_0"]/tbody/tr['+str(
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

                    if amount == 0:
                        pass

                    elif amount % 100 == 0:
                        self.Page2_SaveData()

                    search_bar.clear()

                    amount += 1

                except TypeError:
                    invalid_data()
                    search_bar.clear()
                    if amount == 0:
                        pass

                    elif amount % 100 == 0:
                        self.Page2_SaveData()

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
        print('Guardado final de SP , terminando ejecucion...')
        self.Page2_SaveData()