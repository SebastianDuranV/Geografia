from flask import Flask, request, Blueprint, render_template
import pprint
import pickle

nodoConsultor = Blueprint('nodo',__name__,url_prefix='/nodo')

instrumentos = ["bmp280","ds18b20","ms5803","tipping", "ultrasonido"]

@nodoConsultor.route('/<id>')
def consultaNodo(id):
    
    graficos = {} 
    for instrumento in instrumentos:
        ubicacion = 'static/monitoreoDinamico/' + str(id) + '/' + instrumento + '.json'
        with open(ubicacion, 'rb') as file:
            graficos[instrumento] = pickle.load(file)

    #print(graficos)
        
    return render_template("monitoreoDinamico/mostrarNodo.html" ,graficos=graficos , id=str(id))