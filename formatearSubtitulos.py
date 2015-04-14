"""============================================================================
Programa para facilitar el formateo de los subtitulos para los videos a partir
del archivo transcript que suministra SAP. Versión 8
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
--------------------------------------------------------------

También hay otro "lenguaje" WebVTT que no usamos por el momento aqui.

--------------------------------------------------------------

SAP me entrega el script así:

WEEK 2, UNIT 1
00:00:10 Hi and welcome to Week 1, Learning unit 3, RDS Consumption
and Services. In this learning unit we'd like to show you
00:00:18 where you can find, browse, download and how to navigate
the packaged SAP rapid
deployment solution content.
...
...

O a veces así
WEEK 2, UNIT 1
00:00:09
Welcome to week 2 of the SAP HANA Cloud Platform course.
00:00:13
In the last week, we looked into how to deploy our first application into the cloud with the HANA Cloud Platform.
00:00:21
In this week, we will be looking into the persistence service and how to use it.
...
...
--------------------------------------------------------------

El ultimo comentario queda mal pues comienza y termina en el mismo momento
al no haber nada después del ultimo renglon
En la versión 4 se adiciono funcionalidad para adelantar o retrasar la sincronizacion general
para corregir problemas de tiempos mal sincronizados

Esta versión debe permitir separar el archivo original en las unidades correspondientes
El archivo original no puede ser tan grande pues esto se procesa en memoria

Se crea una función (generarArchivo) para el procesamiento del archivo, completar tiempo

A veces algunos caraceres especiales generan mensaje de error
Desde el notepad++ se debe guardar el archivo como utf sin BOM
Menu encoding - Encode in utf 8 without BOM

En versión 7 podemos seleccionar el archivo fuente con un cuadro de dialogo
dialogo.

En la versión 8 se crea una carpeta files en donde se almacenaran los archivos a procesar,
para que queden separados de el codigo fuente.

Versión 9 eliminar número de pagina desde el principio
en algunos archivos despues de copiar del pdf a texto aparece así:
00:07:01 His focus is on how to help customers to move to the cloud edition in a simple way, how to
help to avoid unnecessary pre-investments in hardware and services,
3
00:07:12 and of course, how to get a fast proof of the unbelievable advantages of a simplified and very
fast Business Suite with SAP S/4HANA,
00:07:24 and finally, how to give customers the choice to drive their own landscape or to use the SAP
cloud.
4
00:08:45 And, also a big note, there soon will be a deep-dive course on S/4HANA here on openSAP.
00:08:55 So now, let’s start the course with Bernd Leukert.
============================================================================"""

import os #Para poder mostrar la ruta al archivo
import re #Para expresiones regulares
import function_utilities#Funciones creadas por mi
from datetime import datetime, date, time, timedelta
from tkinter import filedialog


#Directorio donde se almacenan archivos a procesar
carpeta = 'files'

#Nombre archivo por defecto a procesar donde estan todos los subtitulos
#de la semana
default_file = "todo_hana_week2.txt"

#Sin retardo sincronizacion por defecto
default_sync_time = 0

#Inicializar la lista de los archivos a procesar
archivos = []

#RegEx para identificar número de página
#{1,2} significa que puede ser uno o dos números
k_num_pag = '\n\d{1,2}\n'

#A regex to match the pattern that separate units(videos)
#Cuando el curso se divide en semanas y estas en unidades
k_expr_separador = '\n(?i)WEEK [\d], (?i)UNIT [\d]'  #(?i)Implica que puede ser mayúsculas o minusculas

#Cuando el curso solo tiene unidades y no hay semanas
#k_expr_separador = '\n(?i)UNIT [\d]'  #(?i)Implica que puede ser mayúsculas o minusculas


#Separador estandar para facilitar posterior division
k_separador = "||||||||||"

####################################Inicio Entradas de datos al programa
#Mostrar cuadro para seleccionar archivo tipo txt o xml
filein = filedialog.askopenfilename(filetypes = (("Text files", "*.txt"),("Xml files", "*.xml") ))

sync_time = float(input("Tiempo Sincronización:"))
#Sin retardo por defecto
if not sync_time:
    sync_time = float(default_sync_time)

#Archivo origen que contiene el timing de los videos que se va a convertir en SRT
if not filein:
    filein = default_file
print("Archivo procesar:", filein)
####################################Fin Entradas de datos al programa


#Abre el archivo con todos los scripts de la semana
f = open(filein, encoding="utf8")#Toco modificar había un caracter de continuación raro
filedata = f.read()
f.close()

newdata1 = filedata


#Versión 9.1
# #Para eliminar los números de pagina de newdata1
p2 = re.compile(k_num_pag)
iterator2 = p2.finditer(newdata1)
reemplazar = '\n'
for match1 in iterator2:
    cadena2 = match1.string[match1.start(): match1.end()]
    newdata1 = newdata1.replace(cadena2, reemplazar)


#Obtener los nombres de archivos a usar
pf = re.compile(k_expr_separador)
iteratorfile = pf.finditer(filedata)
for match in iteratorfile:
    #print(match.span())#Punto en donde se encuentra la coincidencia
    #print( match.start())#Donde comienza el string que concuerda
    #print( match.end())#Donde termina el string que concuerda
    cadena = match.string[match.start(): match.end()]
    newdata1 = newdata1.replace(cadena, k_separador)
    cadena = cadena.replace(",", "_")
    cadena = cadena.replace(" ", "")
    cadena = cadena.replace("\n", "")#Quitar salto de linea del nombre del archivo.
    cadena = carpeta + os.path.sep + cadena #Para que el archivo quede en una subcarpeta "carpeta"
    archivos.append(cadena)


#Ahora si dividimos el archivo y generamos tantos archivos txt como sea necesario
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
for i, part in enumerate(newdata1.split(k_separador)):
    if not part.strip():continue # make sure its not empty
    nombre_archivo = archivos[i-1]
    na = nombre_archivo + ".txt"
    file_tmp = open(na,'w')
    #Escribe en el archivo la información separada por unidades(week_unit1.txt, week_unit2.txt ...)
    file_tmp.write(part)
    file_tmp.close()
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



#Ejecutar esta parte tantas veces como archivos existan
##=============================================================================
#Loop sobre los nombres de los archivos a generar
for w in archivos:
    function_utilities.generarArchivo(w, sync_time)

##=============================================================================
