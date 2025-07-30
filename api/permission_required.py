from functools import wraps
from flask import jsonify, make_response
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def permission_required(permission_name: str):
    """
    Concede acesso quando:
    • o usuário é admin   → claims["is_admin"] == True
    • OU possui a permissão solicitada
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            # Admin sempre passa
            if claims.get("is_admin", False):
                return fn(*args, **kwargs)

            # Caso contrário, verifica a permissão específica
            if permission_name not in claims.get("permissions", []):
                return make_response(
                    jsonify(message="Permissão negada"), 403
                )
            return fn(*args, **kwargs)
        return wrapper
    return decorator
