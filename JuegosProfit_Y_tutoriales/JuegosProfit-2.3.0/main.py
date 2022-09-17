from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import page



#https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&ignore_preferences=1


class FindGamesOn(object):

    # def __init__(self):
    #     ua = UserAgent ()
    #     opts = Options ()
    #     opts.add_argument ('user-agent=' + str (ua.random))
    #     self.driver = webdriver.Chrome("chromedriver.exe", chrome_options = opts)
    #     #Vercion 400+ resultados
    #     #self.driver.get('https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&ignore_preferences=1')
    #     #Vercion 300 items
    #     self.driver.get('https://store.steampowered.com/search/?sort_by=Price_ASC&ignore_preferences=1&maxprice=70&category1=998%2C994%2C992&category2=29&specials=1')
    #     self.driver.maximize_window()

    def search_games_list(self):
        # backup = page.Backup()
        # mainPage = page.MainPage (self.driver)
        # #secondPage = page.SecondMainPage(self.driver)
        # backup.CreateLogFolder()
        # backup.DTFS()
        # #mainPage.Gwait()
        # #mainPage.Gdata()
        # -------------Opcional Part---------------
        pass


        #backup.Pre_SaveData()

        # ---------------------------------------
        #secondPage.LoadContents()

        #backup.Post_SaveData()
        #backup.Full_Savedata()


if __name__ == '__main__':
    FindGamesOn().search_games_list()
