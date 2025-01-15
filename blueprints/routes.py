from flask import Blueprint, render_template, request, flash, redirect, session
from methods import get_all_news
from manage import *
from models import Credentials
from werkzeug.security import check_password_hash

main_routes = Blueprint('routes', __name__)

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')

        credentials = Credentials.query.filter_by(login=login).first()
        if not credentials or not check_password_hash(credentials.password_hash, password):
            flash('Неверный логин или пароль.', 'error')
            return redirect('/routes/login')

        session['user_id'] = credentials.user_id
        login_user(User(credentials))
        print(credentials.user.is_admin)
        flash('Вы успешно вошли!', 'success')
        if credentials.user.is_admin:
            print(session)
            return redirect('/admin/HomePage')
        else:
            print(session)
            return redirect('/users/HomePage')

    return render_template('login.html')


@main_routes.route('/logout')
def logout():
    logout_user()
    session.pop('user_id', None)
    flash('Вы вышли из системы.', 'success')
    return redirect('/routes/login')


@main_routes.route("/events")
def events():
    news_list = get_all_news()
    return render_template("index.html", news=news_list, page_type="events")

@main_routes.route("/wall")
def wall():
    return render_template("index.html", page_type="wall")

@main_routes.route("/team_search")
def team_search():
    return render_template("index.html", page_type="team_search")
