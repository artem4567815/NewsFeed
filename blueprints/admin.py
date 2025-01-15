from flask import Blueprint, render_template, request, redirect, jsonify
from werkzeug.security import generate_password_hash
from manage import *
from methods import *

admin_routes = Blueprint('admin', __name__)

@admin_routes.route("/HomePage")
@login_required
@admin_required
def home():
    return render_template("admin.html")

@admin_routes.route("/post")
@login_required
@admin_required
def posts():
    return render_template("canvas.html")


@admin_routes.route('/save-image', methods=['POST'])
@login_required
@admin_required
def save_image():
    if request.method == "POST":
        data = request.get_json()
        title = data.get('title')
        short_description = data.get('shortDescription')
        full_description = data.get('fullDescription')
        interval = data.get('input')
        file = ""
        user_id = session.get("user_id")
        if data:
            image = data.get('dataURL')
            file = save_file(image)

        if not user_id:
            return jsonify({"message": "ERROR"}), 404
        
        add_to_database2(title, short_description, full_description, file, interval, user_id)

        return jsonify({"message": "OK"}), 200
    return jsonify({"message": "ERROR"}), 404