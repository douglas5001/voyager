from api import ma
from ..models.permission_model import Profile, Permission

class PermissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Permission
        load_instance = True

class ProfileSchema(ma.SQLAlchemyAutoSchema):
    permissions = ma.Nested(PermissionSchema, many=True)
    

    class Meta:
        model = Profile
        load_instance = True
