from bs4 import BeautifulSoup
import pandas as pd
import requests
from lxml import etree
from numpy import argmin

df = pd.read_excel('./logs/excel/log.xlsx')
LFullAppidLinkPLUS = df["Full appid link"]
List_Prices_WOtext = []
amount = 0
for linkappid in LFullAppidLinkPLUS:
    source = requests.get(linkappid)
    #page = linkappid.split("-")[-1]
    soup = BeautifulSoup(source.text, "html.parser")
    dom = etree.HTML(str(soup))
    NumberOfCards = int(dom.xpath('//*[@id="content-area"]/div[2]/div[2]/div[3]/table/tr/th[1]/text()')[amount])
    print(NumberOfCards)

    current_container = 2
    current_card = 1
    for i in range(int(NumberOfCards)):
        card_price = str(dom.xpath('//*[@id="content-area"]/div[2]/div[4]/div[' + str(current_container) + ']/div[' + str(current_card) + ']/div/a/text()')[amount])
        if current_card % 6 == 0:  # Onda si es multiplo de 6
            current_container += 1
            current_card = 1
        else:
            current_card += 1
        List_Prices_WOtext.append(float(card_price.replace("Price: $", "")))
        print(List_Prices_WOtext)
    amount += 1

    MinIndex = argmin(List_Prices_WOtext)
    print(MinIndex)
    print('##############')
    print('##############')




    # filename = 'card-%s.html' % page
    # with open(filename, 'w+') as f:
    #     f.write(soup.prettify())


