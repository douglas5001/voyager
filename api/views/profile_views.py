from flask import request
from flask_restful import Resource

from api import api
from ..schemas.profile_schema import ProfileSchema
from ..services import profile_service
from ..permission_required import permission_required

schema = ProfileSchema()


class ProfileList(Resource):
    # @permission_required("profile:create")
    def post(self):
        """
        Criar um novo perfil e vincular permissões existentes.

        Exemplo de JSON no corpo da requisição:
        {
          "name": "Administrador",
          "permission_ids": [1, 2, 3]
        }
        ---
        tags:
          - Profile
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              id: ProfileRequest
              required:
                - name
              properties:
                name:
                  type: string
                  example: Administrador
                permission_ids:
                  type: array
                  items:
                    type: integer
                  example: [1, 2, 3]
        responses:
          201:
            description: Perfil criado com sucesso
            schema:
              id: ProfileResponse
              properties:
                id:
                  type: integer
                name:
                  type: string
                permissions:
                  type: array
                  items:
                    type: string
          400:
            description: Erro de validação nos dados de entrada
        """
        erros = schema.validate(request.json)
        if erros:
            return erros, 400

        name = request.json["name"]
        permission_ids = request.json.get("permission_ids", [])

        profile = profile_service.create_profile(name, permission_ids)
        return schema.dump(profile), 201

api.add_resource(ProfileList, "/profiles")