from datetime import date
from datetime import datetime
from koboextractor import KoboExtractor
import pandas as pd

from math import pi
import pandas as pd
from bokeh.palettes import Category20c
from bokeh.plotting import figure, show
from bokeh.transform import cumsum

import bokeh
from bokeh.io import output_file, show
from bokeh.layouts import row,column
from bokeh.plotting import figure,output_file, save, show, ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.resources import CDN
from bokeh.embed import components

from collections import OrderedDict
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


import imageio
import cv2
import urllib
import numpy as np
import requests
from io import StringIO, BytesIO
from PIL import Image



# Obtener las imagenes
def getUrlData(punto,data,tipo):
    lista_data_i = []
    lista_name = []
    j = 0
    """ for i in range (len(data)):
        if data[i][tipo] == punto:
            lista_data_i.append(data[i]['_attachments'][0]['download_url'])
            lista_name.append(data[i]['Nombre'])
            j =+ 1
            
        if j > 3 :
            break """ 

    for i in range (3):
        if data[i][tipo] == punto:
            lista_data_i.append(data[i]['_attachments'][0]['download_url'])
            lista_name.append(data[i]['Nombre'])
    
    lista_data_i.append("https://image.flaticon.com/icons/png/512/1034/1034633.png")
    lista_name.append("No hay imagen")
    lista_data_i.append("https://image.flaticon.com/icons/png/512/1034/1034633.png")
    lista_name.append("No hay imagen")
    lista_data_i.append("https://image.flaticon.com/icons/png/512/1034/1034633.png")
    lista_name.append("No hay imagen")
            
    return lista_data_i , lista_name



# Obtener datos de paises 
def getCountryData(punto,data,tipo):
    dict_data = {}
    for i in range (len(data)):
        if data[i][tipo] == punto:
            try:
                dict_data[data[i]['Pais']] = dict_data[data[i]['Pais']] + 1
            except:
                x = {data[i]['Pais'] : 1}
                dict_data.update(x)
                
    return dict_data



def getGraphicCountry(punto,x):
    
    data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'country'})
    #display(x)
    
    p = figure(x_range=data['country'].tolist(), height=350, title="Nacionalidades/Nationalities",
           toolbar_location=None, sizing_mode='scale_width')
    
    p.vbar(x=data['country'].tolist(), top=data['value'].tolist(), width=0.9)
    
    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    script , div = components(p)
    #show(p)
    
    return script , div



def getUrlDataList(punto, data, tipo):
    lista_data_i = []
    lista_name = []
    for i in range (len(data)):
        if data[i][tipo] == punto:
            lista_data_i.append(data[i]['_attachments'][0]['download_medium_url'])
            lista_name.append(data[i]['Nombre'])
    
    #display(lista_name)
    
    img_array = []
    for x, y in zip(lista_data_i, lista_name):
        
        #Asignar a variable leer_imagen, el nombre de cada imagen
        try:
            leer_imagen = imageio.imread(x)
            texto = y
            posicion = (100,100)
            font = cv2.FONT_ITALIC
            tamano = 1.5
            colorLetra = (250,250,250)
            grosorLetra = 4
        
            cv2.putText(leer_imagen,texto,posicion,font,tamano,colorLetra,grosorLetra)
    
            # anadir imagenes al arreglo img_array
            img_array.append(leer_imagen)
        except:
            print("Error de formato en archivo")
        
    
    #Guardar Gif
    nombre_archivo = punto + '.gif'
    try:
        imageio.mimwrite(nombre_archivo, img_array, 'GIF', duration=5)
    except:
        print("No image")



def generateGraphics(data,punto):
    #Graficando con Bokeh
    source=  ColumnDataSource(ColumnDataSource.from_df(data))
    #Figura width=750, plot_height=250,
        
    fig = figure(width=750, plot_height=280, title=None,
                     x_axis_type = "datetime",
                     tools= 'pan,box_zoom,save,reset,hover', sizing_mode='scale_width')
            
    #Gráfico línea
    fig.line(x="date_time",y="baliza",color='dodgerblue',line_width = 2,
                 legend_label= "Emergencia de baliza(cm)",source=source)
    
    #Puntito sobre cada dato
    fig.circle(x="date_time",
                y="baliza",
               source=source,
               color='orangered',
               selection_color='deepskyblue',
               nonselection_color='lightgray',
                nonselection_alpha=0.3,
              size=8)
        
    #Esto no esta funcionando la idea es que se desplieguen estos datos cuando pinchas uno de los puntos
    # Format tooltip
    tooltips = [ ('Pais', '@Pais'),
                    ('Nombre', '@Nombre'),
                    ('Grupo','@Grupo')]

    #Labels
    fig.xaxis.axis_label = "Fecha"
    fig.yaxis.axis_label = "Pérdida de hielo (cm)"
    
    #Leyenda
    fig.legend.location = "top_left"
    fig.legend.click_policy="hide"
    fig.legend.padding=5
    fig.legend.margin=0

    #Circulo que aparece al acercarse al dato
    hover_glyph = fig.circle(x='date_time', y='baliza', source=source,
                            size=15, alpha=0,
                           hover_fill_color='orangered', hover_alpha=0.5)

    fig.hover.tooltips = tooltips

    script , div = components(fig)
    #show(fig)
    
    return script , div



