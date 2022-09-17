from selenium.common.exceptions import NoSuchElementException, TimeoutException
# from fake_useragent import UserAgent
from selenium import webdriver
import pandas as pd
from Utiles import *
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys




def resource_path (relative_path):
    "si no vas a hacer la vercion '.exe' borra esta funcion , porque sino genera error creo, o al menos si no importas"
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath (".")

    return os.path.join (base_path, relative_path)

ua = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument('user-agent='+str(ua.random))
prefs = {"profile.managed_default_content_settings.images": 2}  # Para no cargar imagenes y acelerar un poco el proceso
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(resource_path("chromedriver.exe"), options=options)



df = pd.read_excel('logs/excel/logR.xlsx')
LAppID = df["Appid"]    #Agarramos todas las appid's de nuestro excel ya refinado
LName = df["Name"]

sql = 'SELECT `Cheapest card price (ARS)` FROM jp_datos_market' #Mas que todo para fijarnos si ya hay algun item que
#podamos skipear
c.execute(sql)
list_of_card_price = c.fetchall()
j = 0
for card in list_of_card_price: #Nos devuelve una lista solamente con los valores que tengan resultados , si es que hay
    list_of_card_price[j] = card[0]
    j += 1

o = 0
#nos fijamos si podemos adelantar algun item ,en la base de datos los items none son los incompletos

if len(list_of_card_price) == 0:
    superId = 0
for offer in list_of_card_price:
    if offer is None:
        superId = o  # es aproposito , tiene que ser una 'o' porque fijate que representa nuestro contador
        break
    elif offer == list_of_card_price[-1]:  # Si es el ultimo elemento , directamente que no ejecute el programa
        superId = len(LAppID[superId:])  #Quedaria algo asi como 33/33, osea un solo item en la lista, esto por si ya esta llena la lista
    else:
        o += 1

for name in list(LName):
    sql = 'insert into jp_datos_market (Name) values (%s)'
    values = (name,)
    c.execute(sql, values)
db.commit()


LAppID = list(LAppID[superId:])
LName = list(LName[superId:])

#Para logearnos en steam
driver.get('https://steamcommunity.com/login/home')
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'input_username'))).send_keys('')   #campo de nombre
time.sleep(3)
driver.find_element(By.ID, 'input_password').send_keys('')   #campo de contrasena
time.sleep(3)
driver.find_element(By.CLASS_NAME, 'login_btn').click() #boton de inicio de sesion
time.sleep(6)

amount = 0

for appid in LAppID:
    name = LName[superId + amount]
    print(appid)
    if appid == 'Bundle/NoID':  #Porque los bundles es muy probable que tiren error
        print('Skipeando bundle')
        continue
    link_modificado = f'https://steamcommunity.com/market/search?q=&category_753_Game%5B%5D=tag_app_{appid}&category_753_item_class%5B%5D=tag_item_class_2&appid=753#p1_price_asc'
    driver.get(link_modificado)

    while True:
        try:
            LCromos = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'market_listing_row_link')))
        except TimeoutException:
            print('Tiempo de espera excedido para cargar la pagina de cromos')
            break

        print(len(LCromos), 'Cromos encontrados')

        for cromo in LCromos:
            try:
                precio_del_cromo = cromo.find_element(By.CLASS_NAME, 'normal_price').text
                precio_del_cromo = precio_del_cromo.split('$')[-1].split(' ')[0]
                tipo_de_cromo = cromo.find_element(By.CLASS_NAME, 'market_listing_game_name').text
            except:
                precio_del_cromo = None
                print('No se encontraron cromos dentro de la pagina')
                break
            if precio_del_cromo == '0.00':
                print('cromo en valor de 0 pesos, continuando con los siguientes')
                continue
            elif tipo_de_cromo.startswith('Cromo Reflectante'):
                print('Cromo reflectante en menor valor, continuando con el siguiente para obtener un mejor valor')
                continue
            else:
                print('Cromo conseguido exitosamente')
                link_al_cromo = cromo.get_attribute("href")
                print(link_al_cromo)
                precio_del_cromo = float(precio_del_cromo)
                print(precio_del_cromo)
                break
        try:
            boton_de_sig_pagina = driver.find_element(By.ID, 'searchResults_btn_next').click()
            color_de_boton_sg = boton_de_sig_pagina.value_of_css_property("background-color")
            print('soy color de fondo de boton de siguiente pagina', color_de_boton_sg)
        except:    #Por si no hay una siguiente pagina salimos del bucle asi continuamos con el siguiente juego
            print('No se detecto ninguna pagina siguiente')
            break

    sql = 'update jp_datos_market set Name = %s, ' \
          ' `Market direct link` = %s,' \
          ' `Cheapest card price (ARS)` = %s, ' \
          ' `Market links cheapest card` = %s where Name = %s'
    values = (name, link_modificado, precio_del_cromo, link_al_cromo, name)

    c.execute(sql, values)

    amount += 1

    if amount % 11 == 0:
        print('Guardando en base de datos')
        db.commit()
        print('Entrando en colldown')
        time.sleep(298)
        print('Volviendo a buscar')
        time.sleep(2)

    print('################################################')
    t = time.localtime()
    print(str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'|JuegosProfit-2.5.0|INFO|CP|', amount, '/', len(LAppID))
    print('################################################')

db.commit()


