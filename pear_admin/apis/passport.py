from flask import Blueprint

passport_bp = Blueprint("passport", __name__)


@passport_bp.post("/login")
def login():
    return {"message": "登录成功", "code": 0}


@passport_bp.post("/logout")
def logout():
    return {"message": "退出成功", "code": 0}
