from flask import jsonify, make_response, request
from flask_restful import Resource
from api import api
from ...schemas.user import profile_permission_schema
from ...services.user import profile_permission_service
from ...permission_required import permission_required
from ...entity.user import profile_permission

class PermissionList(Resource):
    #@permission_required("permission:create")
    def get(self):
      """
      Listar todas as permissões disponíveis.

      ---
      tags:
        - Permission
      responses:
        200:
          description: Lista de permissões obtida com sucesso
          schema:
            type: array
            items:
              $ref: '#/definitions/PermissionResponse'
      """
      schema = profile_permission_schema.PermissionSchema(many=True)
      permission = profile_permission_service.list_permission()
      return make_response(schema.jsonify(permission))
    
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
        schema = profile_permission_schema.PermissionSchema()
        validate = schema.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
          name = request.json["name"]
          
          new_permission = profile_permission.Permission(name=name)
          
          result = profile_permission_service.create_permission(new_permission)
          
          x = schema.jsonify(result)
          return make_response(x, 201)
                 
                 
class PermissionDetail(Resource):
    def delete(self, id):
      """
      Excluir uma permissão existente pelo ID.

      ---
      tags:
        - Permission
      parameters:
        - in: path
          name: id
          required: true
          type: integer
          description: ID da permissão a ser excluída
      responses:
        204:
          description: Permissão excluída com sucesso (sem conteúdo)
        404:
          description: Permissão não encontrada
      """
      permission = profile_permission_service.list_permission_id(id)
      if permission is None:
        return make_response(jsonify("Permission não encontrado"), 404)
      profile_permission_service.delete_permission(permission)
      return make_response("Permissão excluida", 204)
    
    def put(self, id):
      """
      Atualizar os dados de uma permissão existente.

      ---
      tags:
        - Permission
      parameters:
        - in: path
          name: id
          required: true
          type: integer
          description: ID da permissão a ser atualizada
        - in: body
          name: body
          required: true
          schema:
            id: PermissionUpdate
            required:
              - name
            properties:
              name:
                type: string
                example: permission:update
      responses:
        200:
          description: Permissão atualizada com sucesso
          schema:
            id: PermissionResponse
            properties:
              id:
                type: integer
              name:
                type: string
        400:
          description: Erro de validação nos dados de entrada
        404:
          description: Permissão não encontrada
      """
      permission = profile_permission_service.list_permission_id(id)
      if permission is None:
        return make_response(jsonify("Permission não encontrado"), 404)
      
      schema = profile_permission_schema.PermissionSchema()
      validate = schema.validate(request.json)
      if validate:
          return make_response(jsonify(validate), 400)
      else:
        name = request.json["name"]
      
      new_Permission = profile_permission.Permission(name=name)
      
      profile_permission_service.put_permission(permission, new_Permission)
      
      update_permision = profile_permission_service.list_permission_id(id)
      
      return make_response(schema.jsonify(update_permision), 200)
      

api.add_resource(PermissionList, "/permissions")
api.add_resource(PermissionDetail, "/permissions/<int:id>")