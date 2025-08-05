# Importamos el modulo Blueprint desde flask que nos ayuda a organizar los modulos reutilizables
from flask import Blueprint
# Importamos reder_template para mostrar pagina HTML desdde carpeta TEMPLATES
from flask import render_template
# Importamos request para obtencion de datos de formulario
from flask import request
# Importamos url_for para generar url_for para generar url automaticamente
from flask import url_for
# Importamos redirect que permite rediccionar a otra pagina
from flask import redirect
# Importamos flash quien se encarga de enviar mensajes a las plantillas
from flask import flash
# Importamos funciones para encriptar la clave y autenticar
from werkzeug.security import generate_password_hash, check_password_hash
# Importamos session para inicio de sesion, el objeto g se utiliza para guardar cualquier valor
from flask import session, g

# Importamos la base de datos de usuarios datos de la tabla
from . models import User
from todor import db

# Creamos una configuracion Blueprint
bp=Blueprint('auth',__name__, url_prefix='/auth')
# Creamos las vista, indicando los metodos que registro
@bp.route('/register', methods=('GET','POST'))
# Creamos una funcion y metodo para bloque de registro de usuarkio
def register():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        # Creamos un objeto de tipo usuario
        user=User(username, generate_password_hash(password))
        # Mensaje de error cuando el usuario ya esta registrado
        error=None

        # Realizamos una consulta a la base de datos si el usuario ya esxiste
        user_name=User.query.filter_by(username=username).first()
        # Si el valor es nulo quiere decir que no existe y se procede a registar
        if user_name==None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        # mensaje de error cuando el usuario ya existe
        else:
            error=f'El usuario {username} ya existe'

        flash(error)

    return render_template('auth/register.html')

# Creamos una funcion y metodo para bloque de inicio de sesion
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        # Mensaje de error cuando el usuario ya esta registrado
        error=None

        # Validar datos para autenticacion
        user=User.query.filter_by(username=username).first()
        if user==None:
            error='Usuario Incorrecto'
        elif not check_password_hash(user.password, password):
            error='Contraseña Incorrecta'

        # Inicio de sesion
        if error is None:
            # Limpiamos la sesion
            session.clear()
            # Inicio de sesion y guardamos los datos de quien inicia la sesion
            session['user_id']=user.id         
            return redirect(url_for('todo.index'))
       
        flash(error)
    return render_template('auth/login.html')

# Con este arreglo indicamos qu se ejecuta la funcion load_logged en cada peticion
@bp.before_app_request
# Codigo para mantener iniciada la sesion
def load_logged_in_user():
    # Recuperamos el nombres de usuario desde session
    user_id=session.get('user_id')
    if user_id is None:
        g.user=None
    else:
        g.user=User.query.get_or_404(user_id)

# Funcion y vista para cerrar ssion
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Utilizamos un decorador para porteger las rutas evitando que usuarios no autenticados acceadan a ciertas rutas
import functools
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # Si nadie a iniciado sesion redireccionamos a la pagina de inicio
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
        


