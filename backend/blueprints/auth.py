from flask import Blueprint, make_response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from methods import *
from schemas import *
from flask_pydantic import validate
from werkzeug.security import check_password_hash
from werkzeug.exceptions import Unauthorized

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
@safe("blueprints/auth.py | login")
@validate()
def login(body: LoginRequest):
    user = UserService.get_user_by_login(body.login)

    if not user or not check_password_hash(user.password_hash, body.password):
        raise Unauthorized()

    access_token = create_access_token(identity=user.user_id,
                                       additional_claims={"user_id": user.user_id, "is_admin": user.is_admin})

    refresh_token = create_refresh_token(identity=user.user_id,
                                         additional_claims={"user_id": user.user_id, "is_admin": user.is_admin})

    response = make_response(jsonify({"access_token": access_token, "is_admin": user.is_admin}))
    response.set_cookie(
        "refresh_token_cookie",
        refresh_token,
        httponly=True,
        secure=False,
        path="/",
    )

    return response, 200


@auth.route("/refresh", methods=["POST"])
@safe("blueprints/auth.py | refresh")
@jwt_required(refresh=True)
def refresh():
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
    if UserService.get_user_by_login(body.login):
        raise Conflict('User already exists')

    new_user = UserService.create_user(body, False)

    return jsonify(new_user.as_dict()), 201


@auth.route('/register/admin', methods=['POST'])
@safe("blueprints/auth.py | register_admin")
@validate()
def register_admin(body: UserRegisterRequest):
    if UserService.get_user_by_login(body.login):
        raise Conflict('User already exists')

    new_user = UserService.create_user(body, True)

    return jsonify(new_user.as_dict()), 201

