from flask import Flask

from flask_cors import CORS

from config import Config

from database.db import db

from flask_jwt_extended import JWTManager

from models.category_model import G4Category

from models.products_model import G4Product

from routes.auth_routes import auth_routes

from routes.products_routes import product_routes

from middleware.error_middleware import register_error_handlers


jwt = JWTManager()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "*"
            }
        }
    )

    db.init_app(app)

    jwt.init_app(app)

    register_error_handlers(app)

    app.register_blueprint(
        auth_routes,
        url_prefix="/api/auth"
    )

    app.register_blueprint(
        product_routes,
        url_prefix="/api/products"
    )

    @app.route("/")
    def home():

        return {
            "message": "G4 ToyStore Backend Running"
        }

    return app