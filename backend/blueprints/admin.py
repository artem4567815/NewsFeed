from flask import Blueprint, request
from methods import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_pydantic import validate
from schemas import *
from models import News

admin_routes = Blueprint('admin', __name__)


@admin_routes.route('/create/post', methods=['POST'])
@safe("blueprints/admin.py | save_news")
@jwt_required()
@check_jwt_access
@validate()
def save_news(body: CreateNewsRequest):
    file = save_base64_image(body.post_img)
    user_id = get_jwt_identity()

    news = create_news(body.title, body.short_content, body.content, file,
                       body.start_date, body.end_date, user_id, body.type, body.tags)

    return jsonify(news.as_dict()), 201


@admin_routes.route('/moderation', methods=['GET'])
@safe("blueprints/admin.py | moderation")
@jwt_required()
@check_jwt_access
def moderation():
    posts = News.query.filter_by(status="pending").all()
    posts = [post.as_dict() for post in posts]
    return jsonify(posts), 200


@admin_routes.route('/moderation/access', methods=['POST'])
@safe("blueprints/admin.py | moderation_access")
@jwt_required()
@check_jwt_access
def moderation_access():
    post_id = request.args.get('post_id')

    post = News.query.filter_by(news_id=post_id).first()
    post.status = "approved"

    db.session.commit()
    return jsonify({"message": "moderation approve"}), 200
