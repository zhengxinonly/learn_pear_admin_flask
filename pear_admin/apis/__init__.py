from flask import Blueprint, Flask

from .department import department_api
from .passport import passport_bp
from .rigths import rights_api
from .role import role_api
from .user import user_api


def register_apis(app: Flask):
    # 二级 api 蓝图
    api_api = Blueprint("api", __name__, url_prefix="/api/v1")

    api_api.register_blueprint(passport_bp)
    api_api.register_blueprint(user_api)
    api_api.register_blueprint(department_api)
    api_api.register_blueprint(rights_api)
    api_api.register_blueprint(role_api)

    app.register_blueprint(api_api)
