import mysql.connector
import pandas as pd
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

#--------------------Base de datos------------------------#





# Function for decimals
def truncate(n, decimals=0):
	multiplier = 10 ** decimals
	return int(n * multiplier) / multiplier


def convert_price(list_to_convert, list_for_results):
	Amt = 1
	for string in list_to_convert:
		# Agaraamos cada precio y lo convertimos a solamente numeros y comas , asi despues si queremos lo podemos pasar a entero o manipular mas facil
		Amt += 1
		word = []
		for letter in string:
			if letter == "," or letter == ".":
				word.append(".")
			elif letter.isdigit():
				word.append(letter)
			else:
				continue
		try:
			list_for_results.append(float("".join(word)))
		except ValueError:
			list_for_results.append(float(999))


def css_color(item):
	if str(item) == 'rgba(21, 102, 183, 1)':  # onda si es azul
		LNewHighestDiscount.append("Product has not been this cheap before")
	elif str(item) == 'rgba(139, 195, 74, 1)':  # onda si es azul
		LNewHighestDiscount.append("Product is priced on par with lowest recorded price")
	else:
		LNewHighestDiscount.append("No")


def invalid_data():
	LNewHighestDiscount.append('-')
	LOfferType.append('-')
	LDaysSinceTheOfferStarted.append('-')
	LDaysForTheOfferToEnd.append('-')


def Remove_unsoported_characters(string):
	list_letters = []
	chars = set('\',:;!"#&/$()=?¿.<>-_[]{}¡+\\@%')
	for letter in string:
		if letter.isalnum():
			list_letters.append(letter)
		elif letter.isspace():
			list_letters.append(letter)
		elif any((c in chars) for c in string):
			list_letters.append(letter)
		else:
			pass
	new_string = "".join(list_letters)
	return new_string


def LimpiaConsola(): os.system('cls')


