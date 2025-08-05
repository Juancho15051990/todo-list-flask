                 # CREACION DE MODELOS PARA LA BASE DE DATOS

# Importamos la instantacia de la base de datos DB
from todor import db

# Creamos una clase para regisstrar usuarios y heredamos de la clase modelo
class User(db.Model):
    # Campos de la tabla de usuario
    id=db.Column(db.Integer, primary_key=True)
    # Columna Usuario, acepta valores unicos y hasta 20 carateres
    username=db.Column(db.String(20), unique=True, nullable=False)
    # Columna Contraseña, No acepta valores nulos
    password=db.Column(db.Text, nullable=False)

    # Creamos un constructor para simplificar el proceso
    def __init__(self, username, password):
        self.username= username
        self.password=password

    # Creamos una funcion para obtener datos y represntados por el usuario
    def __repr__(self):
        return f'<User: {self.username}>'

class Todo(db.Model):
    # Campos de la tabla de usuario
    id=db.Column(db.Integer, primary_key=True)
    # Creamos una relacion con la tabla usuarios
    created_by=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Columna del titulo de la tarea
    tittle=db.Column(db.String(100), nullable=False)
    # Columna para descripcion de la tarea
    desc=db.Column(db.Text)
    # Creamos columna para el campo del estado
    state=db.Column(db.Boolean, default=False)

    # Creamos un constructor para simplificar el proceso
    def __init__(self, created_by, tittle, desc, state=False):
        self.created_by= created_by
        self.tittle=tittle
        self.desc=desc
        self.state=state

    # Creamos una funcion para obtener datos y representados por el usuario
    def __repr__(self):
        return f'<Todo: {self.tittle}>'
    
