from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from methods import *
from flask_pydantic import validate

from schemas import PatchUserRequest, SubscribeRequest
from methods import UserService

user_routes = Blueprint('user', __name__)


@user_routes.route('/HomePage', methods=['GET'])
@safe("blueprints/users.py | get_posts_by_user_id")
@jwt_required()
def get_posts_by_user_id():
    user_id = get_jwt_identity()
    posts = PostService.get_news_by_user_id(user_id)

    return jsonify({"user_posts": posts}), 200


@user_routes.route('/profile', methods=['GET'])
@safe("blueprints/users.py | profile")
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = UserService.get_user_by_user_id(user_id)
    return jsonify(user.as_dict()), 200


@user_routes.route('/profile', methods=['PATCH'])
@safe("blueprints/users.py | patch_profile")
@jwt_required()
@validate()
def patch_profile(body: PatchUserRequest):
    user_id = get_jwt_identity()
    user = UserService.get_user_by_user_id(user_id)
    user = UserService.patch_profile(user, body)

    return jsonify(user.as_dict()), 200


@user_routes.route("/my-likes", methods=["GET"])
@safe("blueprints/users.py | my_likes")
@jwt_required()
def my_likes():
    user_id = get_jwt_identity()

    liked_post_ids = db.session.query(UsersHistory.post_id).filter_by(user_id=user_id, liked=True).all()
    liked_post_ids_list = [str(post_id) for (post_id,) in liked_post_ids]

    return jsonify({"posts_liked_by_user": liked_post_ids_list}), 200


@user_routes.route("/<post_id>/send/to/moderation", methods=["POST"])
@safe("blueprints/users.py | send_to_moderation")
@jwt_required()
@check_user_access
def send_to_moderation(post_id, only_user=True):
    PostService.is_valid_uuid(post_id)
    post = PostService.get_news_by_post_id(post_id)

    if post.status != "pending":
        post.status = "pending"
        db.session.commit()

    return jsonify({}), 204


@user_routes.route('/subscribe', methods=['POST'])
@safe("blueprints/subscribe.py | subscribe")
@jwt_required()
@validate()
def subscribe(body: SubscribeRequest):
    user_id = get_jwt_identity()

    SubscribeService.remove_existing_subscription(user_id)
    valid_tags = SubscribeService.validate_tags(body.tags)
    valid_authors = SubscribeService.validate_authors(body.authors)

    SubscribeService.create_subscription(user_id, valid_tags, valid_authors)

    return jsonify({"message": "subscription was successful"}), 200


@user_routes.route('/subscribe', methods=['GET'])
@safe("blueprints/subscribe.py | get_subscribe")
@jwt_required()
def get_subscribe():
    user_id = get_jwt_identity()
    subscribe = SubscribeService.get_subscription(user_id)

    return jsonify({"subscriptions": subscribe.as_dict()}), 200


@user_routes.route('/drafts', methods=['GET'])
@safe("blueprints/users.py | drafts")
@jwt_required()
def drafts():
    user_id = get_jwt_identity()
    posts = News.query.filter_by(status="draft", user_id=user_id).all()
    posts = [post.as_dict() for post in posts]
    return jsonify({"drafts": posts}), 200
