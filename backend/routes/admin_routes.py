from flask import Blueprint

from middleware.auth_middleware import admin_required


admin_routes = Blueprint(
    "admin_routes",
    __name__
)


@admin_routes.route(
    "/dashboard",
    methods=["GET"]
)
@admin_required
def dashboard():

    return {
        "message": "Welcome Admin"
    }, 200