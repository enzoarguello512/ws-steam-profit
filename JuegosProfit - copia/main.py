from selenium import webdriver
#from fake_useragent import UserAgent
import page
import os
import sys

def resource_path (relative_path):
    "si no vas a hacer la vercion '.exe' borra esta funcion , porque sino genera error creo, o al menos si no importas"
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath (".")

    return os.path.join (base_path, relative_path)

class FindGamesOn(object):

    def __init__(self):
        #ua = UserAgent ()
        #options = webdriver.ChromeOptions()
        #options.add_argument ('user-agent=' + str (ua.random))
        self.driver = webdriver.Chrome(resource_path("chromedriver.exe"))  #options = options
        # Vercion 400+ resultados
        #self.driver.get('https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&ignore_preferences=1')
        # Version actualizada 507+ resultados 2020:
        self.driver.get('https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992%2C993&category2=29&specials=1&ignore_preferences=1')
        #Vercion 300 items
        #self.driver.get('https://store.steampowered.com/search/?sort_by=Price_ASC&ignore_preferences=1&maxprice=70&category1=998%2C994%2C992&category2=29&specials=1')
        self.driver.maximize_window()

    def search_games_list(self):
        backup = page.Backup()
        mainPage = page.MainPage(self.driver)
        secondPage = page.SecondMainPage(self.driver)
        backup.CreateLogFolder()
        backup.DTFS()   #Creamos el dataframe si es que no existe
        mainPage.Gwait()
        mainPage.Gdata()

        # -------------Opcional Part---------------
        backup.Page1_SaveData()

        self.driver.get('https://steamdb.info/sales/')
        secondPage.GdataExtra()
        backup.Page2_SaveData()



        # ---------------------------------------
        #secondPage.LoadContents()

        #backup.Post_SaveData()
        #backup.Full_Savedata()


if __name__ == '__main__':
    FindGamesOn().search_games_list()
