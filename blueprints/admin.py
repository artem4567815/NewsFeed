from flask import Blueprint, render_template, request, redirect, jsonify
from config import ADMIN_PASSWORD_HASH, ADMIN_USERNAME
from werkzeug.security import generate_password_hash, check_password_hash
from manage import *
from methods import *

admin_routes = Blueprint('admin', __name__)

@admin_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            user = User(1)
            login_user(user)
            return redirect("/admin/HomePage")
        else:
            return jsonify({"message": "Invalid username or password"})

    else:
        return render_template("login.html")

@admin_routes.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@admin_routes.route("/HomePage")
@login_required
def home():
    return render_template("admin.html")

@admin_routes.route("/post")
@login_required
def posts():
    return render_template("canvas.html")


@admin_routes.route('/save-image', methods=['POST'])
@login_required
def save_image():
    if request.method == "POST":
        data = request.get_json()
        title = data.get('title')
        short_description = data.get('shortDescription')
        full_description = data.get('fullDescription')
        interval = data.get('input')
        file = ""

        if data:
            image = data.get('dataURL')
            file = save_file(image)

        add_to_database2(title, short_description, full_description, file, interval)

        return jsonify({"message": "OK"}), 200
    return jsonify({"message": "ERROR"}), 404