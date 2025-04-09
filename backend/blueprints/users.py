from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from methods import find_news_by_user_id, safe, find_user_by_user_id

user_routes = Blueprint('user', __name__)


@user_routes.route('/HomePage')
@safe("blueprints/users.py | dashboard")
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    walls = find_news_by_user_id(user_id)
    return jsonify(walls.as_dict()), 200


@user_routes.route('/profile', methods=['GET'])
@safe("blueprints/users.py | profile")
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    user = find_user_by_user_id(user_id)
    if user is None:
        return jsonify({'error': 'user not found'}), 404

    return jsonify(user.as_dict()), 200

