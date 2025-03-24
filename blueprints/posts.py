from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from methods import *
from flask_pydantic import validate
from schemas import *
from manage import r
from datetime import timedelta
import json
from config import USER_LIST_KEY

posts = Blueprint('posts', __name__)


@posts.route("", methods=["GET"])
@safe("blueprints/posts.py | category_posts")
def category_posts():
    query = request.args.get("type", "news")
    posts_list = get_news_for_category(query)
    posts_list = [news.as_dict() for news in posts_list]
    print(posts_list)
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
    user_id = get_jwt_identity()
    key = f"user:{user_id}"

    r.setex(key, timedelta(days=30), json.dumps(dict(body)))
    r.sadd(USER_LIST_KEY, user_id)

    return jsonify({"message": "Data saved successfully"}), 201
