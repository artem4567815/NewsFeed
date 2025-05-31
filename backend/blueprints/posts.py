from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from methods import *
from flask_pydantic import validate
from schemas import *
from manage import minio

posts = Blueprint('posts', __name__)


@posts.route("", methods=["GET"])
@safe("blueprints/posts.py | category_posts")
@validate()
def category_posts(query: QueryRequest):
    posts_list, posts_count = PostService.get_news_by_query(query)
    return jsonify({"posts": posts_list, "posts_count":posts_count}), 200


@posts.route("/<post_id>", methods=["GET"])
@safe("blueprints/posts.py | detailed_posts")
def detailed_posts(post_id):
    PostService.is_valid_uuid(post_id)
    post = PostService.get_news_by_post_id(post_id)

    return jsonify(post.as_dict()), 200


@posts.route("/<post_id>", methods=["PATCH"])
@safe("blueprints/posts.py | patch_posts")
@jwt_required()
@validate()
@check_user_access
def patch_posts(body: PatchPostRequest, post_id, only_user=True):
    PostService.is_valid_uuid(post_id)
    post = PostService.get_news_by_post_id(post_id)
    post = PostService.patch_post(post, body)

    return jsonify(post.as_dict()), 200


@posts.route("/<post_id>", methods=["DELETE"])
@safe("blueprints/posts.py | delete_posts")
@jwt_required()
@check_user_access
def delete_posts(post_id):
    PostService.is_valid_uuid(post_id)
    post = PostService.get_news_by_post_id(post_id)

    minio.delete_file_by_url(post.image_url)

    db.session.delete(post)
    db.session.commit()

    return jsonify({}), 204


@posts.route("/<post_id>/like", methods=["POST"])
@safe("blueprints/posts.py | like_posts")
@jwt_required()
def like_posts(post_id):
    PostService.is_valid_uuid(post_id)
    post = PostService.get_news_by_post_id(post_id)
    user_id = get_jwt_identity()

    PostService.like_post(post, user_id)
    return jsonify({}), 204


@posts.route("/<post_id>/unlike", methods=["POST"])
@safe("blueprints/posts.py | unlike_posts")
@jwt_required()
def unlike_posts(post_id):
    PostService.is_valid_uuid(post_id)
    post = PostService.get_news_by_post_id(post_id)
    user_id = get_jwt_identity()

    PostService.unlike_post(post, user_id)
    return jsonify({}), 204


@posts.route("/<post_id>/view", methods=["POST"])
@safe("blueprints/posts.py | view_posts")
def view_posts(post_id):
    PostService.is_valid_uuid(post_id)
    post = PostService.get_news_by_post_id(post_id)

    post.views += 1
    db.session.commit()

    return jsonify({}), 204


@posts.route("/<post_id>/join", methods=["POST"])
@safe("blueprints/posts.py | join_to_posts")
@jwt_required()
def join_to_posts(post_id):
    PostService.is_valid_uuid(post_id)
    post = PostService.get_news_by_post_id(post_id)
    user_id = get_jwt_identity()
    PostService.join(post, user_id)

    return jsonify({}), 204


@posts.route('/create/post', methods=['POST'])
@safe("blueprints/posts.py | save_news")
@jwt_required()
@validate()
def save_news(body: CreateNewsRequest):
    user_id = get_jwt_identity()
    user = UserService.get_user_by_user_id(user_id)

    file_url = PostService.resolve_file_url(body.post_img, user.login)

    post_status = "published" if get_jwt().get("is_admin") else "draft"
    news = PostService.create_news(body, file_url, user_id, post_status)

    return jsonify(news.as_dict()), 201


@posts.route('/filter/info', methods=['GET'])
@safe("blueprints/posts.py | get_filter_info")
def get_filter_info():
    tags = PostService.get_tags()
    schools = UserService.get_school()

    return jsonify({"tags": tags, "schools": schools}), 200
