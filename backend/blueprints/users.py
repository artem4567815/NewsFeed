from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from methods import *
from flask_pydantic import validate

from schemas import PatchUserRequest, SubscribeRequest
from models import Subscription

user_routes = Blueprint('user', __name__)


@user_routes.route('/HomePage', methods=['GET'])
@safe("blueprints/users.py | get_posts_by_user_id")
@jwt_required()
def get_posts_by_user_id():
    user_id = get_jwt_identity()
    posts = find_news_by_user_id(user_id)
    posts = [post.as_dict() for post in posts]
    return jsonify({"user_posts": posts}), 200


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


@user_routes.route('/subscribe', methods=['POST'])
@safe("blueprints/subscribe.py | subscribe")
@jwt_required()
@validate()
def subscribe(body: SubscribeRequest):
    user_id = get_jwt_identity()
    subscriptions = Subscription.query.filter_by(user_id=user_id).first()

    if subscriptions is not None:
        db.session.delete(subscriptions)

    found_authors = None

    if body.tags:
        valid_tags = db.session.query(db.func.unnest(News.tags)).distinct().all()
        valid_tags = [tag[0] for tag in valid_tags]
        invalid_tags = [tag for tag in body.tags if tag not in valid_tags]
        if invalid_tags:
            raise BadRequest(f"Invalid tags: {', '.join(invalid_tags)}")

    if body.authors:
        authors = Users.query.filter(Users.login.in_(body.authors)).all()
        found_authors = [author.login for author in authors]
        missing_authors = [a for a in body.authors if a not in found_authors]

        if missing_authors:
            raise BadRequest(f"Authors not found: {', '.join(missing_authors)}")

    subscription = Subscription(
        user_id=user_id,
        tags=body.tags,
        authors=found_authors
    )

    db.session.add(subscription)
    db.session.commit()

    return jsonify({"message": "subscription was successful"}), 200


@user_routes.route('/subscribe', methods=['GET'])
@safe("blueprints/subscribe.py | get_subscribe")
@jwt_required()
def get_subscribe():
    user_id = get_jwt_identity()
    subscribe = Subscription.query.filter_by(user_id=user_id).first()

    if not subscribe:
        return jsonify({"message": "subscription was not found"}), 404

    out = {}
    if subscribe.authors:
        out["authors"] = subscribe.authors
    if subscribe.tags:
        out["tags"] = subscribe.tags
    print(out)
    return jsonify({"subscriptions": out}), 200
