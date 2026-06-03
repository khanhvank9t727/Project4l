from database.db import db
from models.products_model import G4Product
from models.order_model import G4Order, G4OrderItem
from models.user_model import G4User
from utils.response import success_response, error_response
from utils.constants import (
    VALID_ORDER_STATUSES, VALID_STATUS_TRANSITIONS,
    ORDER_STATUS_CANCELLED, ORDER_STATUS_PENDING,
    ROLE_ADMIN, ROLE_LOCKED, ROLE_CUSTOMER
)
from flask import request
from sqlalchemy.orm import joinedload
from datetime import datetime


def get_dashboard_stats():
    now = datetime.utcnow()
    first_day = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    total_orders = G4Order.query.count()
    
    # Doanh thu tháng hiện tại (loại bỏ đơn hủy)
    total_revenue = db.session.query(db.func.sum(G4Order.HKKM_Total_Amount)).filter(
        db.and_(
            G4Order.HKKM_Status != ORDER_STATUS_CANCELLED,
            G4Order.HKKM_Created_At >= first_day
        )
    ).scalar() or 0
    
    total_users = G4User.query.filter_by(HKKM_Role=ROLE_CUSTOMER).count()
    total_products = G4Product.query.count()
    
    return success_response("Stats fetched successfully", {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "total_users": total_users,
        "total_products": total_products
    })


