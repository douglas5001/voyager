from flask import request
from flask_restful import Resource

from api import api
from ..schemas.profile_schema import ProfileSchema
from ..services import profile_service
from ..permission_required import permission_required

schema = ProfileSchema()


class ProfileList(Resource):
    @permission_required("profile:create")
    def post(self):
        """
        Cria um perfil e vincula permissões
        ---
        tags: [Perfis]
        """
        erros = schema.validate(request.json)
        if erros:
            return erros, 400

        name = request.json["name"]
        permission_ids = request.json.get("permission_ids", [])

        profile = profile_service.create_profile(name, permission_ids)
        return schema.dump(profile), 201

api.add_resource(ProfileList, "/profiles")