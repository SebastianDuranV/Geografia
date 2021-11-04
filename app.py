from flask import Flask, redirect, render_template, url_for, request, flash, make_response, session
from consultor_sql import User, Category , db, Blog, News, Monitoring, Proyects, Maps, app
import forms
import os
from werkzeug.utils import secure_filename
from pandas import pandas as pd
import glob


#app = Flask(__name__)
app.secret_key = 'Mi_perro_se_llama_manjar'
db.create_all()

# Diccionario para disminuir el codigo
TipeClass = dict(
    User = User,
    Category = Category,
    Blog = Blog ,
    News = News ,
    Monitoring = Monitoring ,
    Maps =  Maps ,
    Proyects = Proyects
)

# El modo editor es para tener acceso a la base de datos.
@app.route('/ModoEditor')
def index():
    try:
        if session['idUser']:
            user = User.query.filter_by(id=session['idUser']).first_or_404()
            return render_template('index_user.html',  isSuper = user.isSuperUser )
            #if user.isSuperUser:
            #    return render_template('index_user.html', isSuper = 1)
            #return render_template('index_user.html', isSuper = 0)
    except:
        return render_template("index.html")

#Crear objetos
formsPostDic = dict(
    Blog = forms.FormBlog ,
    News = forms.FormNews ,
    Monitoring = forms.FormMonitoring ,
    Maps =  forms.FormWebMaps ,
    Proyects = forms.FormProyects
)

translateNameSingle = dict(
    Blog = "Blog",
    News = "Noticias",
    Monitoring = "Monitoreo",
    Maps = "WebMaps",
    Proyects = "Proyectos"
)

# Cargar archivos en directorio 
# Crear directorio
def createDirectory(id,type,x=0):
    directory = os.path.join('/home/iribarrenp/Geografia/static/uploaders/' + type + '/' + str(id))
    #directory = os.path.join('C:/Users/Sebastián-Durán/Documents/P R O Y E C T O S/Nueva carpeta/Geografia/static/uploaders/' + type + '/' + str(id))
    os.mkdir(directory)


#Cargar archivos
def upload(id,type,request):
    createDirectory(id,type)
    app.config['UPLOAD_FOLDER'] = "/home/iribarrenp/Geografia/static/uploaders/" + type +'/'+ str(id)
    #app.config['UPLOAD_FOLDER'] = "C:/Users/Sebastián-Durán/Documents/P R O Y E C T O S/Nueva carpeta/Geografia/static/uploaders/" + type +'/'+ str(id)

    # save each "charts" file
    uploaded_files = request.files.getlist("files")
    for file in uploaded_files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


# Creación de un usuario nuevo
@app.route('/createUser', methods = ['POST','GET'] )
def createUser():
    comment_form = forms.FormUser(request.form)
    if request.method == 'POST' and comment_form.validate():
        userName = comment_form.name.data
        lastname = comment_form.lastname.data
        password = comment_form.password.data
        email = comment_form.email.data
        user = User(username=userName , email=email, lastname = lastname, password=password )
        db.session.add(user)
        db.session.commit()
        flash("Usuario creado")
        return redirect(url_for('index'))
    else:
        return render_template('create_user.html', user=comment_form)

#Creación de una nueva categoría para {la sección de los blog
@app.route('/createCategory', methods = ['POST','GET'] )
def createCategory():
    comment_form = forms.FormCategory(request.form)
    user = User.query.filter_by(id=session['idUser']).first_or_404()
    if request.method == 'POST' and comment_form.validate():
        name = comment_form.name.data
        cat = Category(name=name)
        db.session.add(cat)
        db.session.commit()
        flash("Categoría para blog creado")
        return redirect(url_for('createCategory'))
    else:
         return render_template('create_category.html', cat=comment_form,  isSuper = user.isSuperUser )

# Crea un blog y lo asocia a una categoría
@app.route('/createPost/<type>', methods = ['POST','GET'] )
def createPost(type):
    comment_form = formsPostDic[type](request.form)
    user = User.query.filter_by(id=session['idUser']).first_or_404()
    if request.method == 'POST' and comment_form.validate():
        title = comment_form.title.data
        subtitle = comment_form.subtitle.data
        image = comment_form.image.data
        body = request.form['Article']
        user = User.query.filter_by(id= session['idUser']).first_or_404()
        if type == "Blog":
            categoryId =  request.form.get('category')
            category = Category.query.filter_by(id = categoryId).first_or_404()
            post = TipeClass[type](title=title, subtitle=subtitle, body=body,category=category ,user=user, image=image)
        else:
            post = TipeClass[type](title=title, subtitle=subtitle, body=body, user=user, image=image)
        db.session.add(post)
        db.session.commit()
        post = TipeClass[type].query.filter_by(title=title, subtitle=subtitle, body=body, user=user).first_or_404()
        if request.files["files"]:
            upload(post.id,type,request)
        #return render_template('create_post.html', type=translateNameSingle[type], post=comment_form, typeEng=type)
        return redirect(url_for('index'))
    else:
        if type == "Blog":
            cat = Category.query.all()
            return render_template('create_post.html', type=translateNameSingle[type], post=comment_form, typeEng=type, cat = cat,  isSuper = user.isSuperUser )
        return render_template('create_post.html', type=translateNameSingle[type], post=comment_form, typeEng=type,  isSuper = user.isSuperUser )




