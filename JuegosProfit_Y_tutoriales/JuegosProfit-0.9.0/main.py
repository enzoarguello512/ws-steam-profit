from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import page
from locator import *


class FindGamesOn(object):

    def __init__(self):
        ua = UserAgent ()
        opts = Options ()
        opts.add_argument ('user-agent=' + str (ua.random))
        self.driver = webdriver.Chrome("chromedriver.exe", chrome_options = opts)
        # self.driver.get("https://steamdb.info/sales/?max_price=300&min_reviews=0&min_rating=0&min_discount=0&category=29")    #Todo tipo de software(juegos, dlc, peliculas,etc)
        self.driver.get("https://steamdb.info/sales/?max_price=300&min_reviews=0&min_rating=0&min_discount=0&category=29&displayOnly=Game") #Todo tipo de juego
        #self.driver.get('https://steamdb.info/sales/?max_price=7&min_reviews=0&min_rating=0&min_discount=0&category=29&displayOnly=Game')  #Solamente 60 items , para tests
        #self.driver.maximize_window()

    def search_games_list(self):
        backup = page.Backup()
        mainPage = page.MainPage (self.driver)
        navigator = page.Navigation(self.driver)
        # backup.CreateLogFolder()
        backup.DTFS()

        navigator.ClickTagPrice ()
        navigator.ShowEntries ()  # 250 , disable for only 50
        while True:
            mainPage.Gwait ()
            mainPage.Gdata ()
            try:
                navigator.ClickNext()
            except:
                break

        # navigator.new_tab()
        # mainPage.LoadContents()
        backup.SaveData()













if __name__ == '__main__':
    FindGamesOn().search_games_list()
