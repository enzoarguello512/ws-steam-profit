import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#https://steamdb.info/sales/?max_price=300&min_reviews=0&min_rating=0&min_discount=0&category=29

#Data interesante
#https://www.steamcardexchange.net/index.php?showcase                      Sin juego
#https://www.steamcardexchange.net/index.php?gamepage-appid-525480         Con juego
#https://www.steamcardexchange.net/index.php?gamepage-appid-439550 xxxxx

#https://steamcommunity.com/market/search?appid=753&category_753_Game%5B%5D=tag_app_603750                          mercado del item
#https://steamcommunity.com/market/search?appid=753&category_753_Game%5B%5D=tag_app_603750#p1_price_asc             mercado del item con precio descendente
#https://steamcommunity.com/market/search?appid=753&category_753_Game%5B%5D=tag_app_603750&q=Cromo#p1_price_asc     mercado del item con precio dsdent. y solo cromos
#Lo unico que creo que varia es el tag app y listo

#Datos que serian utiles:
# Nombre:
# Precio
# App idd para comparar a ver si sale rentable
# Y si estuvo mas barato en algun momento

chrome_driver = webdriver.Chrome("chromedriver.exe")
chrome_driver.get("https://steamdb.info/sales/?max_price=300&min_reviews=0&min_rating=0&min_discount=0&category=29")
time.sleep(15)
Buscador = chrome_driver.find_elements_by_xpath('//*[@id="DataTables_Table_0"]/tbody/tr')
try:
    ListadoDeJuegos = WebDriverWait(chrome_driver, 600).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr'))
    )
    for i in ListadoDeJuegos:
        print(i.text)
except:
    print("Tiempo de demora excedido , 10 minutos pasaron y no se recibio respuesta de la pagina , intenta en otro momento")
finally:
    print("Listo")