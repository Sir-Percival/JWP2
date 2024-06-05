from datetime import datetime, timedelta
from jose import jwt
from flask import Blueprint, request, make_response, redirect, url_for, render_template
from werkzeug.security import check_password_hash, generate_password_hash

import models
from database import SessionLocal

SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"

auth_blueprint = Blueprint('auth', __name__, template_folder='templates')


def get_database():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_access_token(username: str, user_id: int, expires_delta: timedelta = None):
    encode = {'user': username, 'id': user_id}
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db = next(get_database())
        username = request.form['username']
        password = request.form['password']
        user = db.query(models.Users).filter(models.Users.username == username).first()
        if user and check_password_hash(user.hashed_password, password):
            token = create_access_token(user.username, user.id, expires_delta=timedelta(minutes=60))
            response = make_response(redirect(url_for('todos.read_all_by_user')))
            response.set_cookie('access_token', token, httponly=True)
            return response
        return render_template('login.html', msg='Incorrect username or password')
    return render_template('login.html')


@auth_blueprint.route('/logout')
def logout():
    response = make_response(render_template('login.html', msg='Logout successful'))
    response.delete_cookie('access_token')
    return response


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = next(get_database())
        email = request.form['email']
        username = request.form['username']
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        password = request.form['password']
        password2 = request.form['password2']
        if password != password2:
            return render_template('register.html', msg='Passwords do not match')
        if db.query(models.Users).filter(models.Users.username == username).first():
            return render_template('register.html', msg='Username already exists')
        if db.query(models.Users).filter(models.Users.email == email).first():
            return render_template('register.html', msg='Email already exists')
        user = models.Users(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            hashed_password=generate_password_hash(password),
            is_active=True
        )
        db.add(user)
        db.commit()
        return render_template('login.html', msg='User successfully created')
    return render_template('register.html')
