from scrapy.crawler import CrawlerProcess
from fake_useragent import UserAgent
import scrapy


SUPERURL = 'https://steamdb.info/sales/'

ua = UserAgent ()

class SteamGameFinder(scrapy.Spider):
	name = 'test'
	start_urls = [SUPERURL]

	custom_settings = {
		# 'DOWNLOAD_DELAY': 1.2,
		# # Lo ideal para mi seria entre 2 o 3 , hay veces que capas tira error el programa , porque se seba con las peticiones por minuto , no es error del el programa en si , es culpa de la pagina que nos limita
		# 'CONCURRENT_REQUESTS': 1,
		#'USER_AGENT': str(ua.random),
		# # Para evitar un posible van de 'navegador' , pero no evitariamos uno de ip , para eso esta TOR browser
		# 'AUTOTHROTTLE_ENABLED': True,
		# 'AUTOTHROTTLE_START_DELAY': 5,
		# 'AUTOTHROTTLE_MAX_DELAY': 60,
		# 'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
		# 'AUTOTHROTTLE_DEBUG': True,
		# 'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
		# 'RANDOMIZE_DOWNLOAD_DELAY': False,
	}

	def parse(self,response):

		filename = 'ResultadoPrueba.html'

		with open(filename, 'wb') as f:
			f.write(response.body)

process = CrawlerProcess()
process.crawl(SteamGameFinder)
process.start()
