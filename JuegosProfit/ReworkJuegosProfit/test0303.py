import mysql.connector
import pandas as pd
import time
import os

db = mysql.connector.connect(
	host='localhost',
	user='root',
	password='enzo',
	database='juegosprofit'
)
c = db.cursor()
#
# ID = []
# LAppID = []
# LName = []
# LGamePrice = []
# LDiscount = []
# LCheapestCardPrice = []
# LPreciosArs = []
# LNumberOfCardsInTotal = []  #
# LObtainableCards = []  #
# LSteamCommission = []  #
# LValueOfTheCardsObtainableWithoutTheSteamCommission = []
# LSales24Hours = []
# LApproximateMinimumProfit = []  #
# LPriceMultipliedByNumberOfAccounts = []  #
# # LPaidOut = []  #
# LDateOfPurchase = []  #
# LOfferType = []
# LNewHighestDiscount = []
# LDaysSinceTheOfferStarted = []
# LDaysForTheOfferToEnd = []
# LMarketDirectLink = []
# LSteamStoreLink = []
# LSteamcardexchangeLink = []
#
#
# def convert_data_sql():
# 	sql = 'SELECT * FROM jp_refinados'
# 	c.execute(sql)
# 	alldata_per_game = c.fetchall()
#
#
# 	for item in alldata_per_game:
# 		ID.append(item[0])
# 		LAppID.append(item[1])
# 		LName.append(item[2])
# 		LGamePrice.append(item[3])
# 		LDiscount.append(item[4])
# 		LCheapestCardPrice.append(item[5])
# 		LPreciosArs.append(item[6])
# 		LNumberOfCardsInTotal.append(item[7])
# 		LObtainableCards.append(item[8])
# 		LSteamCommission.append(item[9])
# 		LValueOfTheCardsObtainableWithoutTheSteamCommission.append(item[10])
# 		LSales24Hours.append(item[11])
# 		LApproximateMinimumProfit.append(item[12])
# 		LPriceMultipliedByNumberOfAccounts.append(item[13])
# 		# LPaidOut = []  #
# 		LDateOfPurchase.append(item[14])
# 		LOfferType.append(item[15])
# 		LNewHighestDiscount.append(item[16])
# 		LDaysSinceTheOfferStarted.append(item[17])
# 		LDaysForTheOfferToEnd.append(item[18])
# 		LMarketDirectLink.append(item[19])
# 		LSteamStoreLink.append(item[20])
# 		LSteamcardexchangeLink.append(item[21])
#
#
# convert_data_sql()
# print(ID)
# print(LAppID)
# print(LName)
# print(LGamePrice)
# print(LDiscount)
# print(LCheapestCardPrice)
# print(LPreciosArs)
# print(LNumberOfCardsInTotal)
# print(LObtainableCards)
# print(LSteamCommission)
# print(LValueOfTheCardsObtainableWithoutTheSteamCommission)
# print(LSales24Hours)
# print(LApproximateMinimumProfit) #
# print(LPriceMultipliedByNumberOfAccounts) #
# # LPaidOut = []  #
# print(LDateOfPurchase)  #
# print(LOfferType)
# print(LNewHighestDiscount)
# print(LDaysSinceTheOfferStarted)
# print(LDaysForTheOfferToEnd)
# print(LMarketDirectLink)
# print(LSteamStoreLink)
# print(LSteamcardexchangeLink)


