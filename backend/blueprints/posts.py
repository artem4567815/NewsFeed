from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from methods import *
from flask_pydantic import validate
from schemas import *
from werkzeug.exceptions import Forbidden


posts = Blueprint('posts', __name__)


@posts.route("", methods=["GET"])
@safe("blueprints/posts.py | category_posts")
@validate()
def category_posts(query: QueryRequest):
    posts_list = get_news_by_query(query)
    posts_list = [news.as_dict() for news in posts_list]
    posts_list = sorted(posts_list, key=lambda news: news["created_at"], reverse=True)
    posts_count = len(posts_list)
    return jsonify({"posts": posts_list, "posts_count":posts_count}), 200


@posts.route("/<post_id>", methods=["GET"])
@safe("blueprints/posts.py | detailed_posts")
def detailed_posts(post_id):
    if not is_valid_uuid(post_id):
        raise BadRequest("post_id not valid")
    post = find_news_by_id(post_id)
    if not post:
        return jsonify({"Message": "Новость не найдена"}), 404

    # post.views += 1
    # db.session.commit()

    return jsonify(post.as_dict()), 200


@posts.route("/<post_id>", methods=["PATCH"])
@safe("blueprints/posts.py | patch_posts")
@jwt_required()
@validate()
def patch_posts(post_id, body: PatchPostRequest):
    if not is_valid_uuid(post_id):
        raise BadRequest("post_id not valid")
    post = find_news_by_id(post_id)
    user_id = get_jwt_identity()

    if not post:
        return jsonify({"Message": "Новость не найдена"}), 404

    if str(post.user_id) != str(user_id):
        raise Forbidden("not allowed")

    post = patch_post_method(post, body)
    return jsonify(post.as_dict()), 200


@posts.route("/<post_id>", methods=["DELETE"])
@safe("blueprints/posts.py | delete_posts")
@jwt_required()
def delete_posts(post_id):
    if not is_valid_uuid(post_id):
        raise BadRequest("post_id not valid")

    post = find_news_by_id(post_id)
    user_id = get_jwt_identity()

    if not post:
        return jsonify({"Message": "Новость не найдена"}), 404

    if str(post.user_id) != str(user_id):
        raise Forbidden("not allowed")

    db.session.delete(post)
    db.session.commit()
    return jsonify({}), 204


@posts.route("/<post_id>/like", methods=["POST"])
@safe("blueprints/posts.py | like_posts")
@jwt_required()
def like_posts(post_id):
    if not is_valid_uuid(post_id):
        raise BadRequest("post_id not valid")

    post = find_news_by_id(post_id)
    user_id = get_jwt_identity()

    if not post:
        return jsonify({"Message": "Новость не найдена"}), 404


    like_post_method(post, user_id)
    return jsonify({}), 204


@posts.route("/<post_id>/unlike", methods=["DELETE"])
@safe("blueprints/posts.py | unlike_posts")
@jwt_required()
def unlike_posts(post_id):
    if not is_valid_uuid(post_id):
        raise BadRequest("post_id not valid")

    post = find_news_by_id(post_id)
    user_id = get_jwt_identity()

    if not post:
        return jsonify({"Message": "Новость не найдена"}), 404


    unlike_post_method(post, user_id)
    return jsonify({}), 204


@posts.route("/<post_id>/view", methods=["POST"])
@safe("blueprints/posts.py | view_posts")
def view_posts(post_id):
    if not is_valid_uuid(post_id):
        raise BadRequest("post_id not valid")

    post = find_news_by_id(post_id)

    if not post:
        return jsonify({"Message": "Новость не найдена"}), 404

    post.views += 1
    db.session.commit()

    return jsonify({}), 204


@posts.route("/<post_id>/join", methods=["POST"])
@safe("blueprints/posts.py | join_to_posts")
@jwt_required()
def join_to_posts(post_id):
    if not is_valid_uuid(post_id):
        raise BadRequest("post_id not valid")

    post = find_news_by_id(post_id)
    user_id = get_jwt_identity()

    if not post:
        return jsonify({"Message": "Новость не найдена"}), 404

    current_timestamp = int(datetime.now().timestamp())
    if post.type == "news":
        if current_timestamp > post.end_date:
            raise BadRequest("Ты уже не можешь присоединиться, событие прошло")

        join_post_method(post, user_id)
    else:
        raise BadRequest("post not is news")
    return jsonify({}), 204


@posts.route('/create/post', methods=['POST'])
@safe("blueprints/admin.py | save_news")
@jwt_required()
@validate()
def save_news(body: CreateNewsRequest):
    file = save_base64_image(body.post_img)
    user_id = get_jwt_identity()
    access = get_jwt()['is_admin']

    if access:
        news = create_news(body.title, body.short_content, body.content, file,
                           body.start_date, body.end_date, user_id, body.type, body.tags)
    else:
        news = create_news(body.title, body.short_content, body.content, file,
                           body.start_date, body.end_date, user_id, body.type, body.tags, "draft")

    return jsonify(news.as_dict()), 201


@posts.route('/create/wallpapers', methods=['POST'])
@safe("blueprints/posts.py | save_wallpapers")
@jwt_required()
@validate()
def save_wallpapers(body: CreateNewsRequest):
    file = save_base64_image(body.post_img)
    user_id = get_jwt_identity()

    news = create_news(body.title, body.short_content, body.content, file, body.start_date, body.end_date,
                       user_id, body.type, body.tags, "draft")

    return jsonify(news.as_dict()), 201
