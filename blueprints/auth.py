from flask import Blueprint, render_template, request
from flask_login import login_user, logout_user
from manage import *
from methods import *
from werkzeug.security import check_password_hash


auth = Blueprint('auth', __name__)

def read_login_form():
    name = request.form.get('name')
    surname = request.form.get('surname')
    school = request.form.get('school')
    corpus = request.form.get('school')
    login_field = request.form.get('login')
    password = request.form.get('password')

    return name, surname, school, corpus, login_field, password


@auth.route('/login', methods=['GET', 'POST'])
@safe
def login():
    if request.method == 'POST':
        login_field = request.form.get('username')
        password = request.form.get('password')

        user = find_user_by_login(login_field)
        if not user or not check_password_hash(user.password_hash, password):
            flash('Неверный логин или пароль.', 'error')
            return redirect('/auth/login')

        login_user(User(user))
        flash('Вы успешно вошли!', 'success')

        if user.is_admin: return redirect('/admin/HomePage')
        else: return redirect('/posts/news')

    return render_template('login.html')


@auth.route('/logout')
@safe
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'success')
    return redirect('/auth/login')


@auth.route('/user/register', methods=['GET', 'POST'])
@safe
def register_user():
    if request.method == 'POST':
        name, surname, school, corpus, login_field, password = read_login_form()

        if find_user_by_login(login_field):
            flash('Этот логин уже занят. Попробуйте другой.', 'error')
            return redirect('/auth/user/register')

        create_user(name, surname, school, corpus, False, login_field, password)
        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')

        return redirect('/auth/login')

    return render_template('register.html')

@auth.route('/admin/register', methods=['GET', 'POST'])
@safe
def register_admin():
    if request.method == 'POST':
        name, surname, school, corpus, login_field, password = read_login_form()

        if find_user_by_login(login_field):
            flash('Этот логин уже занят. Попробуйте другой.', 'error')
            return redirect('/auth/admin/register')

        create_user(name, surname, school, corpus, True, login_field, password)

        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')

        return redirect('/auth/login')

    return render_template('register_admin.html')