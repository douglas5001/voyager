# models/permission_model.py
from api import db

profile_permissions = db.Table(
    "profile_permissions",
    db.Column("profile_id", db.Integer, db.ForeignKey("profile.id"), primary_key=True),
    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id"), primary_key=True),
)

class Permission(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)

class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    permissions = db.relationship(
        "Permission",
        secondary=profile_permissions,
        backref=db.backref("profiles", lazy="dynamic"),
        lazy="dynamic",
    )
