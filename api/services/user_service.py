from ..models import user_model
from api import db

def create_user(user):
    user_bd = user_model.User(name=user.name, email=user.email, password=user.password, profile_id=user.profile_id, is_admin=user.is_admin)
    user_bd.encrypt_password()
    db.session.add(user_bd)
    db.session.commit()
    return user_bd

def list_user():
    user = user_model.User.query.all()
    return user

def list_user_email(email):
    return user_model.User.query.filter_by(email=email).first()

def list_user_id(id):
    return user_model.User.query.filter_by(id=id).first()

