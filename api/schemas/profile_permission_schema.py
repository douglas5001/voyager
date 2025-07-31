from api import ma
from ..models import profile_permission_model

class PermissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = profile_permission_model.Permission
        load_instance = True
        include_fk = True
        
        fields = ("id", "name")

class ProfileSchema(ma.SQLAlchemyAutoSchema):
    permissions = ma.Nested(PermissionSchema, many=True)
    

    class Meta:
        model = profile_permission_model.Profile
        load_instance = True
        
        fields = ("id", "name")
