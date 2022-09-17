import unittest
from selenium import webdriver
import page

class BusquedaDeJuegos(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.driver.get("https://www.python.org/")

    def test_search_python(self):    #Corre cada test por separado y que empiece por la palabra "test"
        mainPage = page.MainPage(self.driver)
        assert mainPage.is_tittle_matches()
        mainPage.search_text_element = "pycon"
        mainPage.click_go_button()
        search_result_page = page.SearchResultPage(self.driver)
        assert search_result_page.is_result_found()

    #def tearDown(self):
        #self.driver.close()

if __name__ == "__main__":   #Basicamente le decimos que si el nombre de este archivo es main , que corra el codigo de abajo
    unittest.main() #Y el codigo de abajo esta llamando a todas las instancias y herencias de unittest , por lo tanto estamos corriendo nuestra clase











