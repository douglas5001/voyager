from api import ma
from ..models.permission_model import Profile, Permission

class PermissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Permission
        load_instance = True
        include_fk = True  # exibe o id no dump

class ProfileSchema(ma.SQLAlchemyAutoSchema):
    permissions = ma.Nested(PermissionSchema, many=True)

    class Meta:
        model = Profile
        load_instance = True
