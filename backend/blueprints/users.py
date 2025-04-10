from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from methods import find_news_by_user_id, safe, find_user_by_user_id, patch_profile_method
from flask_pydantic import validate
from schemas import PatchUserRequest

user_routes = Blueprint('user', __name__)


@user_routes.route('/HomePage', methods=['GET'])
@safe("blueprints/users.py | get_posts_by_user_id")
@jwt_required()
def get_posts_by_user_id():
    user_id = get_jwt_identity()
    posts = find_news_by_user_id(user_id)
    return jsonify(posts.as_dict()), 200


@user_routes.route('/profile', methods=['GET'])
@safe("blueprints/users.py | profile")
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    user = find_user_by_user_id(user_id)
    if user is None:
        return jsonify({'error': 'user not found'}), 404

    return jsonify(user.as_dict()), 200


@user_routes.route('/profile', methods=['PATCH'])
@safe("blueprints/users.py | patch_profile")
@jwt_required()
@validate()
def patch_profile(body: PatchUserRequest):
    user_id = get_jwt_identity()

    user = find_user_by_user_id(user_id)
    if user is None:
        return jsonify({'error': 'user not found'}), 404

    user = patch_profile_method(user, body)

    return jsonify(user.as_dict()), 200

