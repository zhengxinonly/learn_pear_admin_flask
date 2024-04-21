from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import backref, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from ._base import BaseORM


class UserORM(BaseORM):
    __tablename__ = "ums_user"

    id = sa.Column(sa.Integer, primary_key=True, comment="自增id")
    nickname = sa.Column(sa.String(128), nullable=False, comment="昵称")
    username = sa.Column(sa.String(128), nullable=False, comment="登录名")
    password_hash = sa.Column(sa.String(255), nullable=False, comment="登录密码")
    mobile = sa.Column(sa.String(32), nullable=False, comment="手机")
    email = sa.Column(sa.String(64), nullable=False, comment="邮箱")
    avatar = sa.Column(sa.Text, comment="头像地址")
    create_at = sa.Column(
        sa.DateTime,
        nullable=False,
        comment="创建时间",
        default=datetime.now,
    )
    department_id = sa.Column(
        sa.Integer, sa.ForeignKey("ums_department.id"), default=1, comment="部门id"
    )

    role_list = relationship(
        "RoleORM", secondary="ums_user_role", backref=backref("user"), lazy="dynamic"
    )

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "mobile": self.mobile,
            "email": self.email,
            "create_at": self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
        }

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password=password)