########################################################################################################################

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
		"Creamos el archivo log si es que no existe"
		try:
			print("reading log.xlsx")
			df = pd.read_excel('logs/excel/log.xlsx')
			del df
		except:
			print("file not found('log.xlsx'), creating it now")
			df = pd.DataFrame({
				"AppID": [],
				"Name": [],
				"Game price (ARS)": [],
				"Discount": [],
				"Cheapest card price (USD)": [],
				"Cheapest card price (ARS)": [],
				"Number of cards in total": [],
				"Obtainable cards": [],
				"Steam commission (ARS)": [],
				"Value of the cards obtainable without the steam commission (ARS)": [],
				"Approximate minimum profit (counting commission and value of the game) (ARS)": [],
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
			df.to_excel('logs/excel/log.xlsx', index=False)
			del df

		##---------------------------------------

		try:
			print("reading log.csv")
			df = pd.read_csv('logs/css-(backup)/log.csv')
			del df
		except:
			print("file not found('log.csv'), creating it now")
			df = pd.DataFrame({
				"AppID": [],
				"Name": [],
				"Game price (ARS)": [],
				"Discount": [],
				"Cheapest card price (USD)": [],
				"Cheapest card price (ARS)": [],
				"Number of cards in total": [],
				"Obtainable cards": [],
				"Steam commission (ARS)": [],
				"Value of the cards obtainable without the steam commission (ARS)": [],
				"Approximate minimum profit (counting commission and value of the game) (ARS)": [],
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
			df.to_csv('logs/css-(backup)/log.csv', index=False)
			del df

	def Del_Prev_Files(self):
		try:
			os.remove('logs/excel/log.xlsx')
			print('Previo log.xlsx borrado exitosamente')
		except:
			print('No se pudo borrar el anterior log.xlsx')
			print('Continuando')
		try:
			os.remove('logs/css-(backup)/log.csv')
			print('Previo log.csv borrado exitosamente')
		except:
			print('No se pudo borrar el anterior log.csv')
			print('Continuando')

	def creating_table_PreSaveData(self, itemsToDuplicate):
		empty_list = [']'] * itemsToDuplicate

		try:
			df = pd.read_excel('logs/excel/log.xlsx')
			df["SI"] = pd.Series(empty_list)
		finally:
			# Problema es que sobreescribe el anterior
			df.to_excel('logs/excel/log.xlsx', index=False)

		try:
			df = pd.read_csv('logs/css-(backup)/log.csv')
			df["SI"] = pd.Series(empty_list)
		finally:
			# Problema es que sobreescribe el anterior
			df.to_csv('logs/css-(backup)/log.csv', index=False)
		del df

	def Page1_SaveData(self):
		"Guardamos la info en un archivo .excel , gracias al modulo pandas , o al menos la primera parte de steamdb"

		try:
			df = pd.read_excel('logs/excel/log.xlsx')

			df["AppID"] = LAppID
			df["Name"] = LName
			df["Game price (ARS)"] = LGamePrice
			df["Discount"] = LDiscount
			df["Steamcardexchange link"] = LSteamcardexchangeLink
			df["Steam store link"] = LSteamStoreLink
			df["SI"] = list(']' * len(LAppID))
		finally:
			# Problema es que sobreescribe el anterior
			df.to_excel('logs/excel/log.xlsx', index=False)

		##---------------------------------------
		try:
			df = pd.read_csv('logs/css-(backup)/log.csv')

			df["AppID"] = LAppID
			df["Name"] = LName
			df["Game price (ARS)"] = LGamePrice
			df["Discount"] = LDiscount
			df["Steamcardexchange link"] = LSteamcardexchangeLink
			df["Steam store link"] = LSteamStoreLink
			df["SI"] = list(']' * len(LAppID))
		finally:
			# Problema es que sobreescribe el anterior
			df.to_csv('logs/css-(backup)/log.csv', index=False)

		del df

		##---------------------------------------

	def Page2_SaveData(self):
		"Para guardar los precios de steamdb"
		try:
			df = pd.read_excel('logs/excel/log.xlsx')
			df["Offer type"] = LOfferType
			df["New highest discount?"] = LNewHighestDiscount
			df["Days since the offer started"] = LDaysSinceTheOfferStarted
			df["Days for the offer to end"] = LDaysForTheOfferToEnd
		finally:
			df.to_excel('logs/excel/log.xlsx', index=False)

		##---------------------------------------

		try:
			df = pd.read_csv('logs/css-(backup)/log.csv')
			df["Offer type"] = LOfferType
			df["New highest discount?"] = LNewHighestDiscount
			df["Days since the offer started"] = LDaysSinceTheOfferStarted
			df["Days for the offer to end"] = LDaysForTheOfferToEnd
		finally:
			df.to_csv('logs/css-(backup)/log.csv', index=False)
		##---------------------------------------

	def Post_SaveData(self):
		"Guardamos la info que sale de LoadContents() por separado , por si queremos hacer 2 pasadas separadas"
		try:
			df = pd.read_excel('logs/excel/log.xlsx')
			df["Cheapest card price (USD)"] = LCheapestCardPrice
			df["Cheapest card price (ARS)"] = LPreciosArs
			df["Number of cards in total"] = LNumberOfCardsInTotal
			df["Obtainable cards"] = LObtainableCards
			df["Steam commission (ARS)"] = LSteamCommission
			df[
				"Value of the cards obtainable without the steam commission (ARS)"] = LValueOfTheCardsObtainableWithoutTheSteamCommission
			df[
				"Approximate minimum profit (counting commission and value of the game) (ARS)"] = LApproximateMinimumProfit
			df["Price multiplied by number of accounts (ARS)"] = LPriceMultipliedByNumberOfAccounts
		# df ["Paid out (ARS)"] = LPaidOut
		finally:
			# Problema es que sobreescribe el anterior
			df.to_excel('logs/excel/log.xlsx', index=False)

		##---------------------------------------

		try:
			df = pd.read_csv('logs/css-(backup)/log.csv')
			df["Cheapest card price (USD)"] = LCheapestCardPrice
			df["Cheapest card price (ARS)"] = LPreciosArs
			df["Number of cards in total"] = LNumberOfCardsInTotal
			df["Obtainable cards"] = LObtainableCards
			df["Steam commission (ARS)"] = LSteamCommission
			df[
				"Value of the cards obtainable without the steam commission (ARS)"] = LValueOfTheCardsObtainableWithoutTheSteamCommission
			df[
				"Approximate minimum profit (counting commission and value of the game) (ARS)"] = LApproximateMinimumProfit
			df["Price multiplied by number of accounts (ARS)"] = LPriceMultipliedByNumberOfAccounts
		# df ["Paid out (ARS)"] = LPaidOut
		finally:
			# Problema es que sobreescribe el anterior
			df.to_csv('logs/css-(backup)/log.csv', index=False)

		t = time.localtime()

		os.rename('logs/excel/log.xlsx',
		          (('logs/excel/log-'+str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'.xlsx').replace(":", ".")).replace(
			          " ", "_"))

		os.rename('logs/css-(backup)/log.csv', (
			('logs/css-(backup)/log-'+str(time.strftime("%Y-%m-%d %H:%M:%S", t))+'.csv').replace(":", ".")).replace(" ",
		                                                                                                            "_"))

