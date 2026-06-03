from flask import Blueprint
from controllers.categories_controller import get_categories

category_routes = Blueprint("category_routes", __name__)

@category_routes.route("/", methods=["GET"], strict_slashes=False)
def fetch_categories():
    return get_categories()
