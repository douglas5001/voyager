from ...models.user import profile_permission_model
from api import db

def create_profile(name: str, permission_ids: list[int] | None = None) -> profile_permission_model.Profile:
    profile = profile_permission_model.Profile(name=name)
    if permission_ids:
        permissions = profile_permission_model.Permission.query.filter(profile_permission_model.Permission.id.in_(permission_ids)).all()
        profile.permissions.extend(permissions)
    db.session.add(profile)
    db.session.commit()
    return profile

def list_profile_id(profile_id: int) -> profile_permission_model.Profile:
    return profile_permission_model.Profile.query.get(profile_id)

