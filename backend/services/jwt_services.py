from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token

def generate_tokens(user):

    access_token = create_access_token(

        identity=str(user.HKKM_Id),

        additional_claims={

            "email": user.HKKM_Email,

            "role": user.HKKM_Role
        }
    )

    refresh_token = create_refresh_token(
        identity=str(user.HKKM_Id)
    )

    return {

        "access_token": access_token,

        "refresh_token": refresh_token
    }