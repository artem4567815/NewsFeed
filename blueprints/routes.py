from flask import Blueprint, render_template
from methods import get_all_news_files, get_all_news

main_routes = Blueprint('routes', __name__)

@main_routes.route("/events")
def events():
    #news_list = get_all_news_files()
    news_list = get_all_news()
    return render_template("index.html", news=news_list, page_type="events")

@main_routes.route("/wall")
def wall():
    return render_template("index.html", page_type="wall")

@main_routes.route("/team_search")
def team_search():
    return render_template("index.html", page_type="team_search")
