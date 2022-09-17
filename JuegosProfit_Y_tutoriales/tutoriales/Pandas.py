import pandas as pd
from re import *
#import xlrd as necesario para pandas / excel

#Lectura y/o creacion

LeectorDeinfo = pd.read_csv("pandas-master/pokemon_data.csv")   #Cargamos la info de nuestro excel asi la podemos usar en python
LeectorDeinfo = pd.read_excel("pandas-master/pokemon_data.xlsx")   #Para leer archivos en columnas , osea excels comunes , los csv son excels si , pero
    # los valores estan separados por comas y queda medio feo
LeectorDeinfo = pd.read_csv("pandas-master/pokemon_data.txt", delimiter='\t')   #En este caso necesitamos poner un limitador si es que estamos usando un
    # archivo .txt porque sino se ve feo , y separado por \t creo , lo recomendable seria que lo probes para estar seguro , creo que es tipo un split comun
#-------------
LeectorDeinfo.to_excel("asd")   #Para convertir un df en un archivo real , igual hacen falta modulos





#Para conseguir primeros o ultimos items de la lista

print(LeectorDeinfo.head(3))    #Hay 2 funciones que nos pueden ser de utilidad , igual creo que hay mas pero las que salen en el video son las
    # siguientes , .head() y entre parentesis hasta que punto queremos que que explore el buscador , osea de arriba hacia el punto que le pasemos ,
    # y .tail() sigue las mismas reglas






print(LeectorDeinfo.columns)   #Para leer los "headers" osea los titulos de las columnas existentes






#Manipulacion de columnas

print(LeectorDeinfo['Name'])    #Sirve para leer todos los items que esten en la columna llamada name
print(LeectorDeinfo.Name)  #Tambien se puede usar y cumple la misma funcion que se describe arriba
print(LeectorDeinfo['Name'][0:5])   #El 0:5 expesifica de donde a donde queres que lea el programa , ahi ponele estarias leyendo solamente los primeros
    # 5 items
print(LeectorDeinfo[['Name','Type 1','HP']])    #Por si queremos sacar los items de esas 3 particulares columnas

print(LeectorDeinfo.iloc[1])    #Sirve basicamente para lo mismo que .columns , pero esto es en el sentido horizontal , osea las rows/filas , con el 1
    # estariamos sacando la primera nada mas
print(LeectorDeinfo.iloc[1:4])  #y con este otro sacariamos un rango , igual que con .columns[]
print(LeectorDeinfo.iloc[2,1])    #Si queremos un item en particular lo podemos sacar asi , poniendo por ejemplo , en el primer parametro el numero de
    # la row/fila y en el segundo en que columna estaria , acordate que es python y cuenta el "0" tambien , es tipo batalla naval





#Para iterar

for index, row in LeectorDeinfo.iterrows():     #Para iterar sobre los nombres creo? nose es mejor buscarlo en la wiki a esto, "index" y "row" son
    # nombres random , podes ponerle el que vos quieras , el primero creo que hace referencia al numero en el que se encuentran , usando las filas claro ,
    # y el segundo creo que puede ser cualquier parametro que nosotros queramos tipo , queremos que nos muestre todos los nombres y nose ponele , todos
    # los apellidos , despues de que se iguala el excel a la variable , asi no tira objetos raros
    print(index, row["Name"])


#Funciones de datos/busquedas:

print(LeectorDeinfo.loc[LeectorDeinfo['Type 1'] == "Fire"])    #Este comando .loc[] para localizar todos los elementos en la columna "Type 1" que
    # contengan la palabra "Fire"

print(LeectorDeinfo.describe())     #Nos serviria para "Ver los high level standard desviation" osea , yo creo que todas las columnas que contengan
    # unicamente enteros xDD , ahi creo que lo entendi mejor y te muestra como las caracteristicas de todos estos enteros , por ejemplo en vida te marca
    # que el maximo numero es 255 y ese numero si existe en el excel , asi que te hace un tipo mini analicis y ahi lo podes apreciar mas facil


