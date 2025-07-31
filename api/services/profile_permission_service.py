from ..models import profile_permission_model
from api import db

# permission
def create_permission(permission):
    db_permission = profile_permission_model.Permission(name=permission.name)
    db.session.add(db_permission)
    db.session.commit()
    return db_permission

def list_permission_id(id):
    return profile_permission_model.Permission.query.filter_by(id=id).firtst()

def create_profile(profile):
    db_profile = profile_permission_model.Profile(name=profile.name)
    db.session.add(db_profile)
    db.session.commit()
    return db_profile

def list_profile_id(id):
    return profile_permission_model.Profile.query.filter_by(id=id).firtst()


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
