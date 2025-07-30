from flask import request
from flask_restful import Resource

from api import api
from ..schemas.permission_schema import PermissionSchema
from ..services import permission_service
from ..permission_required import permission_required

schema = PermissionSchema()


class PermissionList(Resource):
    @permission_required("permission:create")
    def post(self):
        """
        Cria uma permissão e (opcionalmente) vincula‑a a perfis
        ---
        tags: [Permissões]
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