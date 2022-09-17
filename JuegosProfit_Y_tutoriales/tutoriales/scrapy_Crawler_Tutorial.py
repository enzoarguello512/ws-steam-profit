# Primero para trabajar con scrapy vamos a tener que importar el modulo

# Despues el primer paso es crear una arana (spider) que es tipo una variable de scrap , osea , tendriamos que crear
# una por cada 'pagina' que varie mucho el url , tipo la pestana 1 ,2 ,3 ,4 de una pagina no son problema , pero si ,
# si ponele , que la pagina cambia el url de http://www.google.com a http://www.googleWiki.blog.com , por ejemplo ,
# cambios asi son mas dificiles de manejar y creo que con una sola spider no nos va a bastar

# Para crear una spider tenemos que poner lo siguiente:







# scrapy startproject scrdata
import scrapy


class NombreCualquiera(scrapy.Spider):
    name = "NombreCualquiera"  # Identificador necesario para saber mas en especifico los spiders
    start_urls = [  # Y aca 'seria como una lista pero si queremos podemos poner una sola url , y ir modificandola ,
        # no hace falta ir poniendo todas las paginas que tenga la pagina , podemos ir cambiando la url con un 'for'
        # o un format capas
        "https://blog.scrapinghub.com/page/1/"
        "https://blog.scrapinghub.com/page/2/"
    ]

    def parse(self, response):  # Despues necesitamos un metodo de respuesta , respuesta seria el (sourcecode)
        # que devuelve la lista con los links de arriba , osea nos devuelve todo el .html creo

        page = response.url.split('/')[-1]  # Esto por si queres hacer varias paginas de la misma pagina , nose si me
        # explico , el '-1' esta para arrancar desde el ultimo item de la lista , porque con split estamos
        # transformando el string a una lista

        filename = 'PruebaDeSpider.html'  # aca creamos un archivo cualquiera , osea esto se podria optimizar y
        # directamente crearlo con el open , pero si vamos a estar cambiando de pagina por ejemplo nos va a servir
        # con el ejemplo siguiente

        # Ejemplo:
        filename = 'PruebaDeSpider/%s.html' % page

        # Para guardar la info de nuestra variable en un archivo fisico si que podemos ver con un excel o un editor de texto comun
        with open(filename, 'wb') as f:
            f.write(response.body)


# PARA EXTRAER ELEMENTOS CONCRETOS:
response.css  # .css siendo el metodo, puede ser .xpath ,etc, o demas , response es el html que nos devuelve el url en respuesta

response.css(
    'tittle').get()  # ahi pusimos el elemento que queremos , y con el get lo estariamos extrallendo , pero nada mas el primero
response.css(
    'h3::text').get()  # Los dos puntos (:) es como el punto de Bs4 o Selenium , es para buscar mas en especifico
response.css('h3::text')[
    1].get()  # Con el [1] representamos que elemento queremos , porque el .get devuelve uno solo (creo que nada mas el primero , pero bueno) , eso si es que no queremos usar el .getall()

response.css(
    'h3::text').getall()  # Para sacar todos los que matchen con los parametros que les pasamos , en este caso 'h3' y el texto de ese 'h3' , es una opcion para no tener que usar los metodos anteriores

response.css('.post-header').getall()  # Ejemplo para sacar todas las clases que se llamen '.post-header'
response.css(
    '.post-header a').getall()  # Sacariamos todos los links , acordate que las 'a' en html stands for anchor (ancla) , y en las anclas estan todos los link , y un texto que es el que te redirecciona
response.css('.post-header a::text').getall()  # Si es que queremos todos los textos de los links

post = response.css('div.post-item')[0]  # Post-item es una clase
print(post)
title = post.css('.post-header h2 a::text')[0].get()  # Nos daria el texto de la ancla (a) anchor , aka el 'href' ,

# Regular expressions:
response.css('p::text').re(r'scraping')  # Esto por si trabajamos con expresiones regulares , nos daria todas las
# palabras con exactamente iguales , esto te puede ser util si las queres contar , ni idea
response.css('p::text').re(r's\w+')  # Nos daria todas las palabras que empiezen con la letra s (dentro de la pagina)
response.css('p::text').re(r'(\w+) you (\w+)')  # Nos daria una lista (creo) con las oraciones(va en realidad te
# da las palabras separadas dentro de la lista) que tengan la palabra 'you' en el medio

