from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from methods import *
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


@user_routes.route("/my-likes", methods=["GET"])
@safe("blueprints/users.py | my_likes")
@jwt_required()
def my_likes():
    user_id = get_jwt_identity()

    liked_post_ids = db.session.query(UsersHistory.post_id).filter_by(
        user_id=user_id, liked=True
    ).all()

    posts = []
    for post_id in liked_post_ids:
        posts.append(News.query.filter_by(post_id=post_id).first())

    return jsonify({"likes": posts}), 200


@user_routes.route("/<post_id>/send/to/moderation", methods=["POST"])
@safe("blueprints/users.py | send_to_moderation")
@jwt_required()
def send_to_moderation(post_id):
    if not is_valid_uuid(post_id):
        raise BadRequest("post_id not valid")

    user_id = get_jwt_identity()
    post = find_news_by_id(post_id)

    if not post:
        return jsonify({"Message": "Новость не найдена"}), 404

    if str(post.user_id) != str(user_id):
        raise Forbidden("not allowed")

    if post.status != "pending":
        post.status = "pending"
        db.session.commit()

    return jsonify({}), 204




