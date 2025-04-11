from flask import Blueprint, request
from methods import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import News
from schemas import QueryRequest
from flask_pydantic import validate

admin_routes = Blueprint('admin', __name__)


@admin_routes.route('/moderation', methods=['GET'])
@safe("blueprints/admin.py | moderation")
@jwt_required()
@check_jwt_access
@validate()
def moderation(query: QueryRequest):
    posts = News.query.filter_by(status="pending").limit(query.limit).offset(query.offset).all()
    posts = [post.as_dict() for post in posts]
    return jsonify({"wall_newspapers": posts}), 200


@admin_routes.route('/moderation/<post_id>/apply', methods=['POST'])
@safe("blueprints/admin.py | moderation_apply")
@jwt_required()
@check_jwt_access
def moderation_apply(post_id):
    if not is_valid_uuid(post_id):
        return BadRequest("Invalid post id")

    post = News.query.filter_by(post_id=post_id).first()

    if not post:
        return jsonify({"Message": "Новость не найдена"}), 404

    post.status = "published"
    db.session.commit()

    return jsonify({}), 204


@admin_routes.route('/moderation/<post_id>/reject', methods=['POST'])
@safe("blueprints/admin.py | moderation_reject")
@jwt_required()
@check_jwt_access
def moderation_reject(post_id):
    if not is_valid_uuid(post_id):
        return BadRequest("Invalid post id")

    reason = request.json.get("reason", None)
    if reason is None:
        raise BadRequest("Invalid reason")

    post = News.query.filter_by(post_id=post_id).first()

    if not post:
        return jsonify({"Message": "Новость не найдена"}), 404

    post.status = "rejected"
    db.session.commit()

    return jsonify({"reason": reason}), 200


# @admin_routes.route('/statistics', methods=['GET'])
# @safe("blueprints/admin.py | statistics")
# @jwt_required()
# @check_jwt_access
# def statistics():
#     user_id = get_jwt_identity()
#     stats = UsersHistory.query.filter_by(user_id=user_id).all()
#     total_posts = News.query.filter_by(status="published").count()
#     active_user = get_most_active_user()
#     user_total_posts = News.query.filter_by(status="published", user_id=user_id).count()
#     user_total_views = db.session.query(UsersHistory).filter_by(post_id=post_id, viewed=True).count()
#     user_total_likes = db.session.query(UsersHistory).filter_by(post_id=post_id, liked=True).count()
#     user_total_joins = db.session.query(UsersHistory).filter_by(post_id=post_id, joined=True).count()
#
#     user_total_conversion = round(joins / views, 4) if views else 0.0
#
#
#     posts = News.query.filter_by(status="pending").limit(query.limit).offset(query.offset).all()
#     posts = [post.as_dict() for post in posts]
#     return jsonify({"wall_newspapers": posts}), 200