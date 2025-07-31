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
        """
        Realizar login e obter tokens de acesso e refresh.
        ---
        tags:
          - Login
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              id: LoginRequest
              required:
                - email
                - password
              properties:
                email:
                  type: string
                  example: usuario@email.com
                password:
                  type: string
                  example: senha123
        responses:
          200:
            description: Login realizado com sucesso
            schema:
              id: LoginResponse
              properties:
                access_token:
                  type: string
                refresh_token:
                  type: string
                message:
                  type: string
                  example: login realizado com sucesso
          400:
            description: Erro de validação nos dados de entrada
          401:
            description: Credenciais inválidas
        """
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


# class RefreshTokenResource(Resource):
#     @jwt_required(refresh=True)
#     def post(self):
#         usuario_id = get_jwt_identity()
#         novo_token = create_access_token(identity=usuario_id, expires_delta=timedelta(hours=1))
#         return {"access_token": novo_token}, 200


api.add_resource(LoginResource, "/login")
# api.add_resource(RefreshTokenResource, "/token/refresh")
