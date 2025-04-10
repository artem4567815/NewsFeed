from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from methods import *
from flask_pydantic import validate
from schemas import *


posts = Blueprint('posts', __name__)


@posts.route("", methods=["GET"])
@safe("blueprints/posts.py | category_posts")
@validate()
def category_posts(query: QueryRequest):
    posts_list = get_news_by_query(query)
    posts_list = [news.as_dict() for news in posts_list]
    return jsonify({"posts": posts_list}), 200


@posts.route("/post/<post_id>", methods=["GET"])
@safe("blueprints/posts.py | detailed_news")
def detailed_news(post_id):
    news = find_news_by_id(post_id)
    if not news:
        return jsonify({"Message": "Новость не найдена"}), 404
    return jsonify(news.as_dict()), 200


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
