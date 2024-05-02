from collections import OrderedDict
from copy import deepcopy

from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    jwt_required,
)

from pear_admin.extensions import db
from pear_admin.orms import UserORM

passport_bp = Blueprint("passport", __name__)


@passport_bp.post("/login")
def login():
    # 1. 获取数据
    data = request.get_json()
    print(data)
    # 2. 校验数据
    user: UserORM = db.session.execute(
        db.select(UserORM).where(UserORM.username == data.get("username"))
    ).scalar()
    if not user:
        return {"message": "登录失败，用户名错误", "code": -1}, 401
    if not user.check_password(data.get("password")):
        return {"message": "登录失败，密码错误", "code": -1}, 401
    # 查询用户的角色标识，权限标识
    # 3. 创建 token
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return {
        "message": "登录成功",
        "code": 0,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@passport_bp.post("/logout")
def logout():
    return {"message": "退出成功", "code": 0}


@passport_bp.get("/menu")
@jwt_required()
def get_menu():
    # 使用数据库的数据，构建一个与 menu.json 结构一样的数据返回回去

    rights_orm_list = set()
    current_user: UserORM = get_current_user()
    for role in current_user.role_list:
        for rights_orm in role.rights_list:
            if rights_orm.type != "auth":
                rights_orm_list.add(rights_orm)

    rights_list = [rights_orm.menu_json() for rights_orm in rights_orm_list]
    rights_list.sort(key=lambda x: (x["pid"], x["id"]), reverse=True)

    menu_dict_list = OrderedDict()
    for menu_dict in rights_list:
        if menu_dict["id"] in menu_dict_list.keys():  # 如果当前节点已经存在与字典中
            # 当前节点添加子节点
            menu_dict["children"] = deepcopy(menu_dict_list[menu_dict["id"]])
            menu_dict["children"].sort(key=lambda item: item["sort"])
            # 删除子节点
            del menu_dict_list[menu_dict["id"]]

        if menu_dict["pid"] not in menu_dict_list:
            menu_dict_list[menu_dict["pid"]] = [menu_dict]
        else:
            menu_dict_list[menu_dict["pid"]].append(menu_dict)
    return sorted(menu_dict_list.get(0), key=lambda item: item["sort"])
