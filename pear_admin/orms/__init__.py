import sqlalchemy as sa

from pear_admin.extensions import db

from .department import DepartmentORM
from .rights import RightsORM
from .role import RoleORM
from .user import UserORM

user_role = sa.Table(
    "ums_user_role",
    db.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("user_id", sa.Integer, sa.ForeignKey("ums_user.id")),
    sa.Column("role_id", sa.Integer, sa.ForeignKey("ums_role.id")),
)

role_rights = sa.Table(
    "ums_role_rights",
    db.metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("role_id", sa.Integer, sa.ForeignKey("ums_role.id")),
    sa.Column("rights_id", sa.Integer, sa.ForeignKey("ums_rights.id")),
)
