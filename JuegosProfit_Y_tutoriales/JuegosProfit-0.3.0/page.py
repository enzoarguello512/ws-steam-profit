from locator import *
from element import BasePageElement

class SearchTextElement(BasePageElement):
    locator = "q"

class BasePage(object):
    def __init__(self, driver):
        self.driver = driver

class MainPage(BasePage):

    search_text_element = SearchTextElement()

    def is_tittle_matches(self):
        return "Python" in self.driver.title

    def click_go_button(self):
        element = self.driver.find_element(*MainPageLocators.GO_BUTTON) #El asterisco desempaqueta la tupla , y la pasa como argumento , ahora en vez de tener un valor , tenemos 2 , y son argumentos
        element.click()

class SearchResultPage(BasePage):

    def is_result_found(self):
        return "No results found" not in self.driver.page_source