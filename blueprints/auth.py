from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required
from manage import *
from methods import *
import datetime
from schemas import *
from flask_pydantic import validate

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
@safe
def login():
    login_field = request.json.get('username')
    password = request.json.get('password')
    user = find_user_by_login(login_field)

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Неверный логин или пароль'}), 401

    access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(days=30),
                                       additional_claims={"user_id": user.id, "is_admin": user.is_admin})
    return jsonify({'access_token': access_token, 'is_admin': user.is_admin}), 200


@auth.route('/logout', methods=['POST'])
@safe
@jwt_required()
def logout():
    return jsonify({'message': 'Вы вышли из системы'}), 200


@auth.route('/user/register', methods=['POST'])
@safe
@validate()
def register_user(body: UserRegisterRequest):
    if find_user_by_login(body.login):
        return jsonify({'message': 'Этот логин уже занят'}), 400

    hashed_password = generate_password_hash(body.password)
    create_user(body.name, body.surname, body.school, body.corpus, False, body.login, hashed_password)

    return jsonify({'message': 'Регистрация успешна'}), 201


@auth.route('/admin/register', methods=['POST'])
@safe
@validate()
def register_admin(body: UserRegisterRequest):
    if find_user_by_login(body.login):
        return jsonify({'message': 'Этот логин уже занят'}), 400

    hashed_password = generate_password_hash(body.password)
    create_user(body.name, body.surname, body.school, body.corpus, True, body.login, hashed_password)

    return jsonify({'message': 'Регистрация успешна'}), 201

