from api import ma
from ..models import user_model
from marshmallow import fields

class userSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = user_model.User
        load_instance = True
        fields = ("id", "name", "email", "password", "is_admin", "profile")

    name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    profile = fields.String(required=False)
    is_admin = fields.Boolean(required=True)
