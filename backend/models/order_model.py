from database.db import db
from datetime import datetime, timezone

class G4Order(db.Model):
    __tablename__ = "G4_Orders"
    HKKM_Id = db.Column(db.Integer, primary_key=True)
    HKKM_User_Id = db.Column(db.Integer, db.ForeignKey("G4_Users.HKKM_Id"), nullable=False)
    HKKM_Total_Amount = db.Column(db.Float, nullable=False)
    HKKM_Status = db.Column(db.String(50), default="Pending")
    HKKM_Payment_Method = db.Column(db.String(50), default="PayPal")
    HKKM_Paypal_Order_Id = db.Column(db.String(255))
    HKKM_Shipping_Address = db.Column(db.Text)
    HKKM_Ship_Name = db.Column(db.String(100))
    HKKM_Ship_Phone = db.Column(db.String(20))
    HKKM_Created_At = db.Column(db.DateTime, default=db.func.now())

    # Relationships
    user = db.relationship("G4User", backref="orders", lazy=True)
    items = db.relationship("G4OrderItem", backref="order", lazy=True, cascade="all, delete-orphan")

class G4OrderItem(db.Model):
    __tablename__ = "G4_Order_Items"
    HKKM_Id = db.Column(db.Integer, primary_key=True)
    HKKM_Order_Id = db.Column(db.Integer, db.ForeignKey("G4_Orders.HKKM_Id"), nullable=False)
    HKKM_Product_Id = db.Column(db.Integer, db.ForeignKey("G4_Products.HKKM_Id"), nullable=False)
    HKKM_Quantity = db.Column(db.Integer, nullable=False)
    HKKM_Price = db.Column(db.Float, nullable=False) # Store price at the time of order

    # Relationships
    product = db.relationship("G4Product", backref="order_items", lazy=True)
