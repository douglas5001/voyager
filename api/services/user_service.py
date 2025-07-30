from ..models import user_model
from api import db

def create_user(user):
    user_bd = user_model.user(name=user.name, email=user.email, password=user.password, is_admin=user.is_admin)
    user_bd.encrypt_password()
    db.session.add(user_bd)
    db.session.commit()
    return user_bd

def list_user():
    user = user_model.user.query.all()
    return user

def list_user_email(email):
    return user_model.user.query.filter_by(email=email).first()

def list_user_id(id):
    return user_model.user.query.filter_by(id=id).first()

