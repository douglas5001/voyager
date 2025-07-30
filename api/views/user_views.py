from flask_restful import Resource
from api import api
from ..permission_required import permission_required
from ..schemas import user_schema
from flask import request, make_response, jsonify
from ..entidades import user
from ..services import user_service
from flask_jwt_extended import jwt_required, get_jwt


class userList(Resource):
    @permission_required("listuser")
    def get(self):
        """
        Lista todos os usuários
        ---
        tags:
          - Usuários
        security:
          - BearerAuth: []
        responses:
          200:
            description: Lista de usuários retornada com sucesso
          401:
            description: Token ausente ou inválido
        """
        users = user_service.list_user()
        us = user_schema.userSchema(many=True)
        return make_response(us.jsonify(users))

    def post(self):
        """
        Cria um novo usuário
        ---
        tags:
          - Usuários
        parameters:
          - name: body
            in: body
            required: true
            schema:
              id: User
              required:
                - name
                - email
                - password
                - is_admin
              properties:
                name:
                  type: string
                email:
                  type: string
                password:
                  type: string
                is_admin:
                  type: boolean
        responses:
          201:
            description: Usuário criado com sucesso
          400:
            description: Erro de validação
        """
        us = user_schema.userSchema()
        validate = us.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            name = request.json["name"]
            email = request.json["email"]
            password = request.json["password"]
            is_admin = request.json["is_admin"]
            novo_user = user.User(name=name, email=email, password=password, is_admin=is_admin)
            resultado = user_service.create_user(novo_user)
            x = us.jsonify(resultado)
            return make_response(x, 201)




api.add_resource(userList, '/users')

