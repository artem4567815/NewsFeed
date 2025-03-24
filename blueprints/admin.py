from flask import Blueprint
from methods import *
from flask_jwt_extended import jwt_required
from flask_pydantic import validate
from schemas import *

admin_routes = Blueprint('admin', __name__)


@admin_routes.route('/create/post', methods=['POST'])
@safe("blueprints/admin.py | save_news")
@jwt_required()
@check_jwt_access
@validate()
def save_news(body: CreateNewsRequest):
    file = save_base64_image(body.dataURL)
    user_id = get_jwt_identity()

    news = create_news(body.title, body.short_description, body.full_description, file, body.input, user_id, body.type)

    return jsonify(news.as_dict()), 200
