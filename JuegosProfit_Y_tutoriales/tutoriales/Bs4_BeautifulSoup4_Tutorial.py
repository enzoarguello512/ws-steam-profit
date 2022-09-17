from bs4 import BeautifulSoup
#pip install beautifulsoup4
#pip install lxml
#pip install html5lib
#pip install requests
import requests

#------Desde un archivo

with open("pato") as html_file:
    soup = BeautifulSoup(html_file, "lxml") # Esto por si lo tenemos al archivo html en fisico , onda en la misma
    # carpeta ponele , el segundo coso es como el lector
print(soup.prettify ())     # Si no usamos el prettify nos va a devolver el codigo base si , si , pero va a estar sin
# identaciones onda es como si lo pusieras con el word para que todas las palabras se peguen a un lado o el otro

match = soup.title.text     # Podemos decirle al programa que buscar , eso iria a buscar el primer elemento
# arrancando desde arriba , y depues con los otros parametros que le pasemos podemos buscar algo mas en especifico ,
# como por ejemplo en este caso buscamos el texto del titulo y lo guardamos en esa variable

article = soup.find('div')   # El metodo find() nos va a permitir buscar (el primer item tambien) que coincidan con el
# los parmetros que le pasemos , en este caso con todos los "div" , igual a medida que le pasamos mas parametros la
# busqueda se reduce mas y mas , eso nos va a permitir encontrar un item en especifico que estemos buscando en vez de
# solamente el primero
#Ejemplo:
article = soup.find('div', class_='footer')   # Class con guion bajo porque la palabra "class" original esta
# reservada por el mismo python
headlines = article.h2.a.text    # Aca usamos nuestro 'article' asi no hace falta abrir el 'soup' de vuelta , osea ,
# asi no cargamos toda la pagina al dope y somos mas especificos
sumary = article.find('div', class_='entry-content').p.text
vid_src = article.find('iframe', class_='youtube-player')['src']    #Podemos hacer tipo un diccionario para poder sacar un atributo de esta tag en particular si queremos
vid_id = vid_src.split('/')[4]
vid_id = vid_id.split('?')[0]
yt_link = f'https//youtube.com/watch?v={vid_id}'    # la letra 'f' stands for format , osea , es lo mismo que si usaramos .format()

for article in soup.find_all('div', class_="pato"):   # Este es la misma vercion del find , pero va a devolver una
    # lista con TODOS los items que concidan
    headlines = article.h2.a.text   #Extraemos el primer item (mirando el comando solo , sin el for que tenemos arriba) que coincida con esos parametros
    print(headlines)

    summary = article.p.text        #Y aca nos ahorramos volver a llamar al archivo y llamamos a la variable de antes para seguir buscando
    print(summary)




#------Desde una web

source = requests.get("https//google.com").text  #El metodo get() de el modulo request nos va a devolver un objeto de
# respuesta (sourcecode) y usamos el .text , como para poder guardarlo como si fuera un string creo y lo almacenamos en una variable
soup = BeautifulSoup(source, "lxml")
print(soup.prettify ())



from bs4 import BeautifulSoup
import pandas as pd
import requests
from lxml import etree
from numpy import argmin

df = pd.read_excel('./logs/excel/log.xlsx')
LFullAppidLinkPLUS = df["Full appid link"]
List_Prices_WOtext = []

for linkappid in LFullAppidLinkPLUS:
    source = requests.get(linkappid)
    #page = linkappid.split("-")[-1]
    soup = BeautifulSoup(source.text, "html.parser")
    dom = etree.HTML(str(soup))
    print(soup)
    find_NOC = dom.xpath('//*[@id="content-area"]/div[2]/div[2]/div[3]/table/tr/th[1]/text()')
    NumberOfCards = int(find_NOC.split('>')[1].split('<')[0])  #Transformamos el string que nos devolvio a un valor manejable

    current_container = 2
    current_card = 1
    find_CP = list(soup.find('div', class_ = "showcase-element-container card").find_all('a', class_ = "button-blue"))
    print(find_CP)
    for price in find_CP:
        card_price = price.split('>')[1].split('<')[0]
        List_Prices_WOtext.append(float(card_price.replace("Price: $", "")))


    print(List_Prices_WOtext)
    card_price = find_CP.split('>')[1].split('<')[0]
    print(card_price)
    List_Prices_WOtext.append(float(card_price.replace("Price: $", "")))
    print(List_Prices_WOtext)


    try:
        for i in range(int(NumberOfCards)):
            card_price = soup.find('div', class_="showcase-element-container card").find('a', class_="button-blue")
            card_price = response.xpath('//*[@id="content-area"]/div[2]/div[4]/div[' + str(current_container) + ']/div[' + str(current_card) + ']/div/a/text()').get()
            if current_card % 6 == 0:  # Onda si es multiplo de 6
                current_container += 1
                current_card = 1
            else:
                current_card += 1
            List_Prices_WOtext.append(float(card_price.replace("Price: $", "")))
    except TypeError:
        pass

    MinIndex = argmin(List_Prices_WOtext)

    print('##############')
    print(NumberOfCards)
    print(List_Prices_WOtext)
    print(MinIndex)
    print('##############')




    filename = 'card-%s.html' % page
    with open(filename, 'w+') as f:
        f.write(soup.prettify())
















