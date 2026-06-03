from models.category_model import G4Category
from utils.response import success_response, error_response

def get_categories():
    categories = G4Category.query.all()
    cat_list = []
    for cat in categories:
        cat_list.append({
            "id": cat.HKKM_Id,
            "name": cat.HKKM_Name
        })
    return success_response("Categories fetched successfully", cat_list)
