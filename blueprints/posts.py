from flask import Blueprint
from flask_jwt_extended import jwt_required
from methods import *
from flask_pydantic import validate
from schemas import *

posts = Blueprint('posts', __name__)


@posts.route("/news", methods=["GET"])
@safe
def all_news():
    news_list = get_all_news()
    news_list = [news.as_dict() for news in news_list]
    return jsonify(news_list), 200


@posts.route("/news/<int:post_id>", methods=["GET"])
@safe
def detailed_news(post_id):
    news = find_news_by_id(post_id)
    if not news:
        return jsonify({"Message": "Новость не найдена"}), 404
    return jsonify(news.as_dict()), 200


# @posts.route("/wall")
# @safe
# def wall():
#     news_list = get_all_news()
#     return render_template("index.html", news=news_list, page_type="wall", session=session)
#

# @posts.route("/team_search")
# @safe
# def team_search():
#     news_list = get_all_news()
#     return render_template("index.html", news=news_list, page_type="team_search", session=session)


@posts.route('/create/news', methods=['POST'])
@safe
@jwt_required()
@check_jwt_access
@validate()
def save_image(body: CreateNewsRequest):
    file = save_base64_image(body.dataURL)
    user_id = get_jwt_identity()
    create_news(body.title, body.short_description, body.full_description, file, body.input, user_id, body.type)

    return jsonify({"message": "ok"}), 200

