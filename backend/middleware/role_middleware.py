from functools import wraps

from flask_jwt_extended import verify_jwt_in_request

from flask_jwt_extended import get_jwt

from utils.response import error_response


def role_required(required_role):

    def decorator(func):

        @wraps(func)

        def wrapper(*args, **kwargs):

            verify_jwt_in_request()

            claims = get_jwt()

            if claims.get("role") != required_role:

                return error_response(

                    "Access denied",

                    403
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator