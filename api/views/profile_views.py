from flask import jsonify, make_response, request
from flask_restful import Resource

from api import api
from ..schemas.profile_permission_schema import ProfileSchema
from ..services import profile_permission_service
from ..permission_required import permission_required
from ..entity import profile_permission

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
        schema = ProfileSchema()
        validate = schema.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
          name = request.json["name"]

          new_profile = profile_permission.Profile(name=name)
          result = profile_permission_service.create_profile(new_profile)
          x = schema.jsonify(result)
          
          return make_response(x, 201)

api.add_resource(ProfileList, "/profiles")


class ProfilePermissionAttach(Resource):
    def post(self, profile_id):
        """
        Adicionar permissões a um perfil existente.

        Envie um array de IDs de permissões para vincular ao perfil.

        ---
        tags:
          - Profile
        consumes:
          - application/json
        parameters:
          - in: path
            name: profile_id
            required: true
            description: ID do perfil que receberá as permissões
            type: integer
          - in: body
            name: body
            required: true
            schema:
              id: AttachPermissionsRequest
              required:
                - permission_ids
              properties:
                permission_ids:
                  type: array
                  items:
                    type: integer
                  example: [1, 2, 3]
        responses:
          200:
            description: Permissões adicionadas com sucesso ao perfil
            schema:
              id: AttachPermissionsResponse
              properties:
                id:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: Administrador
                permissions:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 2
                      name:
                        type: string
                        example: permission:create
          400:
            description: Erro de validação nos dados de entrada
            schema:
              properties:
                error:
                  type: string
                  example: permission_ids deve ser uma lista
          404:
            description: Perfil não encontrado
            schema:
              properties:
                error:
                  type: string
                  example: Perfil não encontrado
        """
        data = request.json
        if "permission_ids" not in data or not isinstance(data["permission_ids"], list):
            return make_response(jsonify({"error": "permission_ids deve ser uma lista"}), 400)

        permission_ids = data["permission_ids"]
        profile = profile_permission_service.add_permissions_to_profile(profile_id, permission_ids)

        if not profile:
            return make_response(jsonify({"error": "Perfil não encontrado"}), 404)

        schema = ProfileSchema()
        return make_response(schema.jsonify(profile), 200)


api.add_resource(ProfilePermissionAttach, "/profiles/<int:profile_id>/permissions")