from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required

from pear_admin.extensions import db
from pear_admin.orms import RightsORM

rights_api = Blueprint("rights", __name__)


@rights_api.get("/rights/treetable")
@jwt_required()
def get_list_as_treetable():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("limit", default=10, type=int)

    q = db.select(RightsORM)
    q = q.where(RightsORM.type == "menu")
    pages = db.paginate(q, page=page, per_page=per_page, error_out=False)

    ret = []
    for page in pages.items:
        # 一级目录
        data = page.json()
        data["children"] = []
        for child in page.children:
            # 二级路径
            child_data = child.json()
            if child.children:
                # 三级权限
                child_data["children"] = [
                    sub_child.json() for sub_child in child.children
                ]
                child_data["isParent"] = True
            data["children"].append(child_data)
            data["isParent"] = True
        ret.append(data)
    return {"code": 0, "message": "获取数据成功", "data": ret}


@rights_api.post("/rights")
def create_rights():
    data = request.get_json()
    rights_orm = RightsORM(**data)
    rights_orm.save()
    return {"code": 0, "msg": "新增数据成功"}


@rights_api.put("/rights/<int:rid>")
def update_rights(rid):
    data = request.get_json()
    rights_orm = RightsORM.query.get(rid)
    for key, val in data.items():
        setattr(rights_orm, key, val)
    rights_orm.save()
    return {"code": 0, "msg": "修改数据成功"}


@rights_api.delete("/rights/<int:rid>")
def drop_rights(rid):
    rights_orm = RightsORM.query.get(rid)
    rights_orm.delete()
    return {"code": 0, "msg": "删除数据成功"}
