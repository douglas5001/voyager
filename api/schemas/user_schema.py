from api import ma
from ..models import user_model
from marshmallow import fields

class userSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = user_model.User
        load_instance = True
        fields = ("id", "name", "email", "password", "is_admin")

    name = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    is_admin = fields.Boolean(required=True)
