from flask import Flask, request, Blueprint
import pprint
from csv import writer
import csv
import os
import pandas as pd
import pickle

import bokeh
from bokeh.io import output_file, show
from bokeh.layouts import row,column
from bokeh.plotting import figure,output_file, save, show, ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.resources import CDN
from bokeh.embed import components

import base64

nodo = Blueprint('api',__name__,url_prefix='/api')

directorio = "/home/iribarrenp/Geografia/"

@nodo.route("/post/<id>/<instrumento>", methods=["POST"])
def post(id,instrumento):
    datos = request.json
    #pprint.pprint(datos)

    if existeArchivo( directorio + 'static/monitoreoDinamico/' + id + '/' + instrumento + '.csv') == False:
        with open( directorio + 'static/monitoreoDinamico/' + id + '/' + instrumento + '.csv', 'a', newline='') as f_object:  
            writer_object = writer(f_object)
            writer_object.writerow(datos)  
            f_object.close()
            print("Nombres guardados")
        
    if instrumento != "camara":
        with open(directorio + 'static/monitoreoDinamico/' + id + '/' + instrumento + '.csv', 'a', newline='') as f_object:  
            writer_object = writer(f_object)
            writer_object.writerow(datos.values())  
            f_object.close()
            print("guardado")

        guardarGraficos(id,instrumento)
        return ""
    else:

        with open(directorio + 'static/monitoreoDinamico/' + id + '/' + instrumento + '.csv', 'a', newline='') as f_object:  
            writer_object = writer(f_object)
            writer_object.writerow(request.json['data'])  
            f_object.close()
            print("guardado")        

        info = request.json['dato']
        info = base64.b64decode(info)
        image_result = open(directorio + 'static/monitoreoDinamico/' + id + '/ultima.jpg', 'wb') # create a writable image and write the decoding result
        image_result.write(info)
        image_result = open(directorio + 'static/monitoreoDinamico/' + id + '/' + request.json['data'] +'.jpg', 'wb') # create a writable image and write the decoding result
        image_result.write(info)

        generarVideo(id)

        return ""


# Comprueba si esta el archivo
def existeArchivo(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False

# Obtiene los script y el div de los graficos
def guardarGraficos(id,instrumento):

    df = pd.read_csv(directorio + 'static/monitoreoDinamico/' + id + '/' + instrumento + '.csv')
    nombres_columnas = df.columns.values
    nombres_columnas_lista = list(nombres_columnas)
    nombres_columnas_lista.remove("data")

    #Transformando fecha y hora a datetime y eliminando nans
    df["data"]=pd.to_datetime(df['data'])
    df.set_index('data', inplace=True)
    df.dropna(inplace=True);

    dictGraficos = {}

    for i in nombres_columnas_lista:
        script, div = generarGraficos(df, i)
        dictGraficos[i] = [script,div]

    # Guardar los graficos
    with open(directorio + 'static/monitoreoDinamico/' + id + '/' + instrumento + '.json', 'wb') as fp:
        pickle.dump(dictGraficos, fp)


# Diccionario para darle nombres a los ejes de la grafica resultante
nombreEjeY = {
    "temperatura" : "Temperatura [°C]",
    "presion" : "Presion [milibares]",
    "humedad" : "Humedad [%]",
    "distancia" : "Distancia [cm] ",
    "precipitacion" : "Precipitacion []",
    "presionNeta": "Presión neta del agua [cmH20]"
}


# Genera los graficos
def generarGraficos(data, atributo):
    
    #print(data[atributo][0])

    #Graficando con Bokeh
    source=  ColumnDataSource(ColumnDataSource.from_df(data))
    #Figura width=750, plot_height=250,
        
    fig = figure(width=750, plot_height=280, title=None,
                     x_axis_type = "datetime",
                     tools= 'pan,box_zoom,save,reset,hover', 
                     sizing_mode='scale_width')
            
    #Grafico linea
    fig.line(x="data",y=atributo, color='dodgerblue',line_width = 2,
                legend_label = nombreEjeY[atributo], source=source)
                # source=source)
    

    #Puntito sobre cada dato
    fig.circle(x="data",
                y=atributo,
               source=source,
               color='orangered',
               selection_color='deepskyblue',
               nonselection_color='lightgray',
                nonselection_alpha=0.3,
              size=8)
        
    # Format tooltip
    tooltips = [ ('data', '@data'),]


    #Labels
    fig.xaxis.axis_label = "Fecha"
    fig.yaxis.axis_label = nombreEjeY[atributo]
    
    #Leyenda
    fig.legend.location = "top_left"
    fig.legend.click_policy="hide"
    fig.legend.padding=5
    fig.legend.margin=0


    #Circulo que aparece al acercarse al dato
    hover_glyph = fig.circle(x='data', y=atributo, source=source,
                            size=15, alpha=0,
                           hover_fill_color='orangered', hover_alpha=0.5)

    fig.hover.tooltips = tooltips

    script , div = components(fig)
    #show(fig)
    
    return script , div



import cv2
import numpy as np
import glob2 as glob
import ffmpy

def generarVideo(id):

    img_array = []
    listaFotos = glob.glob(directorio + 'static/monitoreoDinamico/' + id +'/*.jpg')
    listaFotos.sort(reverse=True) # Ordena las fotos en orden de fecha

    print(listaFotos)

    # Preguntar largo de video
    for filename in listaFotos:
        print(filename)
        img = cv2.imread(filename)
        print("A")
        height, width, layers = img.shape
        size = (width,height)
        img_array.insert(0,img)
    


    out = cv2.VideoWriter(directorio + 'static/monitoreoDinamico/' + id +'/video.avi',cv2.VideoWriter_fourcc(*'DIVX'), 1, size)
 
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

    avi_file_path = directorio + 'static/monitoreoDinamico/' + id +'/video.avi'
    output_name = directorio + 'static/monitoreoDinamico/' + id +'/video.mp4'


    os.popen("ffmpeg -y -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}'".format(input = avi_file_path, output = output_name))
