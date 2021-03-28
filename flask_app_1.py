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

TipeClass = dict(
    User = User,
    Category = Category,
    Blog = Blog ,
    News = News ,
    Monitoring = Monitoring ,
    Maps =  Maps ,
    Proyects = Proyects
)

# Inicio
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

# Cargar archivos en directorio ::::::::::::::::::
#Crear directorio
def createDirectory(id,type,x=0):
    #if x != 0 :
    #    return 0
    directory = os.path.join('/home/iribarrenp/Geografia/static/uploaders/' + type + '/' + str(id))
    #try:
        #os.makedirs(directory)
    #try:
    os.mkdir(directory)
    #except:
    #    return 0
    #except:
    #    directory = os.path.join('./static/uploaders/' + type)
    #    os.mkdir(directory)
        #os.makedirs(directory)
    #    createDirectory(id,type,1)


#Cargar archivos
def upload(id,type,request):
    createDirectory(id,type)
    app.config['UPLOAD_FOLDER'] = "/home/iribarrenp/Geografia/static/uploaders/" + type +'/'+ str(id)
    #f = request.files['files']
    #filename = secure_filename(f.filename)
    #f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # save each "charts" file
    uploaded_files = request.files.getlist("files")
    for file in uploaded_files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    #for file in request.files['files']:
    #    print(file)
    #    file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))


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




# Eliminar
@app.route('/deleteUser/<username>')
def delete_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/deleteCategory/<idCat>')
def delete_category(idCat):
    cat = Category.query.filter_by(id=idCat).first_or_404()
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/deletePost/<type>/<idPost>')
def delete_post(idPost,type):
    post = TipeClass[type].query.filter_by(id=idPost).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))




#@app.route('/updateUser/<username>', methods = ['POST','GET'] )
#def updateUser(username):
#    user = User.query.filter_by(username=username).first_or_404()
#    if request.method == 'POST':
#        user.userName = request.form['username']
#        user.email = request.form['email']
#        db.session.commit()
#        flash("Usuario fue actualizado")
        #return redirect(url_for('index'))
#        return render_template('update_user.html' , user=user, username=username)
#    else:
#        return render_template('update_user.html' , user=user, username=username)


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
        if type=='Blog':
            post.category_id = request.form['idcategory']
        db.session.commit()
        flash("Actualizado")
        return render_template('update_post.html', post=post, id=idPost, type=type, isSuper = user.isSuperUser )
    else:
        return render_template('update_post.html', post=post, id=idPost, type=type, isSuper = user.isSuperUser )


# Mostrar
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
# ::: Entrar
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

# ::: Salir
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

@app.route('/single')
def single():
    return render_template('/Frontal/single.html')


@app.route('/show_casa')
def show_casa():

    #Fecha ultimo dato
    data= pd.read_csv("/home/iribarrenp/mysite/static/casa/datos/bmp280.csv")
    data= data.iloc[:,1:]
    data.columns=["Date","Temp","Hum","Press","lluvia"]#Renombro columnas porque se me dan vuelta :)
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index("Date",inplace=True)
    fecha=str(data.index[-1])[:-10]

    #Ruta ultima foto
    files = glob.glob("/home/iribarrenp/mysite/static/casa/fotos/"+"*.jpg")
    files.sort(key=os.path.getmtime)
    foto= files[-1]
    foto=foto.split('/static')[-2:][1]

    #Ruta ultimos datos
    templateData = {
      'fecha': fecha,
      'ruta_foto':foto
      }

    return render_template('/Frontal/casa.html',**templateData)