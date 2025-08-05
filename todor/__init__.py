# Importamos la libreria Flask
from flask import Flask, render_template

# Luego de isntalar SQL-Alchemy importamos la libreria SQL-Alchemy
from flask_sqlalchemy import SQLAlchemy

# Crea,os una extencion de base de datos SQLAlchemy
db=SQLAlchemy()

# Creamos la aplicacion a traves de un afuncion con le fin de generar instancias
def create_app():
    app= Flask(__name__)

    # Seccion de configuracion del proyecto
    app.config.from_mapping(
        DEBUG=False,
        SECRET_KEY='devtodo',
        SQLALCHEMY_DATABASE_URI="sqlite:///todolist.db"
        
    )
    # Inicializamos la conexion a la base de datos
    db.init_app(app)

    # Registramos Blueprint
    from . import todo
    app.register_blueprint(todo.bp)

    # Registramos Blueprint
    from . import auth
    app.register_blueprint(auth.bp)
    # Creamos una vista y para ello se requiere de una ruta
    @app.route('/')
    # Creamos una funcion que se asocia con la ruta
    def index():
        return render_template('index.html')
    
    # Este codigo crea todas las tablas en la base de datos bansandose en modelos definidos con clases
    with app.app_context():
        db.create_all()
    
    return app