#Manipulacion y orden de columnas:

print(LeectorDeinfo.sort_values('Name'))     #Con esto podemos ordenar nuestra columna "Name" alfabeticamente , osea de la A-Z
print(LeectorDeinfo.sort_values('Name', ascending=False))   #Y con este otro la podriamos invertir , osea de la Z-A
print(LeectorDeinfo.sort_values(['Name','Type 1'], ascending=[1,0]))   #Con esto podriamos agarrar mas de una columna y elegir el orden (ascendente
# o descendente) de c/u , acordate que 1 = True y 0 = False
LeectorDeinfo['Total'] = LeectorDeinfo['HP'] + LeectorDeinfo['Attack'] + LeectorDeinfo['Speed']       #OJITO DE NO COMBINAR STRINGS CON ENTEROS ACA ,
# QUE TIRAR ERROR .Esta es una forma de crear una nueva columna y tambien de darle valor , nuestra nueva columna total va a ser una suma de otras
# columnas ( no completas ) osea que es segun cada individuo , sino seria un quilombo jaja
print(LeectorDeinfo['Total'] =  LeectorDeinfo['Name'] + LeectorDeinfo['Type 1'] + LeectorDeinfo['Speed'])  #EJEMPLO MAL HECHO , NO SE PUEDE JUNTAR
# UN STRING CON UN ENTERO



#Borrar columnas/sobreescribir:

LeectorDeinfo = LeectorDeinfo.drop(columns = ['Total'])   #Para borrar una columna creo , es como que la sobreescribis con un valor en blanco/nulo
# igual , pero sirve




LeectorDeinfo['Total'] = LeectorDeinfo.iloc[:, 4:10].sum(axis=1)    #A ver paso a explicar detenidamente , iloc ya lo explicamos mas arriba , ahi
# le estamos diciendo que las queremos a todas porque no expesificamos ni un parametro de inicio ni uno de final , por lo tanto son todos , despues ,
# el siguiente parametro que le pasamos es que columnas queremos que agarre , en este caso desde la columna 4 (5 si contaramos bien) que seria HP la
# numero 4 , de ahi hasta la 10 (exepto , asi que no se cuenta la 10 , se cuenta la 9) y despues usamos el comando .sum creo que que es de python
# original y expesificamos con el axis , si quremos sumar los valores que estan horizontales con True/1 y si queremos que sume los verticales False/0
print(LeectorDeinfo.head(5))




#Formas de reordenar las columnas:
LeectorDeinfo = LeectorDeinfo[['Total','HP','Defense']]     #Asi seria una forma , medio tedioso pero sirve , y vas poniendo uno por uno los
# nombres de las columnas

#Otra forma de hacerlo:

columnas = list(LeectorDeinfo.columns.values)   #Sacamos los valores de las columnas (nombres) y los almacenamos en una lista
LeectorDeinfo = LeectorDeinfo[columnas[0:4] + [columnas[-1]] + columnas[4:12]]      #Fijate que columnas -1 tiene doble corchete porque lo toma
# como string sino y ahi lo transformamos en una lista con estos corchetes y asi si lo podemos sumar , sino otra forma de evitarte el doble
# corchete seria creo poniendo algo asi como [12:12] y poniendo ese solo item en cuestion



#Para guardar info:

LeectorDeinfo.to_csv('VercionModificada.csv')   #Basicamene lo que hace el comando .to_ es pasar la info que tenemos en nuestro dataframe , que
# en este caso seria nuestra variable LeectorDeInfo , y lo guarda en un archivo que elijamos a gusto en este caso lo vamos a guardar en formato
# csv (separado por comas) pero tranquilamente lo podriamos guardar en formato excel
LeectorDeinfo.to_excel('VercionModificada.xlsx', index=False)  #Con el index = 0 estariamos dejando de mostrar el numero de rows/filas , que ya
# ese te lo muestra el excel basico , pero si queres lo podes dejar
LeectorDeinfo.to_csv('VercionModificada.txt', index=False, sep='\t')    #Aca en este caso el parametro sep hace referencia a por que van a estar
# separados los valores , en este caso por una tabulacion , pero tranquilamente le podriamos decir que separe los valores con la palabra pato ,
# o con un salto de line '\n' por ejemplo


