from flask import Blueprint, Flask

from .department import department_api
from .passport import passport_bp
from .user import user_api


def register_apis(app: Flask):
    # 二级 api 蓝图
    api_api = Blueprint("api", __name__, url_prefix="/api/v1")

    api_api.register_blueprint(passport_bp)
    api_api.register_blueprint(user_api)
    api_api.register_blueprint(department_api)

    app.register_blueprint(api_api)
