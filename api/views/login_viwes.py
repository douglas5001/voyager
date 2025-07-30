from datetime import timedelta

from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)

from api import api, jwt
from ..schemas.login_schema import LoginSchema
from ..services import user_service


@jwt.additional_claims_loader
def adicionar_permissoes(identity):
    usuario = user_service.list_user_id(identity)
    permissoes = [p.name for p in usuario.profile.permissions] if usuario.profile else []
    return {
        "permissions": permissoes,
        "is_admin": usuario.is_admin
    }


class LoginResource(Resource):
    def post(self):
        schema = LoginSchema()
        erros = schema.validate(request.json)
        if erros:
            return erros, 400

        email = request.json["email"]
        senha = request.json["password"]

        usuario = user_service.list_user_email(email)
        if not (usuario and usuario.show_password(senha)):
            return {"message": "Credenciais inválidas"}, 401

        access_token = create_access_token(identity=usuario.id, expires_delta=timedelta(hours=1))
        refresh_token = create_refresh_token(identity=usuario.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "login realizado com sucesso",
        }, 200


class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        usuario_id = get_jwt_identity()
        novo_token = create_access_token(identity=usuario_id, expires_delta=timedelta(hours=1))
        return {"access_token": novo_token}, 200


api.add_resource(LoginResource, "/login")
api.add_resource(RefreshTokenResource, "/token/refresh")
