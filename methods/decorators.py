from functools import wraps
from flask import redirect, flash, jsonify
from flask_login import current_user
from werkzeug.exceptions import *


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('У вас нет доступа к этой странице.', 'error')
            return redirect('/users/HomePage')
        return f(*args, **kwargs)
    return decorated_function


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin:
            flash('У вас нет доступа к этой странице.', 'error')
            return redirect('/admin/HomePage')
        return f(*args, **kwargs)
    return decorated_function


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