from flask import Blueprint

from controllers.products_controller import get_products
from controllers.products_controller import get_product_detail


product_routes = Blueprint(
    "product_routes",
    __name__
)


@product_routes.route(
    "/",
    methods=["GET"]
)
def products():

    return get_products()


@product_routes.route(
    "/<int:product_id>",
    methods=["GET"]
)
def product_detail(product_id):

    return get_product_detail(
        product_id
    )