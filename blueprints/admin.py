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