# Usando Xpath:
# Haciendo lo de arriba nada mas que con .xpath
response.xpath('//h3')  # para sacar todos los headings 3 , aka h3

# Podemos usar el extract o el get() que creo que hacen lo mismo
response.xpath('//h3/text()').extract()  # Para sacar el texto de esos h3
response.xpath('//h3/text()').getall()  # Lo mismo nada mas que otro metodo

response.xpath(
    '//*[@id="hs_cos_wrapper_module_1523032069834331"]/div/div/div/div/div[1]/div[1]/div[2]/h2/a').extract()  # Usando el xpath copiado tal cual
response.xpath(
    '//*[@id="hs_cos_wrapper_module_1523032069834331"]/div/div/div/div/div[1]/div[1]/div[2]/h2/a/text()').extract()  # Sacando el texto del mismo xpath

########Ejemplos:
post = response.css('div.post-item')[0]
print(post)

title = post.css('.post-header h2 a::text')[0].get()
print(title)

date = post.css('.post-header a::text')[1].get()
print(date)

author = post.css('.post-header a::text')[2].get()
print(author)

# BUCLES:
for post in response.css('div.post-item'):
    title = post.css('.post-header h2 a::text')[0].get()
    date = post.css('.post-header a::text')[1].get()
    author = post.css('.post-header a::text')[2].get()
    print(dict(title = title, date = date, author = author))


#VERCION MAS EFICIENTE PARA MANEJO DE VARIAS PAGINAS:
class NombreCualquiera(scrapy.Spider):
    name = "NombreCualquiera"
    start_urls = [
        "https://blog.scrapinghub.com/"
    ]

    def parse(self, response):
        for post in response.css('div.post-item'):
            yield {
                'title': post.css('.post-header h2 a::text')[0].get(),  #Acordate las comas xD
                'date':post.css('.post-header h2 a::text')[1].get(),
                'author':post.css('.post-header h2 a::text')[2].get()
            }
            next_page = response.css('a.next-posts-link::attr(href)').get()     #Basicamente buscamos una ancla/anchor/(a) que tenga la clase 'next-posts' y de esa queremos sacar el atributo 'href'
            if next_page is not None:   #Esto para comprobar si existe el boton de 'next page' , si no existe va a devolver 'None' y con esto nos ahorrariamos el error
                next_page = response.urljoin(next_page) #Basicamente urljoin lo que hace es 'scrapear' la esa pagina tambien
                yield scrapy.Request(next_page, callback = self.parse)



>>% scrapy crawl NombreCualquiera -o posts.json
# '-o' stands for output , osea , salida , onda , por si queremos guardar los contenidos del "scrapeo" en un archivo fisico , estilo .json , .csv , etc



#COMANDOS UTILES PARA SCRAPEAR:
#Estando en el navegador , para verificar si usa JS(javascript) para cargar los contenidos, tenes que hacer lo siguiente:
#*Apretas 'F12' o al menos en Chrome , despues vas al apartado 'Network' , y clickeas las opcion para 'desahabilitar el cache'
#*Estando ahi aprestas estas teclas en combo , 'Ctrl' + 'Shift' + 'P'
#*Y escribis 'dis' , y buscas uno que diga 'Disable javascript' y recargas la pagina y miras

#*Para volver a habilitar el JS , destickeas el casillero del cache que activamos previamente y despues volves a apretar las mismas teclas del paso 2
#*Y una vez ahi buscas 'enable javascript' o algo asi y la clickeas y listo

# PARA CORRER EL PROGRAMA SIN TENER QUE USAR LA TERMINAL:
import scrapy
from scrapy.crawler import CrawlerProcess


class asd():
    pass


process = CrawlerProcess()
process.crawl(asd)  # 'asd' representa el nombre de nuestra clase que contenga el spider
process.start()

#PARA VER QUE ES LO QUE VE SCRAPY:
# scrapy fetch --nolog https://example.com > response.html
#Tenes que reemplazar el url nada mas y te tendria que crear un archivo .html en la carpeta en la que estas trabajando con lo que ve scrapy