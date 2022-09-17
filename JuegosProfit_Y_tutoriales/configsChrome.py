import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent



# username = os.getenv("USERNAME")
# userProfile = "C:\\Users\\maquinadefiambre\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
# options = webdriver.ChromeOptions()
# ua = UserAgent()
# options.add_argument('user-agent=' + str(ua.random))
#
# options.add_argument("user-data-dir={}".format(userProfile))
# options.add_argument("--disable-blink-features")
# options.add_argument("--disable-blink-features=AutomationControlled")
# # add here any tag you want.
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors", "safebrowsing-disable-download-protection", "safebrowsing-disable-auto-update", "disable-client-side-phishing-detection"])
# chromedriver = "chromedriver.exe"
# os.environ["webdriver.chrome.driver"] = chromedriver
# driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
# driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#   "source": """
#     Object.defineProperty(navigator, 'webdriver', {
#       get: () => undefined
#     })
#   """
# })
# print(driver.execute_script("return navigator.userAgent;"))
# driver.get('https://steamdb.info/sales/?max_price=7&min_reviews=0&min_rating=0&min_discount=0&category=29&displayOnly=Game')
driver = webdriver.Chrome("chromedriver.exe")
#https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&ignore_preferences=1
#de ahi scamos los juegos
#de steam exchange los precios
#de https://steamdb.info/sales/
#sacamos los fechas y lowest recorded