from flask import request
from flask_restful import Resource

from api import api
from ..schemas.permission_schema import PermissionSchema
from ..services import permission_service
from ..permission_required import permission_required

schema = PermissionSchema()


class PermissionList(Resource):
    #@permission_required("permission:create")
    def post(self):
        """
        Criar uma nova permissão e atribuí-la a perfis, se necessário.

        Exemplo de JSON no corpo da requisição:
        {
          "name": "permission:create",
          "profile_ids": [1, 2, 3]
        }
        ---
        tags:
          - Permission
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              id: Permission
              required:
                - name
              properties:
                name:
                  type: string
                  example: permission:create
                profile_ids:
                  type: array
                  items:
                    type: integer
                  example: [1, 2, 3]
        responses:
          201:
            description: Permissão criada com sucesso
            schema:
              id: PermissionResponse
              properties:
                id:
                  type: integer
                name:
                  type: string
          400:
            description: Erro de validação nos dados de entrada
        """
        erros = schema.validate(request.json)
        if erros:
            return erros, 400

        name = request.json["name"]
        profile_ids = request.json.get("profile_ids", [])

        permission = permission_service.create_permission(name)

        if profile_ids:
            permission_service.add_permission_to_profiles(permission.id, profile_ids)

        return schema.dump(permission), 201


api.add_resource(PermissionList, "/permissions")