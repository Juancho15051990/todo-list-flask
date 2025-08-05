# Importamos el modulo Blueprint desde flask que nos ayuda a organizar los modulos reutilizables
from flask import Blueprint, render_template, redirect, url_for, request, redirect, url_for, g

# Importamos el decorador de proteccion de rutas
from todor.auth import login_required
from .models import Todo, User
from todor import db
# Creamos una configuracion Blueprint
bp=Blueprint('todo',__name__, url_prefix='/todo')



# Creamos vistas a traves de las rutas
@bp.route('/list')
# Insertamos un decorador que se requiere iniciar sesion
@login_required
def index():
    todos=Todo.query.all()
    return render_template('todo/index.html', todos= todos)

@bp.route('/create', methods=('GET','POST'))
def create():
    # Recuperamos datos de la database
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']

        todo= Todo(g.user.id, title, desc)

        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo.index'))
    return render_template('todo/create.html')

# Funcion para la opcion editar
def get_todo(id):
    todo=Todo.query.get_or_404(id)
    return todo

@bp.route('/update/<int:id>', methods=('GET','POST'))
@login_required
def update(id):
    todo=get_todo(id)
    if request.method=='POST':
        todo.tittle=request.form['tittle']
        todo.desc=request.form['desc']
        todo.state=True if request.form.get('state')=='on' else False
        db.session.commit()
        return redirect(url_for('todo.index'))
    return render_template('todo/update.html', todo=todo)

# Boton eliminar
@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    todo=get_todo(id)
    db. session.delete(todo)
    db.session.commit()
    return redirect(url_for('todo.index'))


