from api import ma
from ...models.user import profile_permission_model
from marshmallow import fields

class PermissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = profile_permission_model.Permission
        load_instance = True
        include_fk = True
        
        fields = ("id", "name")
        
    name = fields.String(required=True)

class ProfileSchema(ma.SQLAlchemyAutoSchema):
    permission_ids = fields.List(fields.Integer(), required=False, load_only=True)
    permissions = ma.Nested(PermissionSchema, many=True, dump_only=True)

    class Meta:
        model = profile_permission_model.Profile
        load_instance = True
        fields = ("id", "name", "permission_ids", "permissions")

    name = fields.String(required=True)