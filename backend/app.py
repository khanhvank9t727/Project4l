from flask import Flask

from flask_cors import CORS

from config import Config

from database.db import db

from flask_jwt_extended import JWTManager

from models.category_model import G4Category
from models.products_model import G4Product
from models.cart_model import G4Cart, G4CartItem
from models.order_model import G4Order, G4OrderItem

from routes.auth_routes import auth_routes

from routes.products_routes import product_routes

from routes.paypal_routes import paypal_routes
from routes.cart_routes import cart_routes
from routes.orders_routes import orders_routes
from routes.categories_routes import category_routes
from routes.admin_routes import admin_routes

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

    app.register_blueprint(
        paypal_routes,
        url_prefix="/api/paypal"
    )
    
    app.register_blueprint(
        cart_routes,
        url_prefix="/api/cart"
    )
    
    app.register_blueprint(
        orders_routes,
        url_prefix="/api/orders"
    )
    
    app.register_blueprint(
        category_routes,
        url_prefix="/api/categories"
    )
    
    app.register_blueprint(
        admin_routes,
        url_prefix="/api/admin"
    )

    @app.route("/")
    def home():

        return {
            "message": "G4 ToyStore Backend Running"
        }

    return app