#Para sacar valores especificos tipo loc/iloc:

NuevoLectorDeinfo = LeectorDeinfo.loc[(LeectorDeinfo['Type 1'] == 'Grass') & (LeectorDeinfo['Type 2'] == 'Poison') & (LeectorDeinfo['HP'] > 70 )]   #Basicamente
    # lo que le decimos es que cree un nuevo dataframe y que busque en la columna type 1 los items que tengan tipo grass y que tambien que buscque en la
    # columna type 2 los que son de tipo poison  y que ademas tengan una vida superior a 70 , tienen que coincidir los valores porque estamos usando un and/&
# Usamos & en vez de and , usamos | (ese singo lo podemos hacer con la siguiente combinacion de teclas , alt + 1,2,4 , todo junto) y ese reemplazaria al or , en la
# wiki lo explican mejor

NuevoLectorDeinfo.to_csv('PruebaDeExcel.csv')   #Si lo tratamos de convertir a .xlsx nose porque tira error <- porque te falto un modulo nabo
#Si imprimeramos NuevoLectorDeinfo va a imprimir con el index antiguo del dataframe anterior , por lo tanto capas que este comando te va a ser util
NuevoLectorDeinfov2 = NuevoLectorDeinfo.reset_index()   #Para reiniciar el index y que vuelva a a la normalidad organizado , pero va a agregar el antiguo index como una
# columna nueva creo , y para borrar esa columna usamos el comando de abajo
NuevoLectorDeinfov2 = NuevoLectorDeinfo.reset_index(drop=True)  #Para borrar el antiguo index que todavia estaba dando vuelta
NuevoLectorDeinfo.reset_index(drop=True, inplace = True)    #Y tampoco haria falta asignar una nueva variable , con el comando inplace nos ahorramos crear la
# variable/dataframe nuevo y ademas ahorramos memoria



#Por si queremos buscar mas especificamente podemos usar el siguiente comando:

