import jwt
from flask import Flask
from flask_jwt_extended import create_access_token, JWTManager, create_refresh_token
import uuid
from datetime import timedelta
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import backend.config as config

JWT_SECRET = config.JWT_SECRET

def get_refresh_token(response, cookie_name):
    cookie = response.cookies.get(cookie_name)
    if not cookie:
        raise ValueError(f"Cookie {cookie_name} not found in response")

    try:
        decoded = jwt.decode(
            cookie,
            options={"verify_signature": False},
            algorithms=["HS256"]
        )
        csrf_token = decoded.get("csrf")
    except Exception as e:
        return {"JWT decoding failed": str(e)}

    return {"refresh_token": cookie,
            "csrf_token": csrf_token}


def create_token_with_invalid_token(response):
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = JWT_SECRET
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)

    non_user = str(uuid.uuid4())
    jwt = JWTManager(app)

    with app.app_context():
        access_token = create_access_token(identity=non_user,
                                           additional_claims={"user_id": non_user, "is_admin": False})

        return {"access_token_invalid": access_token}

def create_expired_access_token(response):
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = JWT_SECRET
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=-1)

    jwtt = JWTManager(app)

    non_user = str(uuid.uuid4())

    with app.app_context():
        access = create_access_token(identity=non_user,
                                             additional_claims={"user_id": non_user, "is_admin": False})

        return {"access_exp": access}

def create_expired_refresh_token(response):
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = JWT_SECRET
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']

    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=-1)

    jwtt = JWTManager(app)

    non_user = str(uuid.uuid4())

    with app.app_context():
        refresh_token = create_refresh_token(identity=non_user,
                                             additional_claims={"user_id": non_user, "is_admin": False})

        try:
            decoded = jwt.decode(
                refresh_token,
                options={"verify_signature": False},
                algorithms=["HS256"]
            )
            csrf_token = decoded.get("csrf")
        except Exception as e:
            return {"JWT decoding failed": str(e)}

        return {"refresh_token2": refresh_token, "csrf_token2": csrf_token}