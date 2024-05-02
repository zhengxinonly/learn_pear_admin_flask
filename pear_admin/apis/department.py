from flask import Blueprint, request
from flask_jwt_extended import current_user, jwt_required

from pear_admin.extensions import db
from pear_admin.orms import DepartmentORM

department_api = Blueprint("department", __name__, url_prefix="/department")


@department_api.get("/")
@jwt_required()
def get_list():
    return {"code": 0, "message": "获取个人数据成功", "user": current_user.json()}


@department_api.get("/treetable")
def get_list_as_treetable():
    # 顶级部门
    q = db.select(DepartmentORM)
    q = q.where(DepartmentORM.pid == 0)
    dept_orm_list = db.session.execute(q).scalars()
    ret = []
    for dept_orm in dept_orm_list:
        dept_orm_data = dept_orm.json()
        dept_orm_data["children"] = []
        if dept_orm.children:
            dept_orm_data["isParent"] = True
        for son in dept_orm.children:
            son_data = son.json()
            dept_orm_data["children"].append(son_data)
        ret.append(dept_orm_data)
    return {"code": 0, "message": "获取树状表格数据成功", "data": ret}


@department_api.post("/")
def create_department():
    data = request.get_json()
    dept_orm = DepartmentORM()
    del data["id"]
    for key, value in data.items():
        setattr(dept_orm, key, value)
    dept_orm.save()
    return {"code": 0, "message": "新建部门成功"}


@department_api.put("/<int:did>")
def update_department(did):
    data = request.get_json()
    dept_orm = DepartmentORM.query.get(did)
    del data["id"]
    for key, value in data.items():
        setattr(dept_orm, key, value)
    dept_orm.save()
    return {"code": 0, "message": "修改部门成功"}


@department_api.delete("/<int:did>")
def drop_department(did):
    dept_orm = DepartmentORM.query.get(did)
    dept_orm.delete()
    return {"code": 0, "message": "修改部门成功"}
