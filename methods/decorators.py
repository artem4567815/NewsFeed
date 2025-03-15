from functools import wraps
from flask import redirect, flash, jsonify
from werkzeug.exceptions import *
from flask_jwt_extended import get_jwt_identity, get_jwt


def check_jwt_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = get_jwt()
        if current_user["is_admin"]:
            return func(*args, **kwargs)
        raise Forbidden("cannot access admin")

    wrapper.__name__ = func.__name__
    return wrapper


def safe(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(f"Исключение: {type(e)} - {e}")
            return jsonify({"status": "error", "message": "Ошибка в данных запроса."}), 400
        except UnsupportedMediaType as e:
            return jsonify({"status": "error", "message": "Ошибка в данных запроса."}), 400
        except NotFound as e:
            print(f"Исключение: {type(e)} - {e}")
            return jsonify({"reason": "object not found"}), 404
        except Forbidden as e:
            print(f"Исключение: {type(e)} - {e}")
            return jsonify({"reason": "error"}), 403
        except Exception as e:
            print(f"Исключение: {type(e)} - {e}")
            return jsonify({"status": "error", "message": "Ошибка сервера"}), 500

    wrapper.__name__ = func.__name__
    return wrapper