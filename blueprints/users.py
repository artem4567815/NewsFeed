from flask import Blueprint, render_template, request, redirect, flash, session, jsonify
from werkzeug.security import generate_password_hash
from models import db, Users, Credentials
from manage import *
from methods import user_required

user_routes = Blueprint('users', __name__)

@user_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        school = request.form.get('school')
        corpus = request.form.get('school')
        login = request.form.get('login')
        password = request.form.get('password')

        if Credentials.query.filter_by(login=login).first():
            flash('Этот логин уже занят. Попробуйте другой.', 'error')
            return redirect('register')

        new_user = Users(name=name, surname=surname, school=school, corpus=corpus, is_admin=False)
        db.session.add(new_user)
        db.session.commit()

        password_hash = generate_password_hash(password)
        credentials = Credentials(user_id=new_user.id, login=login, password_hash=password_hash)
        db.session.add(credentials)
        db.session.commit()

        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect('/routes/login')

    return render_template('register.html')


@user_routes.route('/HomePage')
@login_required
@user_required
def dashboard():
    return jsonify({"MESSAGE": "OK"}), 200

