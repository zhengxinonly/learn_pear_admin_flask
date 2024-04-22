from flask import Blueprint
from flask_jwt_extended import current_user, jwt_required

user_api = Blueprint("user", __name__)


@user_api.get("/user/profile")
@jwt_required()
def get_profile():
    return {"code": 0, "message": "获取个人数据成功", "user": current_user.json()}
