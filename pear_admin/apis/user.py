from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required

from pear_admin.extensions import db
from pear_admin.orms import RoleORM, UserORM

user_api = Blueprint("user", __name__)


@user_api.get("/user/profile")
@jwt_required()
def get_profile():
    return {"code": 0, "message": "获取个人数据成功", "user": current_user.json()}


@user_api.get("/user")
def user_list():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("limit", default=10, type=int)
    q = db.select(UserORM)

    pages = db.paginate(q, page=page, per_page=per_page)

    return {
        "code": 0,
        "msg": "获取用户数据成功",
        "data": [item.json() for item in pages.items],
        "count": pages.total,
    }


@user_api.post("/user")
def create_user():
    data = request.get_json()
    if data["id"]:
        del data["id"]
    user = UserORM(**data)
    create_at = data["create_at"]

    if create_at:
        user.create_at = datetime.strptime(create_at, "%Y-%m-%d %H:%M:%S")

    user.password = "123456"
    user.save()
    return {"code": 0, "msg": "新增用户成功"}


@user_api.put("/user/<int:uid>")
def update_user(uid):
    data = request.get_json()

    user = UserORM.query.get(uid)
    for key, value in data.items():
        setattr(user, key, value)

    user.save()
    return {"code": 0, "msg": "新增用户成功"}


@user_api.delete("/user/<int:uid>")
def del_user(uid):
    user_obj = UserORM.query.get(uid)
    user_obj.delete()
    return {"code": 0, "msg": "删除用户成功"}


@user_api.get("/user/user_role/<int:uid>")
def get_user_role(uid):
    user: UserORM = db.session.execute(
        db.select(UserORM).where(UserORM.id == uid)
    ).scalar()

    wn_role_list = [r.id for r in user.role_list]

    return {
        "code": 0,
        "msg": "返回角色权限数据成功",
        "data": wn_role_list,
    }


@user_api.put("/user/user_role/<int:rid>")
def change_user_role(rid):
    role_ids = request.json.get("rights_ids", "")
    role_list = role_ids.split(",")

    user: UserORM = db.session.execute(
        db.select(UserORM).where(UserORM.id == rid)
    ).scalar()

    role_obj_list = db.session.execute(
        db.select(RoleORM).where(RoleORM.id.in_(role_list))
    ).all()

    user.role_list = [r[0] for r in role_obj_list]
    user.save()
    return {"code": 0, "msg": "授权成功"}
