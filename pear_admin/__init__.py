from flask import Flask, render_template

from pear_admin.views.index import views_bp


def create_app():
    app = Flask("pear_admin_flask")
    app.register_blueprint(views_bp)
    return app
