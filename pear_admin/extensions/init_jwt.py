from flask_jwt_extended import JWTManager

from pear_admin.orms import UserORM

jwt = JWTManager()


# create_access_token(user)  -> token
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# jwt_required -> 加载 token
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]  # user.id
    return UserORM.query.filter(UserORM.id == identity).one_or_none()


@jwt.unauthorized_loader
def missing_token_callback(error):
    return {"msg": "操作未授权，请重新登录", "code": -1}, 403


@jwt.expired_token_loader
def expired_token_callback():
    return {"msg": "token 已过期，请重新登录", "code": -1}, 403