def getGraphicsGlaciar(data, punto):
    x = ['Pais','Grupo','cm','Seccion','Nombre','date','time']
    df = pd.DataFrame()
    
    for i in x:
        df[i] = None


    for i in data:
        if i['Baliza'] == punto:
            df = df.append({'Pais' : i['Pais'], 'Grupo' : i['Observador'],'cm' : int(i['Altura_cms']),'Seccion' : i['Segmento_Baliza'],
                       'Nombre' : i['Observador'],'Fecha' : i['Fecha_y_Hora'][:10],
                            'Hora' : i['Fecha_y_Hora'][-5:]},
                      ignore_index=True)

    #Transformando fecha y hora a datetime y eliminando nans
    df['date']=pd.to_datetime(df['Fecha'], format="%Y-%m-%d").dt.date.astype(str)
    df['time']=pd.to_datetime(df['Hora'], format="%H:%M").dt.time.astype(str)
    df["date_time"]=pd.to_datetime(df['Fecha']+" "+df['Hora'])
    df.set_index('date_time', inplace=True)
    df.drop(["Fecha","Hora"],axis=1,inplace=True)
    df.dropna(inplace=True);
    
    #Sumando largo de balizas anteriores para ver pérdida total de hielo en el periodo
    baliza= []
    for i in range(df.shape[0]):
        if df["Seccion"].iloc[i] == "1":
            baliza.append(df["cm"].iloc[i])
        elif df["Seccion"].iloc[i] == "2":
            baliza.append(df["cm"].iloc[i]+200)
        elif df["Seccion"].iloc[i] == "3":
            baliza.append(df["cm"].iloc[i]+400)
        elif df["Seccion"].iloc[i] == "4":
            baliza.append(df["cm"].iloc[i]+600)
        
    df["baliza"]= baliza
    
    script , div = generateGraphics(df,punto)
    print(div)
    #print(script)
    
    return script , div #df



def numberOfMedition(data, tipoPunto, punto):
    n = 0
    for i in data:
        if i[tipoPunto] == punto:
            n += 1
    #print(n)
    return n




def lostThickness(data):
    c = 0
    return c



# Puntos de cambio
KOBO_TOKEN = '26566dd7934bcb45fee86851765c4f7c867e9cc3'
kobo = KoboExtractor(KOBO_TOKEN, 'https://kf.kobotoolbox.org/api/v2') # kobo.humanitarianresponse.info
asset_uid = "ajYQ63QAQhzKx7F3F9zEvR" #"a7Wd6TUVqejWxSwBkzSGY9"
# asset_uid = "aGigj5YaeQpmeyqvzjUEVp" Para el otro formulario
#today = date.today()
#print(date.today())
datos_today = kobo.get_data(asset_uid,submitted_after = "2021-11-6" )
data = kobo.get_data(asset_uid)
data = kobo . sort_results_by_time(data['results'], reverse = True) 

puntos = ["punto_1", "punto_2", "punto_3", "punto_4", "punto_5" , "punto_6"]



import pickle

for punto in puntos:
    
    try:
        script, div = getGraphicCountry(punto,getCountryData(punto,data,'Punto_de_Observaci_n'))
    except:
        print("ERROR: getGraphicCountry => " + punto)
        
    try:
        img = getUrlData(punto, data, 'Punto_de_Observaci_n')
    except:
        img = "Not image"
        print("ERROR: getUrlData => " + punto)
        
    #try:
    getUrlDataList(punto, data, 'Punto_de_Observaci_n') # generar GIF
    #except:
    #    print("ERROR: GIF => " + punto)
    
    
    num_med = numberOfMedition(data,'Punto_de_Observaci_n',punto)
    perdido = lostThickness(data)
    
    d = {"punto": punto , "div" : div ,"script" : script,
        "img" : img, 
       "num_mediciones" : num_med, "perdido" : perdido}
    
    nombre_archivo = punto + ".json"
    with open(nombre_archivo, 'wb') as fp:
        pickle.dump(d, fp)



print("Cambios")
# Obtener los datos baliza
KOBO_TOKEN = '26566dd7934bcb45fee86851765c4f7c867e9cc3'
kobo = KoboExtractor(KOBO_TOKEN, 'https://kf.kobotoolbox.org/api/v2') # kobo.humanitarianresponse.info
#asset_uid = "atX9jThsvhvhhjFf573eng" #"a7Wd6TUVqejWxSwBkzSGY9"
asset_uid = "a5xomk6KgJfvM3CpiX23tH" # Para el otro formulario
#today = date.today()
datos_today = kobo.get_data(asset_uid,submitted_after = "2021-11-6" )
data = kobo.get_data(asset_uid)
data = data['results']

#puntos = ["punto_1", "punto_2", "punto_3", "punto_4", "punto_5" , "punto_6"]
baliza = ["b1","b2","b3","b4","b5","b6"]


print("")
print("Baliza")
for punto in baliza:
    try:
        script1 , div1 = getGraphicsGlaciar(data, punto)
        script2 , div2 = getGraphicCountry(punto,getCountryData(punto,data,"Baliza"))
        img, names = getUrlData(punto, data, 'Baliza')
        num_med = numberOfMedition(data,"Baliza",punto)
        perdido = lostThickness(data)
        print(punto)
    except:
        script1 , div1 = "","<h6> Sin datos <h6/>"
        script2 , div2 = "","<h6> Sin datos <h6/>"
        img, names = ["https://image.flaticon.com/icons/png/512/1034/1034633.png","https://image.flaticon.com/icons/png/512/1034/1034633.png","https://image.flaticon.com/icons/png/512/1034/1034633.png"] , ["No hay imagen","No hay imagen","No hay imagen"]
        num_med = "-"
        perdido = "-"

    d = {"punto": punto , "div1" : div1 ,"script1" : script1, "div2" : div2 ,"script2" : script2,
        "img" : img, "names" : names,
       "num_mediciones" : num_med, "perdido" : perdido}
        
    nombre_archivo = punto + ".json"
    with open(nombre_archivo, 'wb') as fp:
        pickle.dump(d, fp)

