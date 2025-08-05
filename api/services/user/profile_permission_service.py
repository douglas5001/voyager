from ...models.user import profile_permission_model
from api import db

# permission
def create_permission(permission):
    db_permission = profile_permission_model.Permission(name=permission.name)
    db.session.add(db_permission)
    db.session.commit()
    return db_permission

def list_permission():
    permission = profile_permission_model.Permission.query.all()
    return permission

def list_permission_id(id):
    return profile_permission_model.Permission.query.filter_by(id=id).first()


def list_profile():
    profile = profile_permission_model.Profile.query.all()
    return profile


def list_profile_id(id):
    return profile_permission_model.Profile.query.filter_by(id=id).first()

def delete_profile(profile):
    db.session.delete(profile)
    db.session.commit()
    
def put_profile(current_profile, new_profile):
    current_profile.name = new_profile.name

    new_permissions = []
    for permission_id in new_profile.permission_ids:
        permission = list_permission_id(permission_id)
        if permission:
            new_permissions.append(permission)

    current_profile.permissions = new_permissions

    db.session.commit()
    return current_profile

def create_profile(profile):
    db_profile = profile_permission_model.Profile(name=profile.name)

    for permission_id in profile.permission_ids:
        permission = list_permission_id(permission_id)
        if permission:
            db_profile.permissions.append(permission)

    db.session.add(db_profile)
    db.session.commit()
    return db_profile

def put_permission(permission, new_permission):
    permission.name = new_permission.name
    db.session.commit()

def delete_permission(permission):
    db.session.delete(permission)
    db.session.commit()

def add_permissions_to_profile(profile_id, permission_ids):
    profile = profile_permission_model.Profile.query.get(profile_id)
    if not profile:
        return None

    existing_permission_ids = {p.id for p in profile.permissions.all()}
    new_permission_ids = set(permission_ids) - existing_permission_ids

    if not new_permission_ids:
        return profile  # Nenhuma nova permissão para adicionar

    new_permissions = profile_permission_model.Permission.query.filter(
        profile_permission_model.Permission.id.in_(new_permission_ids)
    ).all()

    profile.permissions.extend(new_permissions)
    db.session.commit()
    return profile
