from functools import wraps
import jwt
from flask import jsonify
from werkzeug.exceptions import *
from flask_jwt_extended import get_jwt
from flask_jwt_extended.exceptions import JWTDecodeError
from flask_pydantic import ValidationError
from manage import logger

def get_first_error(e):
    errors = []

    if e.form_params:
        errors += e.form_params

    if e.query_params:
        errors += e.query_params

    if e.body_params:
        errors += e.body_params

    if e.path_params:
        errors += e.path_params

    error = errors[0]
    return f"{error['msg']}: {error['loc']}"


def safe(func_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValidationError as e:
                logger.log("error", f"{func_name} | Type of error: {type(e)} - error: {get_first_error(e)}")
                return jsonify({"Validation error": f"{get_first_error(e)}"}), 400
            except ValueError as e:
                logger.log("error", f"{func_name} | Type of error: {type(e)} - error: {str(e)}")
                return jsonify({"status": "error", "message": "Ошибка в данных запроса." + str(e)}), 400
            except UnsupportedMediaType as e:
                logger.log("error", f"{func_name} | Type of error: {type(e)} - error: {e}")
                return jsonify({"status": "error", "message": "Ошибка в данных запроса."}), 400
            except NotFound as e:
                logger.log("error", f"{func_name} | Type of error: {type(e)} - error: {e}")
                return jsonify({"reason": "object not found"}), 404
            except Forbidden as e:
                logger.log("error", f"{func_name} | Type of error: {type(e)} - error: {e}")
                return jsonify({"reason": "error"}), 403
            except JWTDecodeError as e:
                logger.log("error", f"{func_name} | Type of error: {type(e)} - error: {e}")
                return jsonify({"reason": "Incorrect token"}), 403
            except jwt.exceptions.InvalidSignatureError as e:
                logger.log("error", f"{func_name} | Type of error: {type(e)} - error: {e}")
                return jsonify({"reason": "Signature verification failed"}), 401
            except jwt.ExpiredSignatureError as e:
                logger.log("error", f"{func_name} | Type of error: {type(e)} - error: {e}")
                return jsonify({"error": "Token expired"}), 401
            except jwt.InvalidTokenError as e:
                logger.log("error", f"{func_name} | Type of error: {type(e)} - error: {e}")
                return jsonify({"error": "Invalid token"}), 401
            except Exception as e:
                logger.log("critical", f"{func_name} | Type of error: {type(e)} - error: {e}")
                return jsonify({"status": "error", "message": "Ошибка сервера"}), 500
        return wrapper
    return decorator

def check_jwt_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = get_jwt()
        print(current_user)
        if current_user["is_admin"]:
            return func(*args, **kwargs)
        raise Forbidden("cannot access admin")

    wrapper.__name__ = func.__name__
    return wrapper
