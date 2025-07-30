from flask_restful import Resource
from api import api, jwt
from ..schemas import login_schema
from flask import request, make_response, jsonify
from ..services import user_service
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta


class LoginList(Resource):
    @jwt.additional_claims_loader
    def add_claims_to_access_token(identity):
        user_token = user_service.list_user_id(identity)
        if user_token.is_admin:
            roles = 'admin'
        else:
            roles = 'user'

        return {'roles':roles}

    def post(self):
        """
        Realiza login e retorna tokens JWT
        ---
        tags:
          - Autenticação
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
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
              type: object
              properties:
                access_token:
                  type: string
                refresh_token:
                  type: string
                message:
                  type: string
                  example: login realizado com sucesso
          400:
            description: Erro de validação nos dados enviados
          401:
            description: Credenciais estão inválidas
        """
        ls = login_schema.LoginSchema()
        validate = ls.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            email = request.json["email"]
            password = request.json["password"]

            user_db = user_service.list_user_email((email))

            if user_db and user_db.show_password(password):
                access_token = create_access_token(
                    identity=user_db.id,
                    expires_delta=timedelta(seconds=500)
                )

                refresh_token = create_refresh_token(
                    identity=user_db.id
                )

                return make_response(jsonify({
                    'access_token':access_token,
                    'refresh_token':refresh_token,
                    'message':'login realizado com sucesso'
                }), 200)

            return make_response(jsonify({
                'message':'Credenciais estao invalidadas'
            }), 401)




api.add_resource(LoginList, '/login')
