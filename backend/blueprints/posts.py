from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from methods import *
from flask_pydantic import validate
from schemas import *


posts = Blueprint('posts', __name__)


@posts.route("", methods=["GET"])
@safe("blueprints/posts.py | category_posts")
def category_posts():
    query = request.args.get("type", "news")
    posts_list = get_news_for_category(query)
    posts_list = [news.as_dict() for news in posts_list]
    return jsonify(posts_list), 200


@posts.route("/post/<int:post_id>", methods=["GET"])
@safe("blueprints/posts.py | detailed_news")
def detailed_news(post_id):
    news = find_news_by_id(post_id)
    if not news:
        return jsonify({"Message": "Новость не найдена"}), 404
    return jsonify(news.as_dict()), 200


@posts.route('/create/wallpapers', methods=['POST'])
@safe("blueprints/posts.py | save_wallpapers")
@jwt_required()
@validate()
def save_wallpapers(body: CreateNewsRequest):
    file = save_base64_image(body.post_img)
    user_id = get_jwt_identity()

    news = create_news(body.title, body.short_content, body.content, file, body.start_date, body.end_date,
                       user_id, body.type, "draft")

    return jsonify(news.as_dict()), 200
