from flask import Blueprint, request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from methods import *
import datetime
from schemas import *
from flask_pydantic import validate
from werkzeug.security import generate_password_hash, check_password_hash
from config import APP_SECRET

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
@safe("blueprints/auth.py | login")
def login():
    login_field = request.json.get('username')
    password = request.json.get('password')
    user = find_user_by_login(login_field)
    print(user.user_id)
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Неверный логин или пароль'}), 401

    access_token = create_access_token(identity=user.user_id, expires_delta=datetime.timedelta(days=30),
                                       additional_claims={"user_id": user.user_id, "is_admin": user.is_admin})

    refresh_token = create_refresh_token(identity=user.user_id, additional_claims={"user_id": user.user_id, "is_admin": user.is_admin})

    response = make_response(jsonify({"access_token": access_token, "is_admin": user.is_admin}))
    response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Strict", secure=True)

    return response, 200


@auth.route("/refresh", methods=["POST"])
@safe("blueprints/auth.py | refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    add = get_jwt()
    new_access_token = create_access_token(identity=identity, expires_delta=datetime.timedelta(days=30),
                                           additional_claims=add)

    return jsonify({"access_token": new_access_token})


@auth.route('/register/client', methods=['POST'])
@safe("blueprints/auth.py | register_user")
@validate()
def register_user(body: UserRegisterRequest):
    if find_user_by_login(body.login):
        return jsonify({'message': 'Этот логин уже занят'}), 400

    new_user = create_user(body.name, body.surname, body.school, body.building, False, body.login, body.password)

    return jsonify(new_user.as_dict()), 201


@auth.route('/admin/register', methods=['POST'])
@safe("blueprints/auth.py | register_admin")
@validate()
def register_admin(body: UserRegisterRequest):
    if find_user_by_login(body.login):
        return jsonify({'message': 'Этот логин уже занят'}), 400

    new_user = create_user(body.name, body.surname, body.school, body.building, True, body.login, body.password)

    return jsonify(new_user.as_dict()), 201

