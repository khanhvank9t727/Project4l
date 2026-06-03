from flask import request
from database.db import db
from services.paypal_service import create_paypal_order, capture_paypal_order
from utils.response import success_response, error_response
from models.cart_model import G4Cart, G4CartItem
from models.products_model import G4Product
from models.order_model import G4Order, G4OrderItem
from utils.constants import ORDER_STATUS_PENDING

VND_TO_USD_RATE = 25000

def create_order(user_id):
    try:
        cart = G4Cart.query.filter_by(HKKM_User_Id=user_id).first()
        if not cart:
            return error_response("Cart is empty", 400)
            
        items = G4CartItem.query.filter_by(HKKM_Cart_Id=cart.HKKM_Id).all()
        if not items:
            return error_response("Cart is empty", 400)
            
        total_vnd = 0
        for item in items:
            product = db.session.get(G4Product, item.HKKM_Product_Id)
            if product:
                # Kiểm tra tồn kho trước khi tạo đơn
                if product.HKKM_Stock_Quantity < item.HKKM_Quantity:
                    return error_response(
                        f"Sản phẩm '{product.HKKM_Name}' chỉ còn {product.HKKM_Stock_Quantity} trong kho",
                        400
                    )
                total_vnd += product.HKKM_Base_Price * item.HKKM_Quantity
                
        total_usd = total_vnd / VND_TO_USD_RATE
        if total_usd < 0.01:
            total_usd = 0.01
            
        description = f"Order for User ID {user_id} - G4 ToyStore"
        order_data = create_paypal_order(amount_usd=total_usd, description=description)
        
        return success_response("PayPal order created successfully", {
            "order_id": order_data["id"],
            "total_vnd": total_vnd,
            "total_usd": round(total_usd, 2),
            "status": order_data["status"]
        })
    except Exception as e:
        return error_response(f"Failed to create PayPal order: {str(e)}", 500)

def capture_order(user_id):
    try:
        data = request.get_json()
        if not data or not data.get("order_id"):
            return error_response("Missing order_id", 400)
            
        paypal_order_id = data["order_id"]
        shipping_address = data.get("shipping_address", "")
        ship_name = data.get("ship_name", "")
        ship_phone = data.get("ship_phone", "")
        
        capture_data = capture_paypal_order(paypal_order_id)
        
        # Check if capture was successful (status COMPLETED)
        if capture_data.get("status") != "COMPLETED":
             return error_response("PayPal payment not completed", 400)
        
        # Create G4Order
        cart = G4Cart.query.filter_by(HKKM_User_Id=user_id).first()
        items = G4CartItem.query.filter_by(HKKM_Cart_Id=cart.HKKM_Id).all()
        
        total_vnd = 0
        order_items = []
        for item in items:
            product = db.session.get(G4Product, item.HKKM_Product_Id)
            if product:
                # Kiểm tra và trừ tồn kho
                if product.HKKM_Stock_Quantity < item.HKKM_Quantity:
                    return error_response(
                        f"Sản phẩm '{product.HKKM_Name}' đã hết hàng",
                        400
                    )
                product.HKKM_Stock_Quantity -= item.HKKM_Quantity
                
                price = product.HKKM_Base_Price
                total_vnd += price * item.HKKM_Quantity
                order_item = G4OrderItem(
                    HKKM_Product_Id=product.HKKM_Id,
                    HKKM_Quantity=item.HKKM_Quantity,
                    HKKM_Price=price
                )
                order_items.append(order_item)
                
        new_order = G4Order(
            HKKM_User_Id=user_id,
            HKKM_Total_Amount=total_vnd,
            HKKM_Status=ORDER_STATUS_PENDING,
            HKKM_Payment_Method="PayPal",
            HKKM_Paypal_Order_Id=paypal_order_id,
            HKKM_Shipping_Address=shipping_address,
            HKKM_Ship_Name=ship_name,
            HKKM_Ship_Phone=ship_phone
        )
        db.session.add(new_order)
        db.session.commit() # Commit to get order ID
        
        for o_item in order_items:
            o_item.HKKM_Order_Id = new_order.HKKM_Id
            db.session.add(o_item)
            
        # Clear Cart
        for item in items:
            db.session.delete(item)
            
        db.session.commit()
        
        return success_response("Payment captured and order created successfully", {
            "order_id": new_order.HKKM_Id,
            "status": ORDER_STATUS_PENDING
        })
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to capture PayPal payment: {str(e)}", 500)
