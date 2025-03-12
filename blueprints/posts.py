from flask import Blueprint, render_template, request, session
from flask_login import login_required
from methods import *

posts = Blueprint('posts', __name__)


@posts.route("/news")
@safe
def all_news():
    news_list = get_all_news()
    return render_template("index.html", news=news_list, page_type="news", session=session)


@posts.route("/news/<int:post_id>")
@safe
def detailed_news(post_id):
    news = find_news_by_id(post_id)
    if not news:
        return jsonify({"Message": "Error"}), 404

    return render_template("detailed_news.html", news=news)


@posts.route("/wall")
@safe
def wall():
    news_list = get_all_news()
    return render_template("index.html", news=news_list, page_type="wall", session=session)


@posts.route("/team_search")
@safe
def team_search():
    news_list = get_all_news()
    return render_template("index.html", news=news_list, page_type="team_search", session=session)


@posts.route('/save-image', methods=['POST'])
@safe
@login_required
def save_image():
    if request.method == "POST":
        data = request.get_json()

        if data:
            short_description = data.get('shortDescription')
            full_description = data.get('fullDescription')
            title = data.get('title')
            type_field = data.get('type')
            interval = data.get('input')
            image = data.get('dataURL')
            file = save_file(image)


            user_id = session.get("_user_id")

            if not user_id:
                return jsonify({"message": "not authorize"}), 401

            add_to_database(title, short_description, full_description, file, interval, user_id, type_field)

        else: return jsonify({"message": "data not found"}), 404

        return jsonify({"message": "ok"}), 200

    return jsonify({"message": "ERROR"}), 404

