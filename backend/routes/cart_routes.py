from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.cart_controller import get_cart, add_to_cart, update_cart_item, remove_from_cart, clear_cart
from utils.response import error_response

cart_routes = Blueprint("cart_routes", __name__)

@cart_routes.route("/", methods=["GET"], strict_slashes=False)
@jwt_required()
def fetch_cart():
    user_id = get_jwt_identity()
    return get_cart(user_id)

@cart_routes.route("/", methods=["POST"], strict_slashes=False)
@jwt_required()
def add_item():
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data or 'product_id' not in data:
        return error_response("Product ID is required", 400)
        
    product_id = data['product_id']
    quantity = data.get('quantity', 1)
    return add_to_cart(user_id, product_id, quantity)

@cart_routes.route("/<int:item_id>", methods=["PUT"], strict_slashes=False)
@jwt_required()
def update_item(item_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    if not data or 'quantity' not in data:
        return error_response("Quantity is required", 400)
        
    quantity = data['quantity']
    return update_cart_item(user_id, item_id, quantity)

@cart_routes.route("/<int:item_id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def remove_item(item_id):
    user_id = get_jwt_identity()
    return remove_from_cart(user_id, item_id)

@cart_routes.route("/clear", methods=["DELETE"])
@jwt_required()
def clear():
    user_id = get_jwt_identity()
    return clear_cart(user_id)
