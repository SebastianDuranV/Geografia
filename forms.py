
from wtforms import Form, StringField, TextField, validators, FloatField
from wtforms.fields.html5 import EmailField



class FormPost(Form):
    title = StringField('Titulo',
        [
            validators.required(message= 'El titulo es requerido'),
            validators.length(min=1, max=120, message='Ingrese un titulo valido.')
        ])
    subtitle = StringField('Subtitulo',
        [
            validators.Required(message= 'El subtitulo es requerido'),
            validators.length(min=1, max=250, message='Ingrese un subtitulo valido.')
        ])
    image = StringField('Imagen',
        [
            validators.required(message= 'La imagen es requerido'),
            validators.length(min=1, max=120, message='Ingrese una imagen valido.')
        ])
    body = TextField('Cuerpo')


class FormCategory(Form): 
    name = StringField('Nombre de categoria',
        [
            validators.Required(message= 'El nombre es requerido'),
            validators.length(min=1, max=50, message='Ingrese un nombre valido.')
        ])


class FormUser(Form):
    name = StringField('Nombres',
        [
            validators.Required(message= 'El nombre es requerido'),
            validators.length(min=1, max=80, message='Ingrese un nombre valido.')
        ])
    lastname = StringField('Apellidos',
        [
            validators.Required(message= 'Los apellidos es requerido'),
            validators.length(min=1, max=80, message='Ingrese los apellidos validos.')
        ])
    password = StringField('Contraseña',
        [
            validators.Required(message= 'El contraseña es requerido'),
            validators.length(min=1, max=100, message='Ingrese un contraseña valido.')
        ])
    email = EmailField('Correo electrónico',
        [
            validators.Required(message= 'El correo electrónico es requerido'),
            validators.Email(message='Ingrese un correo electrónico valido.')
        ])


class FormLoginUser(Form):
    password = StringField('Contraseña',
        [
            validators.Required(message= 'El contraseña es requerido'),
            validators.length(min=1, max=100, message='Ingrese un contraseña valido.')
        ])
    email = EmailField('Correo electrónico',
        [
            validators.Required(message= 'El correo electrónico es requerido'),
            validators.Email(message='Ingrese un correo electrónico valido.')
        ])

class FormBlog(FormPost):
    categoryName = StringField('Categoría')

class FormProyects(FormPost):
    pass

class FormNews(FormPost):
    pass


class FormMonitoring(FormPost):
    pass

class FormWebMaps(FormPost):
    pass


class FormNodo(Form):
    nombre = StringField('nombre',
        [
            validators.Required(message= 'El nombre es requerido'),
            validators.length(min=1, max=80, message='Ingrese un nombre valido.')
        ])
    latitud = FloatField('latitud',
        [
            validators.Required(message= 'Latitud es requerido'),
        ])
    longitud = FloatField('longitud',
        [
            validators.Required(message= 'El longitud es requerido'),
        ])