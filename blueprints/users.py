from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from methods import find_news_by_user_id, safe

user_routes = Blueprint('user', __name__)


@user_routes.route('/HomePage')
@safe("blueprints/users.py | dashboard")
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    walls = find_news_by_user_id(user_id)
    return jsonify(walls.as_dict()), 200
