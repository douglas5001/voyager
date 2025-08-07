import os
import uuid
from ...models.user import user_model
from api import db
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER

def save_image_file(image_file):
    if not image_file:
        return None

    filename = secure_filename(image_file.filename)
    ext = filename.rsplit(".", 1)[-1]
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    path = os.path.join(UPLOAD_FOLDER, unique_name)
    image_file.save(path)
    return unique_name

def create_user(user, image_file=None):
    image_name = save_image_file(image_file) if image_file else None
    
    user_bd = user_model.User(name=user.name, email=user.email, password=user.password, profile_id=user.profile_id, is_admin=user.is_admin,  image=image_name)
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

def list_user_email(email):
    return user_model.User.query.filter_by(email=email).first()