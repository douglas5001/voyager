from flask_restful import Resource
from api import api
from api.services import profile_service
from ..permission_required import permission_required
from ..schemas import user_schema
from flask import request, make_response, jsonify
from ..entity import user
from ..services import user_service
from flask_jwt_extended import jwt_required, get_jwt


class userList(Resource):
    @permission_required("listuser")
    def get(self):
        """
        Lista todos os usuários cadastrados.

        ⚠️ **Requer token JWT no header**  
        Exemplo de header:
        Authorization: Bearer **<seu_token_aqui>**

        ---
        tags:
          - User
        security:
          - BearerAuth: []
        responses:
          200:
            description: Lista de usuários retornada com sucesso
            schema:
              type: array
              items:
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  email:
                    type: string
                  profile_id:
                    type: integer
                  is_admin:
                    type: boolean
          401:
            description: Token ausente ou inválido
        """
        users = user_service.list_user()
        us = user_schema.userSchema(many=True)
        return make_response(us.jsonify(users))

    def post(self):
        """
        Criar um novo usuário e vinculá-lo a um perfil existente.

        Exemplo de JSON no corpo da requisição:
        {
          "name": "João da Silva",
          "email": "joao@email.com",
          "password": "senhaSegura123",
          "profile_id": 2,
          "is_admin": false
        }
        ---
        tags:
          - User
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              id: UserRequest
              required:
                - name
                - email
                - password
                - profile_id
                - is_admin
              properties:
                name:
                  type: string
                  example: João da Silva
                email:
                  type: string
                  example: joao@email.com
                password:
                  type: string
                  example: senhaSegura123
                profile_id:
                  type: integer
                  example: 2
                is_admin:
                  type: boolean
                  example: false
        responses:
          201:
            description: Usuário criado com sucesso
            schema:
              id: UserResponse
              properties:
                id:
                  type: integer
                name:
                  type: string
                email:
                  type: string
                profile_id:
                  type: integer
                is_admin:
                  type: boolean
          400:
            description: Erro de validação nos dados de entrada
        """
        us = user_schema.userSchema()
        validate = us.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            name = request.json["name"]
            email = request.json["email"]
            password = request.json["password"]
            profile_id = request.json["profile_id"]
            list_profile = profile_service.list_profile_id(profile_id)
            if list_profile is None:
              return make_response(jsonify("perfil não existe"))
            
            is_admin = request.json["is_admin"]
            novo_user = user.User(name=name, email=email, password=password, profile_id=profile_id, is_admin=is_admin)
            resultado = user_service.create_user(novo_user)
            x = us.jsonify(resultado)
            return make_response(x, 201)




api.add_resource(userList, '/users')

