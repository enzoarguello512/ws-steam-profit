from selenium.webdriver.common.by import By

class MainPageLocators(object):
    "Aca van toda la lista de items que queremos y que metodo vamos a usar , tipo id,xpath,class,etc"
    DivGames = (By.XPATH,   )
    Name = ()
    TypeOfSale = ()    #60 items son   #Toma 0 o mas parametros
    Discount = (By.XPATH,   '//*[@id="DataTables_Table_0"]/tbody/tr[.]/td[4]')

class MainPageAtrLoc(object):
    AppID =
    Name = "text"
    pattern = r"(.)*"


class SearchResultsPageLocators(object):
    pass