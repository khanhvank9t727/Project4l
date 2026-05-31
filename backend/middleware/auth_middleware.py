from functools import wraps

from flask_jwt_extended import verify_jwt_in_request

from flask_jwt_extended import get_jwt

from utils.response import error_response


def admin_required(func):

    @wraps(func)

    def wrapper(*args, **kwargs):

        verify_jwt_in_request()

        claims = get_jwt()

        if claims.get("role") != "ADMIN":

            return error_response(

                "Admin access required",

                403
            )

        return func(*args, **kwargs)

    return wrapper