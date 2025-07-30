from ..models.permission_model import Profile, Permission
from api import db

# permission
def create_permission(name: str) -> Permission:
    permission = Permission(name=name)
    db.session.add(permission)
    db.session.commit()
    return permission

# profile
def create_profile(name: str, permission_ids: list[int]) -> Profile:
    profile = Profile(name=name)
    profile.permissions = Permission.query.filter(Permission.id.in_(permission_ids)).all()
    db.session.add(profile)
    db.session.commit()
    return profile

def list_profile_id(profile_id: int) -> Profile:
    return Profile.query.get(profile_id)

def add_permission_to_profiles(permission_id: int, profile_ids: list[int]) -> None:
    permission = Permission.query.get_or_404(permission_id)
    profiles = Profile.query.filter(Profile.id.in_(profile_ids)).all()
    for profile in profiles:
        if permission not in profile.permissions:
            profile.permissions.append(permission)
    db.session.commit()