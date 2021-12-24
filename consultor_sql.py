from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/proyectogeografia'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://SebastianDuranVi:1996duranrugby@SebastianDuranVilches.mysql.pythonanywhere-services.com/SebastianDuranVi$geografia'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://iribarrenp:valdivia2021@iribarrenp.mysql.pythonanywhere-services.com/iribarrenp$geografia'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/geografia.db'

# Descomentar cuando se suba a pythonanywhere
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_POOL_RECYCLE'] = 30
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 40

# Comentar cuando se suba a pythonanywhere
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.config['SQLALCHEMY_POOL_RECYCLE'] = 30
#app.config['SQLALCHEMY_POOL_TIMEOUT'] = None
#app.config['SQLALCHEMY_POOL_SIZE'] = None


db = SQLAlchemy(app)
db.create_all()


#class Post(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    title = db.Column(db.String(120), nullable=False)
#    subtitle = db.Column(db.String(250), nullable=False)
#image =  db.Column(db.String(120), nullable=False)
#    body = db.Column(db.Text, nullable=False)
#    pub_date = db.Column(db.DateTime, nullable=False,
#        default=datetime.utcnow)#


    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        #nullable=False)
    #user = db.relationship('User',
    #    backref=db.backref('posts', lazy=True))
##
    #def __repr__(self):
        #return '%r' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '%r' % self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    lastname = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    isSuperUser = db.Column(db.Boolean, nullable=False, default=0)

    def __repr__(self):
        return '%r' % self.username

#class SuperUser(User):
#    def __init__(self):
#        self.isSuperUser = db.Column(db.Boolean, nullable=False, default=1)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    image =  db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('posts', lazy=True))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
        nullable=False)
    category = db.relationship('Category',
        backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '%r' % self.title
    #pass

class Maps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    image =  db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('maps', lazy=True))

    def __repr__(self):
        return '%r' % self.title

class Proyects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    image =  db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('proyects', lazy=True))

    def __repr__(self):
        return '%r' % self.title

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    image =  db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('news', lazy=True))

    def __repr__(self):
        return '%r' % self.title

class Monitoring(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    image =  db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('monirotings', lazy=True))

    def __repr__(self):
        return '%r' % self.title


class Nodo(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    latitud = db.Column(db.Float, nullable=False)
    longitud = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)


    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('nodo', lazy=True))
    
    def __repr__(self):
        return '(%s,%s,%s,%s, %s)' % (self.id,self.nombre,self.latitud,self.longitud,self.descripcion)
