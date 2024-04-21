from pear_admin.extensions import db


class BaseORM(db.Model):
    __abstract__ = True

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
