"""============================================================================
Programa para facilitar el formateo de los subtitulos para los videos a partir
de el archivo transcript que da SAP. Versión 4
Fecha creación: 27.01.2015 John Jairo Pachon H.
El formato del archivo srt mas sencillo es algo así:
1
00:00:10,500 --> 00:00:13,000
Elephant's Dream

2
00:00:15,000 --> 00:00:18,000
At the left we can see...

--------------------------------------------------------------
Se pueden colocar en determinada posicion, estilo, etc. Ejemplo:
1
00:00:10,500 --> 00:00:13,000  X1:63 X2:223 Y1:43 Y2:58
<i>Elephant's Dream</i>

2
00:00:15,000 --> 00:00:18,000  X1:53 X2:303 Y1:438 Y2:453
<font color="cyan">At the left we can see...</font>
-----------------------------------------------

También hay otro "lenguaje" WebVTT

-------------------------------------------------
SAP me entrega el script así:
00:00:10 Hi and welcome to Week 1, Learning unit 3, RDS Consumption
and Services. In this learning unit we'd like to show you
00:00:18 where you can find, browse, download and how to navigate
the packaged SAP rapid
deployment solution content.
...
...

El ultimo comentario queda mal pues comienza y termina en el mismo momento
al no haber nada despues del ultimo renglon
En la versión 4 se puede adelantar o retrasar la sincronizacion general
para corregir problemas de tiempos mal sincronizados
============================================================================"""

import os #Para poder mostrar la ruta al archivo
import re #Para expresiones regulares
import function_utilities#Funciones creadas por mi
from datetime import datetime, date, time, timedelta


#Nombre archivo por defecto a procesar
default_file = "w2u5.txt"
#Sin retardo sincronizacion por defecto
default_sync_time = 0

k_expresion = '\d\d[:]\d\d[:]\d\d'#RegEx para identificar hora con minutos y segundos Ej 03:34:10

sync_time = float(input("Tiempo Sincronización:"))
#Sin retardo por defecto
if not sync_time:
    sync_time = float(default_sync_time)

filein = input("Nombre archivo origen:  %s"%default_file )
#Archivo origen que contiene el timing de los videos que se va a convertir en SRT
if not filein:
    filein = default_file

#Archivo en el que quedaran los subtitulos en formato srt
fileout = input("Nombre archivo con subtitulos corregidos: ")
fileout = fileout + ".srt"

#Abre el archivo origen en modo lectura
#f = open(filein,'r')
f = open(filein, encoding="utf8")#Toco modificar había un caracter de continuación
filedata = f.read()
f.close()

newdata = filedata
p = re.compile(k_expresion)
iterator = p.finditer(filedata)

#Se usa para almacenar en una lista todos los intervalos de tiempo
#Sirve para obtener el tiempo en el que debe terminar de verse el texto
#El cual corresponde a cuando comienza el siguiente.
p1 = re.compile(k_expresion)
iterator1 = p1.finditer(filedata)
l = list(iterator1)
tamano_lista = len(l)

i = 0 #Inicializar contador

for match in iterator:
    print(match.span())#Punto en donde se encuentra la coincidencia
    print( match.start())#Donde comienza el string que concuerda
    print( match.end())#Donde termina el string que concuerda
    cadena = match.string[match.start(): match.end()]
    partes = cadena.split(':')
    print(partes)
    t = datetime(100,1,1, int(partes[0]), int(partes[1]), int(partes[2]))#Inicia speak
    siguiente = i+1

    if siguiente < tamano_lista:
        fila = l[siguiente]
        hora2 = fila.string[fila.start(): fila.end()]
        partes1 = hora2.split(':')
        t1 = datetime(100,1,1, int(partes1[0]), int(partes1[1]), int(partes1[2]))#Inicia speak

    t = function_utilities.sincronizar(t, sync_time)#Añade o resta sync_time segundos al tiempo inicial
    t1 = function_utilities.sincronizar(t1, sync_time)#Añade o resta sync_time segundos al tiempo final

    #Se toma la parte de hh:mm:ss y se le colocan 0 ms
    ti = str(t)[11:19] + ",000"
    tf = str(t1)[11:19] + ",000"

    if i == 0:#Para el primer elemento
        reemplazar = str(i)  + '\n' + ti + " --> " + tf #+ '\n' x que ahora viene en diferente renglon
    else:
        cadena = '\n' + cadena
        reemplazar = '\n\n' + str(i)  + '\n' + ti + " --> " + tf #+ '\n'  x que ahora viene en diferente renglon

    i = i + 1

    newdata = newdata.replace(cadena, reemplazar)
    print(cadena)
    print(reemplazar)
   
mensaje =  'hay  %s  lineas de dialogo en el archivo '
print(mensaje %  i)    

##Abre el archivo en donde se almacenará el archivo de subtitulos
f2 = open(fileout,'w')
##Escribe en el archivo la información sin los caracteres que se eliminaron
f2.write(newdata)
f2.close()
##Mostrar en que lugar quedo el resultado
archivo_salida = os.getcwd() + "\\" + f2.name
print ("Archivo procesado:", archivo_salida)

##=============================================================================
