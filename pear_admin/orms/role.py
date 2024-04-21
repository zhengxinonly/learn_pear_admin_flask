import sqlalchemy as sa
from sqlalchemy.orm import backref, relationship

from ._base import BaseORM


class RoleORM(BaseORM):
    __tablename__ = "ums_role"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(20), nullable=False, comment="角色名称")
    code = sa.Column(sa.String(20), nullable=False, comment="角色标识符")
    desc = sa.Column(sa.Text)

    rights_ids = sa.Column(
        sa.String(512),
        comment="权限ids,1,2,5。冗余字段，用户缓存用户权限",
    )

    rights_list = relationship(
        "RightsORM", secondary="ums_role_rights", backref=backref("role")
    )

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "desc": self.desc,
            "rights_ids": self.rights_ids,
        }
