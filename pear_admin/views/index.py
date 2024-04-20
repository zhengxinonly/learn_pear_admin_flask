from flask import Blueprint, render_template

views_bp = Blueprint(__name__, "views")


@views_bp.route("/")
def index():
    return render_template("index.html")


@views_bp.route("/view/console/index.html")
def console1():
    return render_template("view/console/index.html")


@views_bp.route("/view/analysis/index.html")
def analysis1():
    return render_template("view/analysis/index.html")


@views_bp.route("/login.html")
def login():
    return render_template("login.html")