# Función para eliminar datos en la base de datos.
# Para usuarios
@app.route('/deleteUser/<username>')
def delete_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

# Para categorías
@app.route('/deleteCategory/<idCat>')
def delete_category(idCat):
    cat = Category.query.filter_by(id=idCat).first_or_404()
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for('index'))

# Para los post
@app.route('/deletePost/<type>/<idPost>')
def delete_post(idPost,type):
    post = TipeClass[type].query.filter_by(id=idPost).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))


#Actualizar bases de datos
@app.route('/updateUserPerfil', methods = ['POST','GET'] )
def updatePerfil():
    id = session['idUser']
    user = User.query.filter_by(id=id).first_or_404()
    if request.method == 'POST':
        user.userName = request.form['username']
        user.lastName = request.form['lastname']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.commit()
        flash("Usuario fue actualizado")
        return render_template('update_user.html' , user=user, isSuper = user.isSuperUser )
    else:
        return render_template('update_user.html' , user=user, isSuper = user.isSuperUser )


@app.route('/updateCategory/<idCat>', methods = ['POST','GET'] )
def updateCategory(idCat):
    user = User.query.filter_by(id=session['idUser']).first_or_404()
    cat = Category.query.filter_by(id=idCat).first_or_404()
    if request.method == 'POST':
        cat.name = request.form['name']
        db.session.commit()
        flash("Categoría fue actualizado")
        return render_template('update_category.html', cat=cat, id=idCat, isSuper = user.isSuperUser )
    else:
        return render_template('update_category.html', cat=cat, id=idCat, isSuper = user.isSuperUser )

@app.route('/updatePost/<type>/<idPost>', methods = ['POST','GET'] )
def updatePost(idPost,type):
    user = User.query.filter_by(id=session['idUser']).first_or_404()
    post = TipeClass[type].query.filter_by(id=idPost).first_or_404()
    if request.method == 'POST':
        post.title = request.form['title']
        post.subtitle = request.form['subtitle']
        post.body = request.form['body']
        post.image = request.form['image']
        #if type=='Blog':
        #    try:
        #        categoryId =  request.form.get('category')
         #       category = Category.query.filter_by(id = categoryId).first_or_404()
        #        post.category_id = category
        #    except:
        #        return 'ERRor'
        db.session.commit()
        flash("Actualizado")
        #if type=="Blog":
        #    category = Category.query.all()
        #    return render_template('update_post.html', post=post, id=idPost, type=type, isSuper = user.isSuperUser, cat = category)
        return render_template('update_post.html', post=post, id=idPost, type=type, isSuper = user.isSuperUser )
    else:
        #if type=="Blog":
        #    category = Category.query.all()
        #    return render_template('update_post.html', post=post, id=idPost, type=type, isSuper = user.isSuperUser, cat = category)
        return render_template('update_post.html', post=post, id=idPost, type=type, isSuper = user.isSuperUser )


# Mostrar en el frontend.
@app.route('/getList')
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


@app.route('/user/<username>')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_user.html', user=user)


@app.route('/post/<type>/<idpost>')
def show_post(idpost,type):
    post = TipeClass[type].query.filter_by(id=idpost).first_or_404()
    otherpost = TipeClass[type].query.order_by(TipeClass[type].pub_date).all()

    # hacer un sistema de previo y siguiente
    for i in range(len(otherpost)):
        if otherpost[i].id == post.id:
            try:
                prev = otherpost[i-1].id
            except:
                prev = 0
            try:
                later = otherpost[i+1].id
            except:
                later = 0
    if type == 'Blog':
        category = Category.query.all()
        return render_template('/Frontal/single.html', post=post, prev = prev, later = later, type=type, category=category)
    return render_template('/Frontal/single.html', post=post, prev = prev, later = later, type=type)



# Sesiones de usuario
# Para acceder a la base de datos
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = forms.FormLoginUser(request.form)
    if request.method == 'POST' and login_form.validate():
        try:
            user = User.query.filter_by(email=login_form.email.data).first_or_404()
        except:
            flash("Email o contraseña no valida")
            return render_template('login.html', user = login_form)
        if login_form.password.data == user.password:
            session['idUser'] = user.id
            return redirect(url_for('index'))
        else:
            flash("Email o contraseña no valida")
            return render_template('login.html', user = login_form)
    else:
        return render_template('login.html', user = login_form)

