from ..models.permission_model import Profile, Permission
from api import db

# permission
def create_permission(name: str) -> Permission:
    perm = Permission(name=name)
    db.session.add(perm)
    db.session.commit()
    return perm

# profile
def create_profile(name: str, permission_ids: list[int] | None = None) -> Profile:
    profile = Profile(name=name)
    if permission_ids:
        permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()
        profile.permissions.extend(permissions)
    db.session.add(profile)
    db.session.commit()
    return profile

def list_profile_id(profile_id: int) -> Profile:
    return Profile.query.get(profile_id)