LeectorDeinfo.[LeectorDeinfo['Name'.str.contains('Mega')]  #Ahi podemos buscar en la columna Name y de los nombres que hay ahi filtrar los que tengan la palabra mega en ellos
LeectorDeinfo.[~LeectorDeinfo['Name'.str.contains('Mega')]   #Y Este es el opuesto , sacamos todos los que tengan mega , usando el singno ~ (alt gr + 4)
LeectorDeinfo.[LeectorDeinfo['Type 1'.str.contains('Fire|Grass'), regex=True]   #Con el regex creo que habilitamos el uso de expreciones regulares  , despues le decimos que
# en la columna type 1 necesitamos que tenga Fire o Grass , o sino que no muestre nada si no coincide , es importante notar que si usamos el comando asi , tengamos en cuenta
# las mayusculas en nuestra columna/fila , sino mira el comando de abajo
LeectorDeinfo.[LeectorDeinfo['Type 1'.str.contains('Fire|Grass'), flags=re.IGNORECASE, regex=True]  #Si bien no lo pude hacer andar , asi seria la forma de que no tengas que
# poner las mayusculas en los nombres como para que te los reconosca bien
LeectorDeinfo.[LeectorDeinfo['Name'.str.contains('^pi[a-z]*'), flags=re.IGNORECASE, regex=True]   #Si no te acordas de las expresiones regulares revisa la lista que te
# armaste , pero basicamente hace match a cualquier nombre que arranque con pi y puede seguir cualquier letra de la "A" a la "z" y el "*" significaba 1una o mas repeticiones
LeectorDeinfo.loc[LeectorDeinfo['Type 1'] == 'Fire', 'Type 1'] = 'FLAMER'     #Con esto podriamos cambiar el nombre/valor de uno de nuestros items almacenados en una columna ,
# pero basicamente lo que esta pasando es que localizamos nuestros items que contengan la palabra Fire , y despues de que ponemos la "," (coma) podemos especificar un
# parametro , por ejemplo en este caso , que si coincide algun valor , que , en la columna "Type 1" se reemplace su valor y se ponga un nuevo valor que seria "FLAMER"
LeectorDeinfo.loc[LeectorDeinfo['Type 1'] == 'Fire', 'Legendary'] = True    #Otro ejemplo para el renglon de arriba
LeectorDeinfo.loc[LeectorDeinfo['Total'] > 500 , ['Legendary','Generation'] = 'SuperPokemon'    #asi podriamos modificar varias columnas a la vez , nada mas necesitariamos
# pasarle una lista con los nombrre de las columnas a modificar
LeectorDeinfo.loc[LeectorDeinfo['Total'] > 500 , ['Legendary','Generation'] = ['SuperPokemon','PatoDuro']   #O tambien modificarlos individualmente




#Grupos

LeectorDeinfo.groupby(['Type 1']).mean().sort_values('Defense',ascending=False)  #el groupby agrupa todos los posibles items , osea como si fuera un diccionario , y
# despues el
    # mean , es como el describe() que te pasa estadisticas de cada grupo , en este caso te muestra el promedio de cada una de las otras columnas , tipo por ejemplo 'HP' y
    # despues nosotros le decimos que nos los ordende con el sort_values , en este caso por la defensa mas alta de los grupos del 'Type 1'

LeectorDeinfo.groupby(['Type 1']).sum() #Ahi sumamos todos los valores por grupos , igual hay mas comandos posiblemente en la wiki , tipo count creo , pero eso despues fijate vos
#Ejemplo
LeectorDeinfo.groupby(['Type 1']).count()   #Par contar , pero si lo queremos hacer mas bonito , porque al contar una sola fila ,las demas toman valores malos , osea , creo
# que no son identicos , porque estamos preguntando de una sola columna en espesifico,  para solucionarlo y que quede mas bonito , ponemos usar los comandos de abajo
#----------
LeectorDeinfo['Count'] = 1
LeectorDeinfo.groupby(['Type 1', 'Type 2']).count()['Count'] #Y asi se solucionaria , igual esto es mas que todo si tenes bases de datos muy grandes




#Cargando Grandes cantidades de info (OPTIMIZACION=):

contador = 0
for df in pd.read_csv('pandas-master/pokemon_data.csv', chunksize=5):    #Cagariamos el documento en pequeñas partecitas , a mayor el numero de chunkside , mayor el consumo ,
# con el numero 5 , nada mas cargamos 5 filas/rows cada vuelta del bucle asi podriamos trabajar con archivos muy grandes y aparte tampoco consumiria tanta memoria
    contador += 1
    print("Soy el chunk ",contador)




#Para crear un nuevo dataframe con las mismas columnas que tiene el otro , pero sin copiar los valores de las rows/filas:

new_df = pd.DataFrame(columns=LeectorDeinfo.columns)

for df in pd.read_csv('pandas-master/pokemon_data.csv', chunksize=5):
    results = LeectorDeinfo.groupby(['Type 1']).count()

    new_df = pd.concat([new_df, results])   #Asi podriamos sacar los valores que nos interesan del dataframe grandote (que no podriamos manejar por temas de ram capas) y lo
    # achicamos y guardamos en una nueva variabla mas chiquita y mas manejable en cuanto a ram , el metodo concat() lo que hace es concatenar 2 dataframes o algo asi , sino
    # miralo en la wiki pobre xD











