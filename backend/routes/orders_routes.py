from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.orders_controller import get_orders, get_order_detail

orders_routes = Blueprint("orders_routes", __name__)

@orders_routes.route("/", methods=["GET"])
@jwt_required()
def fetch_orders():
    user_id = get_jwt_identity()
    return get_orders(user_id)

@orders_routes.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def fetch_order_detail(order_id):
    user_id = get_jwt_identity()
    return get_order_detail(user_id, order_id)
