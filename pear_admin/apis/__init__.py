from flask import Blueprint, Flask

from .passport import passport_bp


def register_apis(app: Flask):
    # 二级 api 蓝图
    api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

    api_bp.register_blueprint(passport_bp)

    app.register_blueprint(api_bp)
