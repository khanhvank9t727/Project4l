from flask import Blueprint
from flask import request
from flask import jsonify
from flask import current_app

from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt

from google.oauth2 import id_token
from google.auth.transport import requests

from database.db import db

from models.user_model import G4User

from services.jwt_services import generate_tokens

from utils.response import success_response, error_response
from utils.validators import is_valid_email, is_strong_password
from utils.constants import ROLE_LOCKED, ROLE_CUSTOMER, AUTH_PROVIDER_LOCAL, AUTH_PROVIDER_GOOGLE

import bcrypt

auth_routes = Blueprint(
    "auth_routes",
    __name__
)

@auth_routes.route(
    "/register",
    methods=["POST"]
)
def register():

    data = request.get_json(silent=True)

    if not data:
        return error_response("Invalid JSON", 400)

    email = data.get("email")
    password = data.get("password")
    full_name = data.get("full_name")

    if not email or not password or not full_name:
        return error_response("Missing required fields", 400)

    if not is_valid_email(email):
        return error_response("Email không hợp lệ", 400)

    if not is_strong_password(password):
        return error_response(
            "Mật khẩu phải có ít nhất 6 ký tự, gồm chữ hoa, chữ thường và số",
            400
        )

    existing_user = G4User.query.filter_by(
        HKKM_Email=email
    ).first()

    if existing_user:
        return error_response("Email already exists", 400)

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    new_user = G4User(
        HKKM_Email=email,
        HKKM_Password_Hash=hashed_password,
        HKKM_Full_Name=full_name,
        HKKM_Auth_Provider=AUTH_PROVIDER_LOCAL
    )

    db.session.add(new_user)
    db.session.commit()

    return success_response("Register successful", None, 201)

@auth_routes.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json(silent=True)

    if not data:
        return error_response("Invalid JSON", 400)

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error_response("Email and password required", 400)

    user = G4User.query.filter_by(
        HKKM_Email=email
    ).first()

    if not user:
        return error_response("Invalid email or password", 401)

    # Kiểm tra tài khoản bị khóa
    if user.HKKM_Role == ROLE_LOCKED:
        return error_response(
            "Tài khoản của bạn đã bị khóa. Vui lòng liên hệ admin.",
            403
        )

    if not user.HKKM_Password_Hash:
        return error_response(
            "Please login with your Google account",
            401
        )

    try:
        password_valid = bcrypt.checkpw(
            password.encode("utf-8"),
            user.HKKM_Password_Hash.encode("utf-8")
        )
    except ValueError:
        return error_response(
            "Invalid password format in database",
            500
        )

    if not password_valid:
        return error_response("Invalid email or password", 401)

    tokens = generate_tokens(user)

    return jsonify({

        "message": "Login successful",

        "access_token": tokens[
            "access_token"
        ],

        "refresh_token": tokens[
            "refresh_token"
        ],

        "user": {

            "id": user.HKKM_Id,

            "email": user.HKKM_Email,

            "full_name": user.HKKM_Full_Name,

            "role": user.HKKM_Role
        }

    }), 200

@auth_routes.route(
    "/google",
    methods=["POST"]
)
def google_login():

    data = request.get_json(
        silent=True
    )

    if not data:
        return error_response("Invalid JSON", 400)

    google_token = data.get("token")

    if not google_token:
        return error_response("Google token required", 400)

    try:

        user_info = id_token.verify_oauth2_token(

            google_token,

            requests.Request(),

            current_app.config[
                "GOOGLE_CLIENT_ID"
            ]
        )

        email = user_info["email"]

        user = G4User.query.filter_by(
            HKKM_Email=email
        ).first()

        # Kiểm tra tài khoản bị khóa
        if user and user.HKKM_Role == ROLE_LOCKED:
            return error_response(
                "Tài khoản của bạn đã bị khóa. Vui lòng liên hệ admin.",
                403
            )

        if not user:

            user = G4User(

                HKKM_Email=email,

                HKKM_Full_Name=user_info.get(
                    "name",
                    "Google User"
                ),

                HKKM_Auth_Provider=AUTH_PROVIDER_GOOGLE,

                HKKM_Provider_Id=user_info["sub"],

                HKKM_Avatar_Url=user_info.get(
                    "picture"
                ),

                HKKM_Is_Email_Verified=True
            )

            db.session.add(user)

            db.session.commit()

        tokens = generate_tokens(user)

        return jsonify({

            "message": "Google login successful",

            "access_token": tokens[
                "access_token"
            ],

            "refresh_token": tokens[
                "refresh_token"
            ],

            "user": {

                "id": user.HKKM_Id,

                "email": user.HKKM_Email,

                "full_name": user.HKKM_Full_Name,

                "role": user.HKKM_Role
            }

        }), 200

    except Exception:

        return error_response("Invalid Google token", 401)

@auth_routes.route(
    "/refresh",
    methods=["POST"]
)
@jwt_required(refresh=True)
def refresh():

    user_id = get_jwt_identity()

    user = db.session.get(G4User, user_id)

    if not user:
        return error_response("User not found", 404)

    # Kiểm tra tài khoản bị khóa khi refresh
    if user.HKKM_Role == ROLE_LOCKED:
        return error_response(
            "Tài khoản của bạn đã bị khóa.",
            403
        )

    tokens = generate_tokens(user)

    return jsonify({

        "access_token": tokens[
            "access_token"
        ]

    }), 200

@auth_routes.route(
    "/profile",
    methods=["GET"]
)
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    claims = get_jwt()

    return jsonify({

        "message": "Access granted",

        "user_id": user_id,

        "email": claims["email"],

        "role": claims["role"]

    }), 200