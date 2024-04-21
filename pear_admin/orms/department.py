import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ._base import BaseORM


class DepartmentORM(BaseORM):
    __tablename__ = "ums_department"

    id = sa.Column(sa.Integer, primary_key=True, comment="部门 ID")
    name = sa.Column(sa.String(50), comment="部门名")
    leader = sa.Column(sa.String(50), comment="负责人")
    enable = sa.Column(sa.Boolean, default=True)

    pid = sa.Column(sa.Integer, sa.ForeignKey("ums_department.id"))

    parent = relationship("DepartmentORM", back_populates="children", remote_side=[id])
    children = relationship("DepartmentORM", back_populates="parent")
