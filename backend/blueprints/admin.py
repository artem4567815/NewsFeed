from flask import Blueprint, request
from methods import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import News
from werkzeug.exceptions import NotFound

admin_routes = Blueprint('admin', __name__)


@admin_routes.route('/moderation', methods=['GET'])
@safe("blueprints/admin.py | moderation")
@jwt_required()
@check_user_access
def moderation(only_admin=True):
    posts = PostService.get_all_news_by_status("pending")
    print(posts)
    return jsonify({"wall_newspapers": posts}), 200


@admin_routes.route('/moderation/<post_id>/apply', methods=['POST'])
@safe("blueprints/admin.py | moderation_apply")
@jwt_required()
@check_user_access
def moderation_apply(post_id, only_admin=True):
    PostService.is_valid_uuid(post_id)
    PostService.apply(post_id)

    return jsonify({}), 204


@admin_routes.route('/moderation/<post_id>/reject', methods=['POST'])
@safe("blueprints/admin.py | moderation_reject")
@jwt_required()
@check_user_access
def moderation_reject(post_id, only_admin=True):
    reasons = request.json.get("reason")
    user_id = get_jwt_identity()

    PostService.is_valid_uuid(post_id)
    PostService.reject(reasons, post_id, user_id)

    return jsonify({}), 204


@admin_routes.route('/statistics', methods=['GET'])
@safe("blueprints/admin.py | statistics")
@jwt_required()
@check_user_access
def statistics(only_admin=True):
    user_id = get_jwt_identity()

    total_posts = News.query.filter_by(status="published").count()
    total_posts_by_current_author = News.query.filter_by(status="published", user_id=user_id).count()

    active_user = get_most_three_active_user()
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
@check_user_access
def statistics_for_post(post_id, only_admin=True):
    PostService.is_valid_uuid(post_id)
    post = News.query.filter_by(status="published", post_id=post_id).first()

    if post is None:
        raise NotFound("Post not found")

    return jsonify(get_statistics_by_posts_id(post_id)), 200
