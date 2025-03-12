from flask import Blueprint, render_template, request
from flask_login import login_required
from methods import *

admin_routes = Blueprint('admin', __name__)

@admin_routes.route("/HomePage")
@safe
@login_required
@admin_required
def home():
    return render_template("admin.html")


@admin_routes.route("/post")
@safe
@login_required
@admin_required
def posts():
    return render_template("canvas2.html")


@admin_routes.route("/post2")
@safe
@login_required
@admin_required
def posts2():
    return render_template("test.html")
