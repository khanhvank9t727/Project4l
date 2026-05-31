from models.products_model import G4Product

from utils.response import success_response
from utils.response import error_response


def get_products():

    products = G4Product.query.all()

    product_list = []

    for product in products:

        product_list.append({

            "id": product.HKKM_Id,

            "name": product.HKKM_Name,

            "description": product.HKKM_Description,

            "price": product.HKKM_Base_Price,

            "stock": product.HKKM_Stock_Quantity,

            "brand_id": product.HKKM_Brand_Id,

            "gender": product.HKKM_Gender,

            "age_range": product.HKKM_Age_Range
        })

    return success_response(
        "Products fetched successfully",
        product_list
    )


def get_product_detail(product_id):

    product = G4Product.query.get(product_id)

    if not product:

        return error_response(
            "Product not found",
            404
        )

    product_data = {

        "id": product.HKKM_Id,

        "name": product.HKKM_Name,

        "description": product.HKKM_Description,

        "price": product.HKKM_Base_Price,

        "stock": product.HKKM_Stock_Quantity,

        "brand_id": product.HKKM_Brand_Id,

        "gender": product.HKKM_Gender,

        "age_range": product.HKKM_Age_Range
    }

    return success_response(
        "Product detail fetched successfully",
        product_data
    )