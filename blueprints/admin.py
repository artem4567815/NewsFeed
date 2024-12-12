from flask import Blueprint, render_template, request, redirect, jsonify
from config import ADMIN_PASSWORD_HASH, ADMIN_USERNAME
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import login_user, login_required, logout_user
from manage import *

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