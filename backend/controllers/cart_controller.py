from database.db import db
from models.cart_model import G4Cart, G4CartItem
from models.products_model import G4Product
from utils.response import success_response, error_response

def get_or_create_cart(user_id):
    cart = G4Cart.query.filter_by(HKKM_User_Id=user_id).first()
    if not cart:
        cart = G4Cart(HKKM_User_Id=user_id)
        db.session.add(cart)
        db.session.commit()
    return cart

def get_cart(user_id):
    cart = get_or_create_cart(user_id)
    items = G4CartItem.query.filter_by(HKKM_Cart_Id=cart.HKKM_Id).all()
    
    cart_list = []
    total = 0
    for item in items:
        product = G4Product.query.get(item.HKKM_Product_Id)
        if product:
            item_total = item.HKKM_Quantity * product.HKKM_Base_Price
            total += item_total
            cart_list.append({
                "id": item.HKKM_Id,
                "product_id": product.HKKM_Id,
                "name": product.HKKM_Name,
                "price": product.HKKM_Base_Price,
                "quantity": item.HKKM_Quantity,
                "item_total": item_total
            })
            
    return success_response("Cart fetched successfully", {
        "cart_id": cart.HKKM_Id,
        "items": cart_list,
        "total": total
    })

def add_to_cart(user_id, product_id, quantity=1):
    cart = get_or_create_cart(user_id)
    product = G4Product.query.get(product_id)
    if not product:
        return error_response("Product not found", 404)
        
    cart_item = G4CartItem.query.filter_by(HKKM_Cart_Id=cart.HKKM_Id, HKKM_Product_Id=product_id).first()
    if cart_item:
        cart_item.HKKM_Quantity += quantity
    else:
        cart_item = G4CartItem(HKKM_Cart_Id=cart.HKKM_Id, HKKM_Product_Id=product_id, HKKM_Quantity=quantity)
        db.session.add(cart_item)
        
    db.session.commit()
    return success_response("Added to cart successfully", None, 201)

def update_cart_item(user_id, item_id, quantity):
    cart = get_or_create_cart(user_id)
    cart_item = G4CartItem.query.filter_by(HKKM_Id=item_id, HKKM_Cart_Id=cart.HKKM_Id).first()
    if not cart_item:
        return error_response("Cart item not found", 404)
        
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.HKKM_Quantity = quantity
        
    db.session.commit()
    return success_response("Cart updated successfully")

def remove_from_cart(user_id, item_id):
    cart = get_or_create_cart(user_id)
    cart_item = G4CartItem.query.filter_by(HKKM_Id=item_id, HKKM_Cart_Id=cart.HKKM_Id).first()
    if not cart_item:
        return error_response("Cart item not found", 404)
        
    db.session.delete(cart_item)
    db.session.commit()
    return success_response("Removed from cart successfully")

def clear_cart(user_id):
    cart = get_or_create_cart(user_id)
    G4CartItem.query.filter_by(HKKM_Cart_Id=cart.HKKM_Id).delete()
    db.session.commit()
    return success_response("Cart cleared successfully")
