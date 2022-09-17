from selenium import webdriver
import page

class FindGamesOn(object):

    def __init__(self):
        self.driver = webdriver.Chrome("chromedriver.exe")
        # self.driver.get("https://steamdb.info/sales/?max_price=300&min_reviews=0&min_rating=0&min_discount=0&category=29")
        self.driver.get("https://steamdb.info/sales/?max_price=300&min_reviews=0&min_rating=0&min_discount=0&category=29&displayOnly=Game")
        # self.driver.maximize_window()

    def search_games_list(self):
        backup = page.Backup()
        backup.CreateLogFolder()
        backup.DTFS()
        mainPage = page.MainPage(self.driver)
        mainPage.Gwait()
        mainPage.Gdata()













if __name__ == '__main__':
    FindGamesOn().search_games_list()
