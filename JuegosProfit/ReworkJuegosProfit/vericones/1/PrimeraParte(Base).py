from scrapy.crawler import CrawlerProcess
from fake_useragent import UserAgent
from numpy import argmin
import pandas as pd
import scrapy
import math
import time
import os

LAppID = []
LName = []
LGamePrice = []
LDiscount = []
LCheapestCardPrice = []
LPreciosArs = []
LNumberOfCardsInTotal = []  #
LObtainableCards = []  #
LSteamCommission = []  #
LValueOfTheCardsObtainableWithoutTheSteamCommission = []  #
LApproximateMinimumProfit = []  #
LPriceMultipliedByNumberOfAccounts = []  #
LPaidOut = []  #
LDateOfPurchase = []  #
LOfferType = []
LNewHighestDiscount = []
LDaysSinceTheOfferStarted = []
LDaysForTheOfferToEnd = []
LSteamStoreLink = []
LSteamcardexchangeLink = []

# https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&ignore_preferences=1
# https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&ignore_preferences=1
# https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1
# https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&page=1
# https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&ignore_preferences=1&page=1
page_number = 0

class SteamGameFinder(scrapy.Spider):
	name = 'SteamGameFinder'
	start_urls = ['file:///C:/Users/maquinadefiambre/PycharmProjects/JuegosProfit/ReworkJuegosProfit/PruebaDeSpider.html']
	# start_urls = ['https://store.steampowered.com/search/?sort_by=Price_ASC&maxprice=350&category1=998%2C994%2C992&category2=29&specials=1&ignore_preferences=1&page=8']

	def parse(self, response):

		global page_number
		page_number += 1
		page = response.url.split('/')[-1]

		# List of game showing in page , and we also use the same line to get the appid's
		# l_visible_games = response.css('.search_result_row').getall()

		amount = 1
		for game in response.css('.search_result_row'):

			#Appid
			try:
				LAppID_pre = game.css('.search_result_row::attr(data-ds-appid)').get()
				LAppID.append(LAppID_pre)
				# FullAppidLink
				LSteamcardexchangeLink.append(
					'https://www.steamcardexchange.net/index.php?gamepage-appid-'+str(LAppID_pre))

				# SteamStoreLink
				LSteamStoreLink.append('https://store.steampowered.com/app/'+str(LAppID_pre))
			except:
				print('exception in appid. Number:', amount, 'Page:', page_number)
				LAppID.append('999999')
				# FullAppidLink
				LSteamcardexchangeLink.append(
					'https://www.steamcardexchange.net/index.php?gamepage-appid-999999')

				# SteamStoreLink
				LSteamStoreLink.append('https://store.steampowered.com/app/999999')

			#Name
			try:
				LName.append(game.css('span[class="title"]::text').get())
				# LName.append(response.xpath('//*[@id="search_resultsRows"]/a[' + str(amount) + ']/div[2]/div[1]/span/text()').get())
			except:
				print('exception in name. Number:', amount, 'Page:', page_number)
				LName.append("Not found")

			#Game price
			try:
				LGamePrice_pre = game.css('div[class="col search_price discounted responsive_secondrow"]').get()
				LGamePrice.append(float((LGamePrice_pre.split('<br>')[1].split(' ')[1]).replace(',', '.')))
				# LGamePrice.append(response.xpath('//*[@id="search_resultsRows"]/a[' + str(amount) + ']/div[2]/div[4]/div[2]/text()').get())
			except:
				print('exception in game price. Number:', amount, 'Page:', page_number)
				LGamePrice.append(float(999))

			#Discount
			try:
				LDiscount_pre = game.css('div[class="col search_discount responsive_secondrow"]').get()
				LDiscount.append(LDiscount_pre.split('<')[2].split('>')[1])
				# LDiscount.append(response.xpath('//*[@id="search_resultsRows"]/a[' + str(amount) + ']/div[2]/div[4]/div[1]/span/text()').get())
			except:
				print('exception in discount. Number:', amount, 'Page:', page_number)
				LDiscount.append("Without discount")




			amount += 1

		print(len(LAppID), LAppID)
		print(len(LName), LName)
		print(len(LGamePrice), LGamePrice)
		print(len(LDiscount), LDiscount)
		print(len(LSteamStoreLink), LSteamStoreLink)
		print(len(LSteamcardexchangeLink), LSteamcardexchangeLink)

		t = time.localtime()
		print(str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'|JuegosProfit-2.5.0|DEBUG|PP', amount, '/', page_number)



		# filename = 'PruebaDeSpider.html'
		# with open(filename, 'wb') as f:
		# 	f.write(response.body)

process = CrawlerProcess()
process.crawl(SteamGameFinder)  # 'asd' representa el nombre de nuestra clase que contenga el spider
process.start()
