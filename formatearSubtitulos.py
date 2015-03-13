"""============================================================================
Programa para facilitar el formateo de los subtitulos para los videos a partir
de el archivo transcript que da SAP
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
00:00:10 Hi and welcome to Week 1, Learning unit 3, RDS Consumption and Services. In this learning
unit we'd like to show you
00:00:18 where you can find, browse, download and how to navigate the packaged SAP rapid
deployment solution content.

Necesito colocar salto de línea al final de los caracteres de tiempo

============================================================================"""

import os #Para poder mostrar la ruta al archivo
import re #Para expresiones regulares
import bdb #Debug

#Nombre archivo por defecto
default = "Week1unit3.txt"
k_expresion = '\d\d[:]\d\d[:]\d\d'

#Archivo origen que contiene el timing de los videos que se va a convertir en SRT
filein = input("Nombre archivo origen:  %s"%default )
if not filein:
    filein = default

#Archivo en el que quedaran los subtitulos en formato srt
fileout = input("Nombre archivo subtitulos: ")
fileout = fileout + ".srt"

#Abre el archivo origen en modo lectura
f = open(filein,'r')
filedata = f.read()
f.close()

newdata = filedata

p = re.compile(k_expresion) 
i = 0
iterator = p.finditer(filedata)
for match in iterator:
    i = i + 1
    print(match.span())#Punto en donde se encuentra la coincidencia
    print( match.start())#Donde comienza el string que concuerda
    print( match.end())#Donde termina el string que concuerda
    cadena = match.string[match.start(): match.end()]
    cadena1 = '\n' + str(i) + '\n' + cadena + ",000 --> " + cadena + ",999" + '\n'
    newdata = newdata.replace(cadena, cadena1)
    print(cadena)
    print(cadena1)
   
mensaje =  'hay  %s  lineas'   
print(mensaje %  i)    

print(newdata)


##Abre el archivo en donde se almacenará el archivo de subtitulos
f2 = open(fileout,'w')
##Escribe en el archivo la información sin los caracteres que se eliminaron
f2.write(newdata)
f2.close()
##Mostrar en que lugar quedo el resultado
archivo_salida = os.getcwd() + "\\" + f2.name
print ("Archivo procesado:", archivo_salida)



"""



newdata = filedata.replace('\t','') ##Elimina el caracter tabulador. 
newdata = filedata.replace('\n','') ##Elimina el caracter de salto de linea.




##=============================================================================
"""
