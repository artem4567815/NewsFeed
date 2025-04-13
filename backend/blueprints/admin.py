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


@admin_routes.route('/statistics', methods=['GET'])
@safe("blueprints/admin.py | statistics")
@jwt_required()
@check_jwt_access
def statistics():
    user_id = get_jwt_identity()
    total_posts = News.query.filter_by(status="published").count()
    total_posts_by_current_author = News.query.filter_by(status="published", user_id=user_id).count()
    active_user = get_most_three_active_user()
    print(active_user)
    avg_conversion = get_expired_posts_avg_conversion(user_id)


    return jsonify({
        "total_posts": total_posts,
        "posts_by_this_author": total_posts_by_current_author,
        "most_three_active_user": active_user,
        "avg_conversion": avg_conversion,
    }), 200


@admin_routes.route('/statistics/<post_id>', methods=['GET'])
@safe("blueprints/admin.py | statistics_for_post")
@jwt_required()
@check_jwt_access
def statistics_for_post(post_id):
    if not is_valid_uuid(post_id):
        return BadRequest("Invalid post id")
    post = News.query.filter_by(status="published", post_id=post_id).first()

    if post is None:
        return NotFound("post not found")

    return jsonify(get_statistics_by_posts_id(post_id)), 200
