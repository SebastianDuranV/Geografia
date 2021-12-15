from flask import Flask, request, Blueprint, render_template,flash,redirect,url_for,session
import pprint
import pickle

import forms
from consultor_sql import User,Nodo, Category , db

nodoServidor = Blueprint('nodo',__name__,url_prefix='/nodo')

instrumentos = ["bmp280","ds18b20","ms5803","tipping", "ultrasonido"]

directorio = "/home/iribarrenp/Geografia/"


@nodoServidor.route('/<id>')
def consultaNodo(id):
    nodo = Nodo.query.filter_by(id=id).first_or_404()
    graficos = {}
    try:
        for instrumento in instrumentos:
            ubicacion = directorio + 'static/monitoreoDinamico/' + str(id) + '/' + instrumento + '.json'
            with open(ubicacion, 'rb') as file:
                graficos[instrumento] = pickle.load(file)
    except:
        return "<h1> Datos no completos </h1>"
      
    return render_template("monitoreoDinamico/mostrarNodo.html" ,graficos=graficos , id=str(id), nodo=nodo)

# Diccionario para disminuir el codigo
TipeClass = dict(
    User = User,
    Category = Category,
    Nodo = Nodo
)

formsPostDic = dict(
    Nodo = forms.FormNodo
)

import os
from os import system
from csv import writer
# Crear nodo
@nodoServidor.route('/crear', methods = ['POST','GET'] )
def createNodo(type = "Nodo"):
    comment_form = formsPostDic[type](request.form)
    user = User.query.filter_by(id=session['idUser']).first_or_404()
    if request.method == 'POST' and comment_form.validate():
        nombre = comment_form.nombre.data
        latitud = comment_form.latitud.data
        longitud = comment_form.longitud.data
        descripcion = request.form['Article']
        user = User.query.filter_by(id= session['idUser']).first_or_404()
        post = TipeClass[type](nombre=nombre, latitud=latitud, longitud=longitud, descripcion=descripcion, user=user)
        db.session.add(post)
        db.session.commit()
        post = TipeClass[type].query.filter_by(nombre=nombre, latitud=latitud, longitud=longitud, descripcion=descripcion, user=user).first_or_404()
        



        os.mkdir(directorio + 'static/monitoreoDinamico/' + str(post.id)) 

        nodoCsv = {
            "id": post.id,
            "nombre" : post.nombre,
            "latitud" : post.latitud,
            "longitud" : post.longitud
        }

        with open(directorio +'static/monitoreoDinamico/' + str(post.id) + '/info.csv', 'a', newline='') as f_object:  
                writer_object = writer(f_object)
                writer_object.writerow(nodoCsv.values())  
                f_object.close()

        return render_template('monitoreoDinamico/mostrar_nodo_admin.html', nodo=post, lat= post.latitud, lon = post.longitud)
        #return redirect(url_for('index'))
    else:
        return render_template('monitoreoDinamico/create_nodo.html', type="nodo", nodo=comment_form, typeEng=type,  isSuper = user.isSuperUser )

# Mostrar nodos a administrador:
@nodoServidor.route('modoeditor/<idPost>')
def mostrarNodoAdmin(idPost, type="Nodo"):
    post = TipeClass[type].query.filter_by(id=idPost).first_or_404()
    return render_template('monitoreoDinamico/mostrar_nodo_admin.html', nodo=post, lat= post.latitud, lon = post.longitud , nombre=post.nombre, id=post.id)


# Eliminar nodos
@nodoServidor.route('/deletePost/nodo/<idPost>')
def eliminarnodo(idPost, type="Nodo"):
    post = TipeClass[type].query.filter_by(id=idPost).first_or_404()
    db.session.delete(post)
    db.session.commit()
    os.rmdir(directorio +'static/monitoreoDinamico/' + idPost)
    return redirect(url_for('index'))


@nodoServidor.route('/lista')
def getList():
    getObject = request.args.get('type','<h1> No type declarated </h1>')
    user = User.query.filter_by(id=session['idUser']).first_or_404()
    try:
        #allObject = TipeClass[getObject].query.filter_by(user_id=session['idUser'])
        if user.isSuperUser == 0:
            allObject = TipeClass[getObject].query.filter_by(user_id=session['idUser'])
        else:
            allObject = TipeClass[getObject].query.all()
    except:
        return '<h1> No found type </h1>'

    #user = User.query.filter_by(id=session['idUser'])
    #if user.isSuperUser:
    #    allObject = TipeClass[getObject].query.filter_by(User=user)
    #else:
    #    allObject = TipeClass[getObject].query.all()

    return render_template('show_list_types.html', objects=allObject , type=getObject, isSuper = user.isSuperUser )


@nodoServidor.route('/editar/<idPost>', methods = ['POST','GET'] )
def updatePost(idPost,type = "Nodo"):
    user = User.query.filter_by(id=session['idUser']).first_or_404()
    post = TipeClass[type].query.filter_by(id=idPost).first_or_404()
    if request.method == 'POST':
        post.nombre = request.form['nombre']
        post.latitud = request.form['latitud']
        post.descripcion = request.form['descripcion']
        post.longitud = request.form['longitud']
        db.session.commit()
        flash("Actualizado")
        return render_template('monitoreoDinamico/mostrar_nodo_admin.html', nodo=post, lat= post.latitud, lon = post.longitud , nombre=post.nombre, id=post.id)
    else:
        return render_template('monitoreoDinamico/editar_nodo.html', post=post, id=idPost, type=type, isSuper = user.isSuperUser )
