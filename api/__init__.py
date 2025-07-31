from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import pymysql

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API REST FULL",
        "description": "Documentação da API com autenticação JWT",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header usando o esquema Bearer. Exemplo: 'Bearer {seu_token}'"
        }
    }
}

swagger = Swagger(app, template=swagger_template)

from .models import profile_permission_model, user_model
from .views import user_views, login_viwes, refresh_toke_views, profile_views, permission_views