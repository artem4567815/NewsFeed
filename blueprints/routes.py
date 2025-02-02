from flask import Blueprint, render_template, request, flash, jsonify
from methods import get_all_news, find_news_by_id, save_file, add_to_database2, to_moderation
from manage import *
from models import Credentials, Users
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

        login_user(User(credentials))
        flash('Вы успешно вошли!', 'success')
        if credentials.user.is_admin:
            return redirect('/admin/HomePage')
        else:
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
    return render_template("index.html", news=news_list, page_type="news")

@main_routes.route("/title/<id>")
def detailed_news(id):
    news = find_news_by_id(id)
    if not news:
        return jsonify({"Message": "Error"}), 404
    
    return render_template("detailed_news.html", news=news)

@main_routes.route("/wall")
def wall():
    news_list = get_all_news()
    return render_template("index.html", news=news_list, page_type="wall")

@main_routes.route("/team_search")
def team_search():
    return render_template("index.html", page_type="team_search")


@main_routes.route('/save-image', methods=['POST'])
@login_required
def save_image():
    if request.method == "POST":
        data = request.get_json()
        title = data.get('title')
        short_description = data.get('shortDescription')
        full_description = data.get('fullDescription')
        type = data.get('type')
        interval = data.get('input')
        file = ""
        user_id = session.get("_user_id")
        if data:
            image = data.get('dataURL')
            file = save_file(image)

        if not user_id:
            return jsonify({"message": "not authorize"}), 401

        add_to_database2(title, short_description, full_description, file, interval, user_id, type)

        return jsonify({"message": "ok"}), 200
    return jsonify({"message": "ERROR"}), 404