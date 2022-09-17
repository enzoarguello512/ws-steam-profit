from selenium import webdriver
#from fake_useragent import UserAgent
import page


class FindGamesOn(object):

    def __init__(self):
        #ua = UserAgent ()
        #options = webdriver.ChromeOptions()
        #options.add_argument ('user-agent=' + str (ua.random))
        self.driver = webdriver.Chrome("chromedriver.exe")  #options = options
        # Vercion 400+ resultados
        self.driver.get('https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&ignore_preferences=1')

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
