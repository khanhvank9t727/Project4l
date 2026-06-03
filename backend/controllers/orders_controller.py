from database.db import db
from models.order_model import G4Order, G4OrderItem
from models.products_model import G4Product
from utils.response import success_response, error_response

def get_orders(user_id):
    orders = G4Order.query.filter_by(HKKM_User_Id=user_id).order_by(G4Order.HKKM_Created_At.desc()).all()
    order_list = []
    
    for order in orders:
        items = []
        for item in order.items:
            product = G4Product.query.get(item.HKKM_Product_Id)
            items.append({
                "product_id": item.HKKM_Product_Id,
                "name": product.HKKM_Name if product else "Unknown Product",
                "quantity": item.HKKM_Quantity,
                "price": item.HKKM_Price
            })
            
        order_list.append({
            "order_id": order.HKKM_Id,
            "total_amount": order.HKKM_Total_Amount,
            "status": order.HKKM_Status,
            "payment_method": order.HKKM_Payment_Method,
            "paypal_order_id": order.HKKM_Paypal_Order_Id,
            "shipping_address": order.HKKM_Shipping_Address,
            "created_at": order.HKKM_Created_At.isoformat() if order.HKKM_Created_At else None,
            "items": items
        })
        
    return success_response("Orders fetched successfully", order_list)

def get_order_detail(user_id, order_id):
    order = G4Order.query.filter_by(HKKM_Id=order_id, HKKM_User_Id=user_id).first()
    if not order:
        return error_response("Order not found", 404)
        
    items = []
    for item in order.items:
        product = G4Product.query.get(item.HKKM_Product_Id)
        items.append({
            "product_id": item.HKKM_Product_Id,
            "name": product.HKKM_Name if product else "Unknown Product",
            "quantity": item.HKKM_Quantity,
            "price": item.HKKM_Price
        })
        
    order_data = {
        "order_id": order.HKKM_Id,
        "total_amount": order.HKKM_Total_Amount,
        "status": order.HKKM_Status,
        "payment_method": order.HKKM_Payment_Method,
        "paypal_order_id": order.HKKM_Paypal_Order_Id,
        "shipping_address": order.HKKM_Shipping_Address,
        "created_at": order.HKKM_Created_At.isoformat() if order.HKKM_Created_At else None,
        "items": items
    }
    
    return success_response("Order detail fetched successfully", order_data)
