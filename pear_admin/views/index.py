from flask import Blueprint, render_template

index_bp = Blueprint("index_bp", __name__)


@index_bp.route("/")
def index():
    return render_template("index.html")


@index_bp.route("/view/console/index.html")
def console1():
    return render_template("view/console/index.html")


@index_bp.route("/view/analysis/index.html")
def analysis1():
    return render_template("view/analysis/index.html")


@index_bp.route("/login.html")
def login():
    return render_template("login.html")
