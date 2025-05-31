from functools import wraps
import jwt
from flask import jsonify
from werkzeug.exceptions import *
from flask_jwt_extended import get_jwt
from flask_jwt_extended.exceptions import JWTDecodeError, NoAuthorizationError
from flask_pydantic import ValidationError
from manage import logger
from methods.posts import PostService
from methods.users import UserService
import inspect


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


ERROR_HANDLERS = {
    ValidationError: {
        "code": 400,
        "message": lambda e: {"Validation error": get_first_error(e)},
        "log_level": "error"
    },
    BadRequest: {
        "code": 400,
        "message": lambda e: {"status": "error", "message": "Ошибка в данных запроса." + str(e)},
        "log_level": "error"
    },
    ValueError: {
        "code": 400,
        "message": lambda e: {"status": "error", "message": "Ошибка в данных запроса." + str(e)},
        "log_level": "error"
    },
    UnsupportedMediaType: {
        "code": 400,
        "message": lambda e: {"status": "error", "message": "Ошибка в данных запроса."},
        "log_level": "error"
    },
    NotFound: {
        "code": 404,
        "message": lambda e: {"reason": "object not found"},
        "log_level": "error"
    },
    Forbidden: {
        "code": 403,
        "message": lambda e: {"reason": "error"},
        "log_level": "error"
    },
    JWTDecodeError: {
        "code": 403,
        "message": lambda e: {"reason": "Incorrect token"},
        "log_level": "error"
    },
    Unauthorized: {
        "code": 401,
        "message": lambda e: {"reason": "Unauthorized"},
        "log_level": "error"
    },
    Conflict: {
        "code": 409,
        "message": lambda e: {"reason": "Conflict data"},
        "log_level": "error"
    },
    NoAuthorizationError: {
        "code": 401,
        "message": lambda e: {
            "reason": "Missing JWT in headers or cookies (Missing Authorization Header; Missing cookie 'refresh_token_cookie')"
        },
        "log_level": "error",
    },
    jwt.InvalidSignatureError: {
        "code": 401,
        "message": lambda e: {"reason": "Signature verification failed"},
        "log_level": "error"
    },
    jwt.ExpiredSignatureError: {
        "code": 401,
        "message": lambda e: {"error": "Token expired"},
        "log_level": "error"
    },
    jwt.InvalidTokenError: {
        "code": 401,
        "message": lambda e: {"error": "Invalid token"},
        "log_level": "error"
    }
}


def safe(func_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                for error_type, config in ERROR_HANDLERS.items():
                    if isinstance(e, error_type):
                        logger.log(config["log_level"], f"{func_name} | Type of error: {type(e)} - error: {e}")
                        return jsonify(config["message"](e)), config["code"]

                logger.log("critical", f"{func_name} | Type of error: {type(e)} - error: {e}")
                return jsonify({"status": "error", "message": "Ошибка сервера"}), 500

        return wrapper

    return decorator


def check_user_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = get_jwt()
        user_id = current_user.get("user_id")
        is_admin = current_user.get("is_admin", False)

        sig = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        arguments = bound_args.arguments

        post_id = kwargs.get("post_id")
        only_user = arguments.get("only_user", False)
        only_admin = arguments.get("only_admin", False)

        if post_id is not None:
            if only_admin and not is_admin:
                raise Forbidden("Access denied: User does not have access")

            PostService.is_valid_uuid(post_id)
            authorized = UserService.is_user_authorized_for_post(user_id, post_id)

            if only_user and not authorized:
                raise Forbidden("Access denied: User does not have access")

            if not only_user and not (authorized or is_admin):
                raise Forbidden("Access denied: User does not have access")

        elif not is_admin:
            raise Forbidden("Access denied: User does not have access")

        return func(*args, **kwargs)

    return wrapper