class Backup(object):
	"Funciones para guardar nuestros datos / y crear los que hagan falta"

	def CreateLogFolder(self):
		"Creamos las carpetas donde van a ir los logs , si es que no existen , cuidado que se borra el contenido previo de estas"
		try:
			os.makedirs('logs/css-(backup)')
			os.makedirs('logs/excel')
			print('Creating logs folder')
			print("Directory's Created ")
		except FileExistsError:
			pass

	def DTFS(self):
		try:
			init_db()
		except:
			print('No se puedo inicializar la base de datos')

	def Del_Prev_Files(self):
		try:
			os.remove('logs/excel/logNR.xlsx')
			os.remove('logs/excel/logR.xlsx')
			print('Previos log.xlsx borrados exitosamente')
		except:
			print('No se pudo borrar(o no se encontro) el anterior log.xlsx')
			print('Continuando')
		try:
			os.remove('logs/css-(backup)/logNR.csv')
			os.remove('logs/css-(backup)/logR.csv')
			print('Previos log.csv borrados exitosamente')
		except:
			print('No se pudo borrar(o no se encontro) el anterior log.csv')
			print('Continuando')


	def create_dataframe_and_save(self):
		try:
			df = pd.DataFrame({
				#"ID": [],
				"Appid": [],
				"Name": [],
				"Game price (ARS)": [],
				"Discount": [],
				"Cheapest card price (USD)": [],
				"Cheapest card price (ARS)": [],
				"Number of cards in total": [],
				"Obtainable cards": [],
				"Steam commission (ARS)": [],
				"Value of the cards obtainable without the steam commission (ARS)": [],
				"Approximate minimum profit (ARS)": [],
				"Price multiplied by number of accounts (ARS)": [],
				# "Paid out (ARS)" : [],
				"Date of purchase": [],
				"Offer type": [],
				"New highest discount?": [],
				"Days since the offer started": [],
				"Days for the offer to end": [],
				"Steamcardexchange link": [],
				"Steam store link": [],
				"SI": [],
			})
		finally:
			# Problema es que sobreescribe el anterior
			df.to_excel('logs/excel/logNR.xlsx', index=False)
			df.to_csv('logs/css-(backup)/logNR.csv', index=False)


		#REDIFINEDD
		try:
			df = pd.DataFrame({
				#"ID": [],
				"Appid": [],
				"Name": [],
				"Game price (ARS)": [],
				"Discount": [],
				"Cheapest card price (USD)": [],
				"Cheapest card price (ARS)": [],
				"Number of cards in total": [],
				"Obtainable cards": [],
				"Steam commission (ARS)": [],
				"Value of the cards obtainable without the steam commission (ARS)": [],
				'Sales x 24 hours for the cheapest item': [],
				"Approximate minimum profit (ARS)": [],
				"Price multiplied by number of accounts (ARS)": [],
				# "Paid out (ARS)" : [],
				"Date of purchase": [],
				"Offer type": [],
				"New highest discount?": [],
				"Days since the offer started": [],
				"Days for the offer to end": [],
				'Market direct link': [],
				"Steamcardexchange link": [],
				"Steam store link": [],
				"SI": [],
			})
		finally:
			# Problema es que sobreescribe el anterior
			df.to_excel('logs/excel/logR.xlsx', index=False)
			df.to_csv('logs/css-(backup)/logR.csv', index=False)


	def convert_data_sql(self):


		LID = []
		LAppID = []
		LName = []
		LGamePrice = []
		LDiscount = []
		LCheapestCardPrice = []
		LPreciosArs = []
		LNumberOfCardsInTotal = []  #
		LObtainableCards = []  #
		LSteamCommission = []  #
		LValueOfTheCardsObtainableWithoutTheSteamCommission = []
		LSales24Hours = []
		LApproximateMinimumProfit = []  #
		LPriceMultipliedByNumberOfAccounts = []  #
		# LPaidOut = []  #
		LDateOfPurchase = []  #
		LOfferType = []
		LNewHighestDiscount = []
		LDaysSinceTheOfferStarted = []
		LDaysForTheOfferToEnd = []
		LMarketDirectLink = []
		LSteamStoreLink = []
		LSteamcardexchangeLink = []

		sql = 'SELECT * FROM jp_refinados order by `Approximate minimum profit (ARS)` asc'


		c.execute(sql)
		alldata_per_game = c.fetchall()


		for item in alldata_per_game:
			# agarrams cada juego y le sacacamos las caracteristicas y las asignamos a nuestras listas asi despues las
			# podemos convertir a excel
			LID.append(item[0])
			if item[1] == 999999:   #Por si el juego en particular es un bundle
				LAppID.append('Bundle/NoID')
			else:
				LAppID.append(item[1])
			LName.append(item[2])
			if item[3] == 999:  #Por si en la pagina principal de steam(primera parte) no aparece el precio , la
				# mayoria del tiempo se debe a que no esta en oferta el juego
				LGamePrice.append('Without offer/error')
				LApproximateMinimumProfit.append('Cannot be calculated')
				LPriceMultipliedByNumberOfAccounts.append('-')
			else:
				LGamePrice.append(item[3])
				LApproximateMinimumProfit.append(item[12])
				LPriceMultipliedByNumberOfAccounts.append(item[13])
			LDiscount.append(item[4])
			if item[5] == 999:  #Osea si ninguna de las cartas tiene un precio (estilo N/A), esto pasa a veces cuando
				#steamexchange no consigue los precios
				LCheapestCardPrice.append('No records')
				LPreciosArs.append('No records')
				LSteamCommission.append('Cannot be calculated')
				LValueOfTheCardsObtainableWithoutTheSteamCommission.append('Cannot be calculated')
			else:
				LCheapestCardPrice.append(item[5])
				LPreciosArs.append(item[6])
				LSteamCommission.append(item[9])
				LValueOfTheCardsObtainableWithoutTheSteamCommission.append(item[10])

			LNumberOfCardsInTotal.append(item[7])
			LObtainableCards.append(item[8])
			LSales24Hours.append(item[11])
			# LPaidOut = []  #
			LDateOfPurchase.append(item[14])
			LOfferType.append(item[15])
			LNewHighestDiscount.append(item[16])
			LDaysSinceTheOfferStarted.append(item[17])
			LDaysForTheOfferToEnd.append(item[18])
			LMarketDirectLink.append(item[19])
			LSteamStoreLink.append(item[21])    # Los inverti junto con el de abajo porque sino los pones opuestos xD
			LSteamcardexchangeLink.append(item[20])


		#Guardamos la info de los no-refinados
		try:
			df = pd.read_excel('logs/excel/logNR.xlsx')
			#df["ID"] = LID
			df["Appid"] = LAppID
			df["Name"] = LName
			df["Game price (ARS)"] = LGamePrice
			df["Discount"] = LDiscount
			df["Cheapest card price (USD)"] = LCheapestCardPrice
			df["Cheapest card price (ARS)"] = LPreciosArs
			df["Number of cards in total"] = LNumberOfCardsInTotal
			df["Obtainable cards"] = LObtainableCards
			df["Steam commission (ARS)"] = LSteamCommission
			df[
				"Value of the cards obtainable without the steam commission (ARS)"] = LValueOfTheCardsObtainableWithoutTheSteamCommission
			df["Approximate minimum profit (ARS)"] = LApproximateMinimumProfit
			df["Price multiplied by number of accounts (ARS)"] = LPriceMultipliedByNumberOfAccounts
			# df["Paid out (ARS)"] = LPaidOut
			df["Date of purchase"] = LDateOfPurchase
			df["Offer type"] = LOfferType
			df["New highest discount?"] = LNewHighestDiscount
			df["Days since the offer started"] = LDaysSinceTheOfferStarted
			df["Days for the offer to end"] = LDaysForTheOfferToEnd
			df["Steamcardexchange link"] = LSteamcardexchangeLink
			df["Steam store link"] = LSteamStoreLink
			df["SI"] = list(']' * len(LAppID))
		finally:
			df.to_excel('logs/excel/logNR.xlsx', index=False)
			df.to_csv('logs/css-(backup)/logNR.csv', index=False)


		# Volvemos a vaciar las listas para hacer un excel nuevo
		LID = []
		LAppID = []
		LName = []
		LGamePrice = []
		LDiscount = []
		LCheapestCardPrice = []
		LPreciosArs = []
		LNumberOfCardsInTotal = []  #
		LObtainableCards = []  #
		LSteamCommission = []  #
		LValueOfTheCardsObtainableWithoutTheSteamCommission = []
		LSales24Hours = []
		LApproximateMinimumProfit = []  #
		LPriceMultipliedByNumberOfAccounts = []  #
		# LPaidOut = []  #
		LDateOfPurchase = []  #
		LOfferType = []
		LNewHighestDiscount = []
		LDaysSinceTheOfferStarted = []
		LDaysForTheOfferToEnd = []
		LMarketDirectLink = []
		LSteamStoreLink = []
		LSteamcardexchangeLink = []

		sql = 'delete from jp_refinados where `Obtainable cards` = 0'
		c.execute(sql)
		sql = 'SELECT * FROM jp_refinados WHERE `Approximate minimum profit (ARS)` >= 0.0 order by `Approximate minimum profit (ARS)` asc'

		c.execute(sql)
		alldata_per_game = c.fetchall()

		for item in alldata_per_game:
			# agarrams cada juego y le sacacamos las caracteristicas y las asignamos a nuestras listas asi despues las
			# podemos convertir a excel
			LID.append(item[0])
			if item[1] == 999999:   #Por si el juego en particular es un bundle
				LAppID.append('Bundle/NoID')
			else:
				LAppID.append(item[1])
			LName.append(item[2])
			if item[3] == 999:  #Por si en la pagina principal de steam(primera parte) no aparece el precio , la
				# mayoria del tiempo se debe a que no esta en oferta el juego
				LGamePrice.append('Without offer/error')
				LApproximateMinimumProfit.append('Cannot be calculated')
				LPriceMultipliedByNumberOfAccounts.append('-')
			else:
				LGamePrice.append(item[3])
				LApproximateMinimumProfit.append(item[12])
				LPriceMultipliedByNumberOfAccounts.append(item[13])
			LDiscount.append(item[4])
			if item[5] == 999:  #Osea si ninguna de las cartas tiene un precio (estilo N/A), esto pasa a veces cuando
				#steamexchange no consigue los precios
				LCheapestCardPrice.append('No records')
				LPreciosArs.append('No records')
				LSteamCommission.append('Cannot be calculated')
				LValueOfTheCardsObtainableWithoutTheSteamCommission.append('Cannot be calculated')
			else:
				LCheapestCardPrice.append(item[5])
				LPreciosArs.append(item[6])
				LSteamCommission.append(item[9])
				LValueOfTheCardsObtainableWithoutTheSteamCommission.append(item[10])

			LNumberOfCardsInTotal.append(item[7])
			LObtainableCards.append(item[8])
			LSales24Hours.append(item[11])
			# LPaidOut = []  #
			LDateOfPurchase.append(item[14])
			LOfferType.append(item[15])
			LNewHighestDiscount.append(item[16])
			LDaysSinceTheOfferStarted.append(item[17])
			LDaysForTheOfferToEnd.append(item[18])
			LMarketDirectLink.append(item[19])
			LSteamStoreLink.append(item[21])    # Los inverti junto con el de abajo porque sino los pones opuestos xD
			LSteamcardexchangeLink.append(item[20])

		# Guardamos la info de los refinados
		try:
			df = pd.read_excel('logs/excel/logR.xlsx')
			#df["ID"] = LID
			df["Appid"] = LAppID
			df["Name"] = LName
			df["Game price (ARS)"] = LGamePrice
			df["Discount"] = LDiscount
			df["Cheapest card price (USD)"] = LCheapestCardPrice
			df["Cheapest card price (ARS)"] = LPreciosArs
			df["Number of cards in total"] = LNumberOfCardsInTotal
			df["Obtainable cards"] = LObtainableCards
			df["Steam commission (ARS)"] = LSteamCommission
			df[
				"Value of the cards obtainable without the steam commission (ARS)"] = LValueOfTheCardsObtainableWithoutTheSteamCommission
			df['Sales x 24 hours for the cheapest item'] = LSales24Hours
			df["Approximate minimum profit (ARS)"] = LApproximateMinimumProfit
			df["Price multiplied by number of accounts (ARS)"] = LPriceMultipliedByNumberOfAccounts
			#df["Paid out (ARS)"] = LPaidOut
			df ["Date of purchase"] = LDateOfPurchase
			df["Offer type"] = LOfferType
			df["New highest discount?"] = LNewHighestDiscount
			df["Days since the offer started"] = LDaysSinceTheOfferStarted
			df["Days for the offer to end"] = LDaysForTheOfferToEnd
			df['Market direct link'] = LMarketDirectLink
			df["Steamcardexchange link"] = LSteamcardexchangeLink
			df["Steam store link"] = LSteamStoreLink
			df["SI"] = list(']' * len(LAppID))
		finally:
			df.to_excel('logs/excel/logR.xlsx', index=False)
			df.to_csv('logs/css-(backup)/logR.csv', index=False)




		t = time.localtime()

		# os.rename('logs/excel/log.xlsx',
		#           (('logs/excel/log-'+str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'.xlsx').replace(":", ".")).replace(
		# 	          " ", "_"))
		#
		# os.rename('logs/css-(backup)/log.csv', (
		# 	('logs/css-(backup)/log-'+str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'.csv').replace(":", ".")).replace(" ",
		#                                                                                                             "_"))
Backup().Del_Prev_Files()
Backup().create_dataframe_and_save()
Backup().convert_data_sql()
