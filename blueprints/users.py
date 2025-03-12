from flask import Blueprint, render_template, session
from flask_login import login_required
from methods import user_required, find_news_by_user_id, safe

user_routes = Blueprint('user', __name__)


@user_routes.route('/HomePage')
@safe
@login_required
@user_required
def dashboard():
    walls = find_news_by_user_id(session['_user_id'])
    return render_template('userPage.html', walls=walls)


@user_routes.route("/create")
@safe
@login_required
@user_required
def create():
    return render_template("canvas2.html")