def create_product():
    data = request.get_json()
    if not data:
        return error_response("Invalid data", 400)

    name = data.get("name")
    if not name or not name.strip():
        return error_response("Tên sản phẩm không được để trống", 400)

    try:
        price = float(data.get("price", 0))
        stock = int(data.get("stock", 0))
        if price < 0:
            return error_response("Giá không được âm", 400)
        if stock < 0:
            return error_response("Số lượng kho không được âm", 400)
    except (ValueError, TypeError):
        return error_response("Giá hoặc số lượng không hợp lệ", 400)

    try:
        new_product = G4Product(
            HKKM_Name=name.strip(),
            HKKM_Description=data.get("description", ""),
            HKKM_Base_Price=price,
            HKKM_Stock_Quantity=stock,
            HKKM_Category_Id=data.get("category_id"),
            HKKM_Brand_Id=data.get("brand_id"),
            HKKM_Gender=data.get("gender"),
            HKKM_Age_Range=data.get("age_range")
        )
        db.session.add(new_product)
        db.session.commit()
        return success_response("Product created successfully", {"id": new_product.HKKM_Id}, 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error creating product: {str(e)}", 500)


def update_product(product_id):
    product = db.session.get(G4Product, product_id)
    if not product:
        return error_response("Product not found", 404)
        
    data = request.get_json()
    if not data:
        return error_response("Invalid data", 400)

    try:
        product.HKKM_Name = data.get("name", product.HKKM_Name)
        product.HKKM_Description = data.get("description", product.HKKM_Description)
        product.HKKM_Base_Price = float(data.get("price", product.HKKM_Base_Price))
        product.HKKM_Stock_Quantity = int(data.get("stock", product.HKKM_Stock_Quantity))
        product.HKKM_Category_Id = data.get("category_id", product.HKKM_Category_Id)
        product.HKKM_Brand_Id = data.get("brand_id", product.HKKM_Brand_Id)
        product.HKKM_Gender = data.get("gender", product.HKKM_Gender)
        product.HKKM_Age_Range = data.get("age_range", product.HKKM_Age_Range)
        
        db.session.commit()
        return success_response("Product updated successfully")
    except (ValueError, TypeError) as e:
        db.session.rollback()
        return error_response(f"Giá trị không hợp lệ: {str(e)}", 400)
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error updating product: {str(e)}", 500)


def delete_product(product_id):
    product = db.session.get(G4Product, product_id)
    if not product:
        return error_response("Product not found", 404)

    # Kiểm tra sản phẩm đã có trong đơn hàng chưa
    has_orders = G4OrderItem.query.filter_by(HKKM_Product_Id=product_id).first()
    if has_orders:
        return error_response("Không thể xóa sản phẩm đã có trong đơn hàng", 400)

    try:
        db.session.delete(product)
        db.session.commit()
        return success_response("Product deleted successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Error deleting product: {str(e)}", 500)

    
def update_order_status(order_id):
    order = db.session.get(G4Order, order_id)
    if not order:
        return error_response("Order not found", 404)
        
    data = request.get_json()
    new_status = data.get("status")
    if not new_status:
        return error_response("Missing status", 400)

    # Validate status value
    if new_status not in VALID_ORDER_STATUSES:
        return error_response(f"Trạng thái '{new_status}' không hợp lệ", 400)
    
    # Validate status transition (state machine)
    current_status = order.HKKM_Status
    allowed = VALID_STATUS_TRANSITIONS.get(current_status, [])
    if new_status not in allowed and new_status != current_status:
        return error_response(
            f"Không thể chuyển từ '{current_status}' sang '{new_status}'", 400
        )
        
    order.HKKM_Status = new_status
    db.session.commit()
    return success_response("Order status updated successfully")


def get_all_orders():
    # Fix N+1 query: dùng joinedload để eager-load items + product + user
    orders = G4Order.query.options(
        joinedload(G4Order.items).joinedload(G4OrderItem.product),
        joinedload(G4Order.user)
    ).order_by(G4Order.HKKM_Created_At.desc()).all()
    
    order_list = []
    for order in orders:
        products_names = []
        for item in order.items:
            if item.product:
                products_names.append(f"{item.product.HKKM_Name} (x{item.HKKM_Quantity})")
            
        user = order.user
        order_list.append({
            "id": order.HKKM_Id,
            "code": f"#G4-{1000 + order.HKKM_Id}",
            "customer": user.HKKM_Full_Name if user else "Khách Vãng Lai",
            "phone": order.HKKM_Ship_Phone or (user.HKKM_Phone if user and user.HKKM_Phone else "Không có"),
            "ship_name": order.HKKM_Ship_Name or (user.HKKM_Full_Name if user else ""),
            "total": order.HKKM_Total_Amount,
            "status": order.HKKM_Status,
            "date": order.HKKM_Created_At.strftime("%d/%m/%Y") if order.HKKM_Created_At else "",
            "products": products_names,
            "shipping_address": order.HKKM_Shipping_Address or "Không có",
            "payment_method": order.HKKM_Payment_Method or "N/A"
        })
    return success_response("Orders fetched successfully", order_list)


def get_all_users():
    users = G4User.query.order_by(G4User.HKKM_Id.desc()).all()
    user_list = []
    for user in users:
        user_list.append({
            "id": f"#U{user.HKKM_Id:03d}",
            "raw_id": user.HKKM_Id,
            "name": user.HKKM_Full_Name,
            "email": user.HKKM_Email,
            "role": user.HKKM_Role,
            "date": user.HKKM_Created_At.strftime("%d/%m/%Y") if user.HKKM_Created_At else ""
        })
    return success_response("Users fetched successfully", user_list)


def lock_user(user_id):
    user = db.session.get(G4User, user_id)
    if not user:
        return error_response("User not found", 404)
    if user.HKKM_Role == ROLE_ADMIN:
        return error_response("Cannot lock an admin", 400)
    if user.HKKM_Role == ROLE_LOCKED:
        return error_response("User is already locked", 400)
        
    user.HKKM_Role = ROLE_LOCKED
    db.session.commit()
    return success_response("User locked successfully")


def unlock_user(user_id):
    user = db.session.get(G4User, user_id)
    if not user:
        return error_response("User not found", 404)
    if user.HKKM_Role != ROLE_LOCKED:
        return error_response("User is not locked", 400)
    
    user.HKKM_Role = ROLE_CUSTOMER
    db.session.commit()
    return success_response("User unlocked successfully")