# Salir
@app.route('/logout')
def logout():
    if 'idUser' in session:
        session.pop('idUser')
    return redirect(url_for('login'))




#### PAGINA NUEVA :::::::::
@app.route('/')
@app.route('/index')
def indexx():
    blogs = Blog.query.order_by(Blog.pub_date.desc()).limit(5).all()
    news = News.query.order_by(News.pub_date.desc()).limit(5).all()
    #proyects = Proyects.query.all()
    #maps = Maps.query.all()
    #monitoring = Monitoring.query.all()
    return render_template('/Frontal/index.html', Blogs = blogs , news =news )

@app.route('/<type>')
def getPublicList(type):
    try:
        allObject = TipeClass[type].query.order_by(TipeClass[type].pub_date.desc()).all()
    except:
        return '<h1> No found type </h1>'
    if type == 'Blog':
        category = Category.query.all()
        return render_template('Frontal/list.html', posts = allObject , type='Blog', transType = 'Blog', category=category)
    return render_template('Frontal/list.html', posts = allObject , type=type, transType = translateNameSingle[type])

@app.route('/Blog/<idcategory>')
def getPublicListBlogCategory(idcategory):
    category = Category.query.filter_by(id=idcategory).first_or_404()
    allObject = Blog.query.filter_by(category=category).all()
    category = Category.query.all()
    return render_template('Frontal/list.html', posts = allObject , type='Blog', transType = 'Blog', category=category)

## BUSQUEDA
@app.route('/search')
def searchs():
    getObject = request.args.get('search','<h1> No type declarated </h1>')
    search = getObject.split()
    types =["News","Monitoring","Blog","Maps","Proyects"]
    allObject = []
    for k in types:
        listType = TipeClass[k].query.order_by(TipeClass[k].pub_date.desc()).all()
        listType = list(listType)
        print(listType)
        for i in listType:
            exist = True
            j = 0
            while j < len(search) and exist:
                if not search[j] in (i.title + " " + i.subtitle + " " + i.body):
                    exist = False
                j += 1
            if exist :
                allObject.append(i)
    return render_template('Frontal/list.html', posts = allObject , type="Resultado de busqueda", transType = "Resultado de busqueda")

@app.route('/contact_us')
def contact_us():
    return render_template('/Frontal/contact_us.html')


# Proyecto exploradores
# Monitoreo de un glaciar
# Mostrar mapa
@app.route('/Monitoring/glaciar')
def map_glaciar():
    return render_template('/Frontal/glaciar.html')

# Mostrar mapas
import pickle
@app.route('/Monitoring/glaciar/<nameType>/<id>')
def prueba(nameType, id):
    df = pd.read_csv("C:/Users/Sebastián-Durán/Documents/P R O Y E C T O S/Nueva carpeta/Geografia/static/csv_glaciar/example_baliza.csv")
    #df = 

    if nameType == 'cambios':
        x = 'punto_'
        nombre_archivo = x + id + ".json"
    else:
        x = 'b'
        nombre_archivo = x + id + ".json"


    path = "C:/Users/Sebastián-Durán/Documents/P R O Y E C T O S/Nueva carpeta/Geografia/static/exploradores/"

    with open(path + nombre_archivo, 'rb') as fp:
        dat = pickle.load(fp)
    #print(type(df))
    #df = pd.DataFrame.from_dict(dat)


    print("")
    print(dat)
    print("")
    print("")

    return render_template('/Frontal/glaciar/graficos.html', information=dat, nameType = nameType )

@app.route('/single')
def single():
    return render_template('/Frontal/single.html')


@app.route('/show_casa')
def show_casa():

    #Fecha ultimo dato
    data= pd.read_csv("/home/iribarrenp/Geografia/static/monitoreo/casa/datos/bmp280.csv")
    data= data.iloc[:,1:]
    data.columns=["Date","Temp","Hum","Press","lluvia"]#Renombro columnas porque se me dan vuelta :)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index("Date",inplace=True)
    fecha=str(data.index[-1])[:-10]

    #Ruta ultima foto
    files = glob.glob("/home/iribarrenp/Geografia/static/monitoreo/casa/fotos/"+"*.jpg")
    files.sort(key=os.path.getmtime)
    foto= files[-1]
    foto=foto.split('/static')[-2:][1]

    #Ruta ultimos datos
    templateData = {
      'fecha': fecha,
      'ruta_foto':foto
      }

    return render_template('/Frontal/casa.html',**templateData)

# Creación de nuevo proyecto


# Comentar al momento de implementarlo en la web.
if __name__=='__main__':
    app.run(host= '0.0.0.0',debug=True)



