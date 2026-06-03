from flask import Blueprint
from middleware.auth_middleware import admin_required
from controllers.admin_controller import (
    get_dashboard_stats, create_product, update_product, delete_product,
    update_order_status, get_all_orders, get_all_users, lock_user, unlock_user
)

admin_routes = Blueprint("admin_routes", __name__)

@admin_routes.route("/dashboard", methods=["GET"], strict_slashes=False)
@admin_required
def dashboard():
    return get_dashboard_stats()

@admin_routes.route("/products", methods=["POST"], strict_slashes=False)
@admin_required
def add_product():
    return create_product()

@admin_routes.route("/products/<int:product_id>", methods=["PUT"], strict_slashes=False)
@admin_required
def edit_product(product_id):
    return update_product(product_id)

@admin_routes.route("/products/<int:product_id>", methods=["DELETE"], strict_slashes=False)
@admin_required
def remove_product(product_id):
    return delete_product(product_id)

@admin_routes.route("/orders", methods=["GET"], strict_slashes=False)
@admin_required
def fetch_all_orders():
    return get_all_orders()
    
@admin_routes.route("/orders/<int:order_id>/status", methods=["PUT"], strict_slashes=False)
@admin_required
def change_order_status(order_id):
    return update_order_status(order_id)

@admin_routes.route("/users", methods=["GET"], strict_slashes=False)
@admin_required
def fetch_all_users():
    return get_all_users()

@admin_routes.route("/users/<int:user_id>/lock", methods=["PUT"], strict_slashes=False)
@admin_required
def block_user(user_id):
    return lock_user(user_id)

@admin_routes.route("/users/<int:user_id>/unlock", methods=["PUT"], strict_slashes=False)
@admin_required
def unblock_user(user_id):
    return unlock_user(user_id)