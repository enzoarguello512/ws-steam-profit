from scrapy.crawler import CrawlerProcess
from fake_useragent import UserAgent
import scrapy
import time
from Utiles import *


#Hacer un bot que revise los precios de arg en particular , osea de los resultados buenos que busque esos que son re poquitos en comparasion con los otros
#Y hacer un bot que agregue una columna con el link a los articulos de un determinado juego por ejemplo para comprobar precios de manera manual mucho mas rapido
#agregar una columna que te diga cada cuanto es el promedio de venta dentro de las 24 horas , a ver si sale rentable comprarlo o no , porque puede tener el re precio
#pero si no se vende no sirve

# https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&ignore_preferences=1
# https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&ignore_preferences=1
# https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1
# https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&page=1
# https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&ignore_preferences=1&page=1

page_number = 0
ua = UserAgent ()
max_items_finded = False

def link_sanitizer(link):
    new_link = []
    link_separator = link.split('/')
    del link_separator[-1]
    for part in link_separator:
        if part == '':
            continue
        elif part.startswith('http'):
            new_link.append(part)
            new_link.append('/' * 2)
        else:
            new_link.append(part)
            new_link.append('/')
    new_link = "".join(new_link)
    return new_link

class SteamGameFinder(scrapy.Spider):
	name = 'SteamGameFinder'
	#SI VAS A USAR EL FICHERO LOCAL DESACTIVA LA PARTE DE NEXT-PAGE ASI NO TIRA ERROR
	# start_urls = ['file:///C:/Users/maquinadefiambre/PycharmProjects/JuegosProfit/ReworkJuegosProfit/PruebaDeSpider.html']
	start_urls = ['https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&ignore_preferences=1&page=33']
	custom_settings = {
		'DOWNLOAD_DELAY': 1.0,
		# Lo ideal para mi seria entre 2 o 3 , hay veces que capas tira error el programa , porque se seba con las peticiones por minuto , no es error del el programa en si , es culpa de la pagina que nos limita
		'CONCURRENT_REQUESTS': 1,
		'USER_AGENT': str(ua.random),
		# Para evitar un posible van de 'navegador' , pero no evitariamos uno de ip , para eso esta TOR browser
		'AUTOTHROTTLE_ENABLED': True,
		'AUTOTHROTTLE_START_DELAY': 5,
		'AUTOTHROTTLE_MAX_DELAY': 60,
		'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
		'AUTOTHROTTLE_DEBUG': True,
		'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
		'RANDOMIZE_DOWNLOAD_DELAY': False,
	}


	def parse(self, response):

		global page_number
		global max_items_finded

		#Check if we are in a empty page
		page_exists = response.xpath('//*[@id="search_result_container"]/p[2]').get()
		if page_exists is not None: #Osea si es cualquier cosa menos None , que ejecute este codigo y ya salga
			print('Pagina inexistente, terminando ejecucion')

		else:
			page = response.url.split('=')[-1]  #Agarramos el numero de la pagina para despues sumarle 1 al final de ejecusion y asi saltar de pagina

			amount = 1  #Es mas que todo como un contador en caso de que ocurra un error , asi lo corto de raiz rapido
			for game in response.css('.search_result_row'): #Basicamente busca los juegos , aprox 25 por pagina

				#Appid
				try:
					LAppID_pre = game.css('.search_result_row::attr(data-ds-appid)').get()
					LAppID = int(LAppID_pre)

				except:
					print('exception in appid. Number:', amount, 'Page:', page_number)
					LAppID = 'Bundle/NoID'

				#Name
				try:
					LName = game.css('span[class="title"]::text').get()
					# LName.append(response.xpath('//*[@id="search_resultsRows"]/a[' + str(amount) + ']/div[2]/div[1]/span/text()').get())
				except:
					print('exception in name. Number:', amount, 'Page:', page_number)
					LName = "Not found"

				#Game price
				try:
					LGamePrice_pre = game.css('div[class="col search_price discounted responsive_secondrow"]').get()
					LGamePrice = float((LGamePrice_pre.split('<br>')[1].split(' ')[1]).replace(',', '.'))
					# LGamePrice.append(response.xpath('//*[@id="search_resultsRows"]/a[' + str(amount) + ']/div[2]/div[4]/div[2]/text()').get())
				except:
					print('exception in game price. Number:', amount, 'Page:', page_number)
					LGamePrice = float(999)

				#Discount
				try:
					LDiscount_pre = game.css('div[class="col search_discount responsive_secondrow"]').get()
					LDiscount = LDiscount_pre.split('<')[2].split('>')[1]
					# LDiscount.append(response.xpath('//*[@id="search_resultsRows"]/a[' + str(amount) + ']/div[2]/div[4]/div[1]/span/text()').get())
				except:
					print('exception in discount. Number:', amount, 'Page:', page_number)
					LDiscount = "Without discount"

				# SteamStoreLink
				try:
					LSteamStoreLink_pre = game.css('.search_result_row::attr(href)').get()
					LSteamStoreLink = link_sanitizer(LSteamStoreLink_pre)
				except:
					print('exception in steam store link. Number:', amount, 'Page:', page_number)
					LSteamStoreLink = 'Not found'

				# FullAppidLink
				try:
					LSteamcardexchangeLink_pre = LSteamStoreLink_pre.split('/')[4]  #Appid
					LSteamcardexchangeLink = 'https://www.steamcardexchange.net/index.php?gamepage-appid-' + LSteamcardexchangeLink_pre
				except:
					print('exception in full appid link. Number:', amount, 'Page:', page_number)
					LSteamcardexchangeLink = 'Not found'

				#Market Direct Link
				if LSteamcardexchangeLink == 'Not found':
					LMarketDirectLink = 'Not found'
				else:
					LMarketDirectLink = f'https://steamcommunity.com/market/search?appid=753&category_753_Game%5B%5D=tag_app_{LSteamcardexchangeLink_pre}#p1_price_asc'



				amount += 1

				#Datos sin refinar
				sql = 'insert into jp_sin_refinar (AppID, Name, `Game price (ARS)`, Discount, `Steam store link`, `Steamcardexchange link`) values (%s, %s, %s, %s, %s, %s)'
				values = (LAppID, LName, LGamePrice, LDiscount, LSteamStoreLink, LSteamcardexchangeLink)
				c.execute(sql, values)

				# Datos refinados
				sql = 'insert into jp_refinados (AppID, Name, `Game price (ARS)`, Discount, `Steam store link`, `Steamcardexchange link`, `Market direct link`) values (%s, %s, %s, %s, %s, %s, %s)'
				values = (LAppID, LName, LGamePrice, LDiscount, LSteamStoreLink, LSteamcardexchangeLink, LMarketDirectLink)
				c.execute(sql, values)

			# print(len(LAppID), LAppID)
			# print(len(LName), LName)
			# print(len(LGamePrice), LGamePrice)
			# print(len(LDiscount), LDiscount)
			# print(len(LSteamStoreLink), LSteamStoreLink)
			# print(len(LSteamcardexchangeLink), LSteamcardexchangeLink)

			t = time.localtime()
			print(str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'|JuegosProfit-2.5.0|DEBUG|PP', page_number)


			#ESTA PARTE DESACTIVALA SI VAS A USAR EL FICHERO LOCAL

			next_page = 'https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&ignore_preferences=1&page=' + str(int(page) + 1)
			yield scrapy.Request(next_page, callback=self.parse)

			page_number += 1



process = CrawlerProcess()
process.crawl(SteamGameFinder)
Backup().CreateLogFolder()
Backup().DTFS() #Borra la antigua base de datos y inicia la base de datos
process.start()
db.commit()

