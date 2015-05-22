"""============================================================================
Archivo para almacenar algunas funciones utiles para facilitar el procesamiento
de los subtitulos.
Fecha creación: 10.02.2015 John Jairo Pachon H.
============================================================================"""
__author__ = 'John Jairo Pachon H.'

import os  # Mostrar la ruta al archivo
import re  # Expresiones regulares
from datetime import datetime, date, time, timedelta

'# RegEx para identificar hora con minutos y segundos Ej 03:34:10'
k_expresion = '\d\d[:]\d\d[:]\d\d'


"""============================================================================
Funcion para tratar de sincronizar los subtitulos con el audio cuando no estan
sincronizados, se adicionan o se restan segundos al tiempo que viene en el
archivo
============================================================================"""


def sincronizar(t, tiempo):
    if not tiempo:
        tiempo = 0
    t1 = t + timedelta(seconds=tiempo)
    return t1
    print("Sincronización %s segundos" % tiempo)



"""============================================================================
Funcion para generar un archivo de subtitulos .srt
Recibe como parametro el nombre del archivo txt a procesar y un número de
segundos a adelantar o atrasar
============================================================================"""


def generarArchivo(w, sync_time):
    filein = w + ".txt"
    f = open(filein, 'r')
#    f = open(filein, encoding="utf8")#Toco modificar había un caracter de continuación raro
    filedata1 = f.read()
    f.close()

    '#Archivo en el que quedaran los subtitulos en formato srt'
    fileout = w + ".srt"
    newdata = filedata1
    p = re.compile(k_expresion)
    iterator = p.finditer(filedata1)

    """Se usa para almacenar en una lista todos los intervalos de tiempo
    Sirve para obtener el tiempo en el que debe terminar de verse el texto
    El cual corresponde a cuando comienza el siguiente."""
    p1 = re.compile(k_expresion)
    iterator1 = p1.finditer(filedata1)
    l = list(iterator1)
    tamano_lista = len(l)

    i = 0  # Inicializar contador

    for match in iterator:
        """print(match.span())#Punto en donde se encuentra la coincidencia
        print( match.start())#Donde comienza el string que concuerda
        print( match.end())#Donde termina el string que concuerda"""
        cadena = match.string[match.start(): match.end()]
        partes = cadena.split(':')
        '# print(partes)'
        t = datetime(100, 1, 1, int(partes[0]), int(partes[1]), int(partes[2]))  # Inicia speak
        siguiente = i+1

        if siguiente < tamano_lista:
            fila = l[siguiente]
            hora2 = fila.string[fila.start(): fila.end()]
            partes1 = hora2.split(':')
            t1 = datetime(100, 1, 1, int(partes1[0]), int(partes1[1]), int(partes1[2]))  # Inicia speak

        t = sincronizar(t, sync_time)  # Añade o resta sync_time segundos al tiempo inicial
        t1 = sincronizar(t1, sync_time)  # Añade o resta sync_time segundos al tiempo final

        '# Se toma la parte de hh:mm:ss y se le colocan 0 ms'
        ti = str(t)[11:19] + ",000"
        tf = str(t1)[11:19] + ",000"


        fin = '\n'  # Cuando hora y texto estan en mismo renglon
        '#fin = ''    # Cuando hora y texto vienen en diferente renglon'

        if i == 0:  # Para el primer elemento
            reemplazar = str(i) + '\n' + ti + " --> " + tf + fin
        else:  # Del segundo elemento en adelante
            cadena = '\n' + cadena
            reemplazar = '\n\n' + str(i) + '\n' + ti + " --> " + tf + fin

        i += 1

        newdata = newdata.replace(cadena, reemplazar)


    mensaje ='hay  %s  lineas de dialogo en el archivo '
    print(mensaje % i)

    '# Abre el archivo en donde se almacenará el archivo de subtitulos'
    f2 = open(fileout, 'w')
    '# Escribe en el archivo la información sin los caracteres que se eliminaron'
    f2.write(newdata)
    f2.close()
    '# Mostrar en que lugar quedo el resultado'
    archivo_salida = os.getcwd() + "\\" + f2.name
    print("Archivo procesado:", archivo_salida)
    '#os.remove(filein)#Borrar el archivo txt una vez fue leido'
