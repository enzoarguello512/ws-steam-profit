# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from fake_useragent import UserAgent
from selenium import webdriver
# import pandas as pd
from Utiles import *
# import page
import os
import sys
import time
from scrapy.crawler import CrawlerProcess
from fake_useragent import UserAgent
from numpy import argmin
from Utiles import *
import scrapy
import math
import time
from scrapy.crawler import CrawlerProcess
from fake_useragent import UserAgent
import scrapy
import time
from Utiles import *
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


def resource_path(relative_path):
	"si no vas a hacer la vercion '.exe' borra esta funcion , porque sino genera error creo, o al menos si no importas"
	try:
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)



ua = UserAgent()
print(ua.random)
options = webdriver.ChromeOptions()
#options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36')
options.add_argument('user-agent='+str(ua.random))
prefs = {"profile.managed_default_content_settings.images": 2}  # Para no cargar imagenes y acelerar un poco el proceso
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(resource_path("chromedriver.exe"), options=options)

# Para logearnos en steam
driver.get('https://steamcommunity.com/login/home')
#WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'input_username'))).send_keys(
#	'')  # campo de nombre
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'input_username'))).send_keys(
	'')  # campo de nombre
time.sleep(3)
#driver.find_element(By.ID, 'input_password').send_keys('')  # campo de contrasena
driver.find_element(By.ID, 'input_password').send_keys('')  # campo de contrasena
time.sleep(3)
driver.find_element(By.CLASS_NAME, 'login_btn').click()  # boton de inicio de sesion
asd = input('Ya estas listo? y/n')

lista_de_links = [
	'https://store.steampowered.com/app/1334590/Furry_Love/',
	'https://store.steampowered.com/app/504400/Optika/',
	'https://store.steampowered.com/app/628760/The_Adventurer__Episode_1_Beginning_of_the_End/',
	'https://store.steampowered.com/app/1070330/Russian_Life_Simulator/',
	'https://store.steampowered.com/app/412620/CropDuster_Supreme/',
	'https://store.steampowered.com/app/385800/NEKOPARA_Vol_0/',
	'https://store.steampowered.com/app/365110/After_All/',
	'https://store.steampowered.com/app/367260/Dwarven_Brawl_Bros/',
	'https://store.steampowered.com/app/389270/Through_Abandoned_The_Underground_City/',
	'https://store.steampowered.com/app/585690/Minimalism/',
	'https://store.steampowered.com/app/485610/Ball_3D_Soccer_Online/',
	'https://store.steampowered.com/app/391160/The_Deletion/',
	'https://store.steampowered.com/app/296050/Battlepaths/',
	'https://store.steampowered.com/app/1171310/Valakas_Story/',
	'https://store.steampowered.com/app/277430/Halo_Spartan_Assault/',
	'https://store.steampowered.com/app/461490/Kaboom_Monsters/',
	'https://store.steampowered.com/app/349140/Corrosion_Cold_Winter_Waiting_Enhanced_Edition/',
	'https://store.steampowered.com/app/353980/Ankh__Anniversary_Edition/',
	'https://store.steampowered.com/app/80350/Blackwell_Convergence/',
	'https://store.steampowered.com/app/597040/Dumbass_Drivers/',
	'https://store.steampowered.com/app/286810/Hard_Truck_Apocalypse_Rise_Of_Clans__Ex_Machina_Meridian_113/',
	'https://store.steampowered.com/app/453100/Frederic_Resurrection_of_Music_Directors_Cut/',
	'https://store.steampowered.com/app/441870/OutDrive/',
	'https://store.steampowered.com/app/280460/Pulstar/',
	'https://store.steampowered.com/app/300620/Flyhunter_Origins/',
	'https://store.steampowered.com/app/507520/ZzzzZzzzZzzz/',
	'https://store.steampowered.com/app/447850/The_Next_Door/',
	'https://store.steampowered.com/app/614910/monstercakes/',
	'https://store.steampowered.com/app/618140/Barro/',
	'https://store.steampowered.com/app/805940/RUSSIA_BATTLEGROUNDS/',
	'https://store.steampowered.com/app/311080/Echelon/',
	'https://store.steampowered.com/app/352120/Fair_Strike/',
	'https://store.steampowered.com/app/519200/Kitty_Kitty_Boing_Boing_the_Happy_Adventure_in_Puzzle_Garden/',
	'https://store.steampowered.com/app/421140/Blades_of_the_Righteous/',
	'https://store.steampowered.com/app/581800/Super_Cuber/',
]
for i in range(12):
	for link in lista_de_links:
		driver.get(link)
		asd4 = WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[class="btn_green_steamui btn_medium"]'))).click()
		asd2 = input('Esta bien?')
	asd3 = input('Mandalo a algun amigo')




