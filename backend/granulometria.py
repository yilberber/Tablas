import pandas as pd
import matplotlib.pyplot as plt #importar la librería matplotlib
from scipy.interpolate import interp1d #Importar la librería scipy para poder interpolar


malla=[ # Para las mallas
    "11/2", #Tamiz 11/2"
    "1", #Tamiz 1"
    "3/4", #Tamiz 3/4"
    "3/8", #Tamiz 3/8"
    "No 4", #Tamiz N°4
    "No 10", #Tamiz N°10
    "No 20", #Tamiz N°20
    "No 40", #Tamiz N°40
    "No 60", #Tamiz N°60
    "No 100", #Tamiz N°100
    "No 200", #Tamiz N°200
    "fondo" #Fondo
]

"""Se crea una lista con el nombre de aberturas donde se ingresa la abertura de cada tamiz"""
abertura=[
    37.5, # Para Tamiz 11/2"
    25, #Para Tamiz 1"
    19, #Para Tamiz 3/4"
    9.5, #Para Tamiz 3/8"
    4.75, #Para Tamiz N°4
    2,  #Para Tamiz N°10
    0.85, #Para Tamiz N°20
    0.425, #Para Tamiz N°40
    0.250, #Para Tamiz N°60
    0.15, #Para Tamiz N°100
    0.075, #Para Tamiz N°200
    0 #Fondo
]

retenido=[
    0, # Para Tamiz 11/2"
    0, #Para Tamiz 1"
    130, #Para Tamiz 3/4"
    150, #Para Tamiz 3/8"
    120, #Para Tamiz N°4
    60, #Para Tamiz N°10
    100, #Para Tamiz N°20
    100, #Para Tamiz N°40
    205, #Para Tamiz N°60
    50, #Para Tamiz N°100
    200, #Para Tamiz N°200
    35 #Fondo
]

granulometria= pd.DataFrame({   #Se crea el dataFrame granulometría
    "Malla": malla, #columana malla
    "Abertura": abertura, #columna abertura
    "Retenido": retenido #columna retenido
}) #Se cierra el dataFrame

granulometria["Retenido_acum"]= granulometria["Retenido"].cumsum() #se crea una columna para retenido acummulado y se aplica cumsum a la columna retenido para hallar su acumulado
granulometria["Pasa"]= granulometria["Retenido"].sum()-granulometria["Retenido_acum"] #Se crea la columna Pasa y se realiza la resta del total de la muestra menos el retenido acumulado en cada fila
granulometria["Por_Pasa"]= round(granulometria["Pasa"]*100/granulometria["Retenido"].sum(),2) #Se crea la columna % pasa y se realiza la operació entre la columna pasa por 100 dividido en el total de la muetra


