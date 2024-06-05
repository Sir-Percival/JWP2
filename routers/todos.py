from flask import Blueprint, request, redirect, url_for, render_template
from jose import jwt, JWTError
import models
from database import SessionLocal
from .auth import SECRET_KEY, ALGORITHM

todos_blueprint = Blueprint('todos', __name__, template_folder='templates')

def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user():
    token = request.cookies.get('access_token')
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {'username': payload.get('user'), 'id': payload.get('id')}
    except JWTError:
        return None

def get_todos_by_user_id(user_id):
    db =next(get_database())
    todos = db.query(models.Todos).filter(models.Todos.owner_id == user_id).order_by(models.Todos.complete, models.Todos.priority.desc()).all()
    return todos

@todos_blueprint.route('/', methods=['GET'])
def read_all_by_user():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    db = next(get_database())
    todos = get_todos_by_user_id(user['id'])
    return render_template('home.html', todos=todos, user=user)

@todos_blueprint.route('/add-todo', methods=['GET', 'POST'])
def add_new_todo():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        db = next(get_database())
        todo = models.Todos(
            title = request.form['title'],
            description = request.form['description'],
            priority = request.form['priority'],
            complete = False,
            owner_id = user['id']
        )
        db.add(todo)
        db.commit()
        return redirect(url_for('todos.read_all_by_user'))
    return render_template('add-todo.html', user=user)

@todos_blueprint.route('/edit-todo/<int:todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    db = next(get_database())
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.description = request.form['description']
        todo.priority = request.form['priority']
        db.add(todo)
        db.commit()
        return redirect(url_for('todos.read_all_by_user'))
    return render_template('edit-todo.html', todo=todo, user=user)

@todos_blueprint.route('/delete/<int:todo_id>', methods=['GET'])
def delete_todo(todo_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    db = next(get_database())
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user['id']).first()
    if todo:
        db.delete(todo)
        db.commit()
    return redirect(url_for('todos.read_all_by_user'))

@todos_blueprint.route('/complete/<int:todo_id>', methods=['GET'])
def complete_todo(todo_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))
    db = next(get_database())
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    todo.complete = not todo.complete
    db.add(todo)
    db.commit()
    return redirect(url_for('todos.read_all_by_user'))