from flask import Blueprint, request, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, set_refresh_cookies
from methods import *
from schemas import *
from flask_pydantic import validate
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
@safe("blueprints/auth.py | login")
def login():
    login_field = request.json.get('login', None)
    password = request.json.get('password', None)

    if login_field is None or password is None:
        raise BadRequest('login and password are required')

    user = find_user_by_login(login_field)

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Неверный логин или пароль'}), 401

    access_token = create_access_token(identity=user.user_id,
                                       additional_claims={"user_id": user.user_id, "is_admin": user.is_admin})

    refresh_token = create_refresh_token(identity=user.user_id, additional_claims={"user_id": user.user_id, "is_admin": user.is_admin})

    response = make_response(jsonify({"access_token": access_token, "is_admin": user.is_admin}))
    response.set_cookie(
        "refresh_token_cookie",
        refresh_token,
        httponly=True,
        secure=False,  # False для http в разработке, True для production
        path="/",      # Важно указать путь
    )

    return response, 200

@auth.route('/debug-cookies', methods=['GET'])
def debug_cookies():
    print(request.cookies)
    return jsonify(dict(request.cookies))

@auth.route("/refresh", methods=["POST"])
@safe("blueprints/auth.py | refresh")
@jwt_required(refresh=True)
def refresh():
    print("Cookies received:")
    print(request.cookies)
    for key, value in request.cookies.items():
        print(112)
        print(f"{key}: {value}")
    identity = get_jwt_identity()
    add = get_jwt()
    claims = {"user_id": add["user_id"], "is_admin": add["is_admin"]}
    new_access_token = create_access_token(identity=identity,
                                           additional_claims=claims)

    return jsonify({"access_token": new_access_token})


@auth.route('/register/client', methods=['POST'])
@safe("blueprints/auth.py | register_user")
@validate()
def register_user(body: UserRegisterRequest):
    if find_user_by_login(body.login):
        return jsonify({'message': 'Этот логин уже занят'}), 409

    new_user = create_user(body.name, body.surname, body.school, body.building, False,
                           body.login, body.password, body.avatar_url)

    return jsonify(new_user.as_dict()), 201


@auth.route('/register/admin', methods=['POST'])
@safe("blueprints/auth.py | register_admin")
@validate()
def register_admin(body: UserRegisterRequest):
    if find_user_by_login(body.login):
        return jsonify({'message': 'Этот логин уже занят'}), 409

    new_user = create_user(body.name, body.surname, body.school, body.building, True, body.login,
                           body.password, body.avatar_url)

    return jsonify(new_user.as_dict()), 201

