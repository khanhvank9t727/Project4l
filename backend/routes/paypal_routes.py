from flask import Blueprint

from controllers.paypal_controller import create_order
from controllers.paypal_controller import capture_order


paypal_routes = Blueprint(
    "paypal_routes",
    __name__
)


@paypal_routes.route(
    "/create-order",
    methods=["POST"]
)
def paypal_create_order():

    return create_order()


@paypal_routes.route(
    "/capture-order",
    methods=["POST"]
)
def paypal_capture_order():

    return capture_order()
