from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.paypal_controller import create_order, capture_order

paypal_routes = Blueprint("paypal_routes", __name__)

@paypal_routes.route("/create-order", methods=["POST"])
@jwt_required()
def paypal_create_order():
    user_id = get_jwt_identity()
    return create_order(user_id)

@paypal_routes.route("/capture-order", methods=["POST"])
@jwt_required()
def paypal_capture_order():
    user_id = get_jwt_identity()
    return capture_order(user_id)
