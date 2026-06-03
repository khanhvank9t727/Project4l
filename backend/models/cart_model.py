from database.db import db
from datetime import datetime

class G4Cart(db.Model):
    __tablename__ = "G4_Cart"
    HKKM_Id = db.Column(db.Integer, primary_key=True)
    HKKM_User_Id = db.Column(db.Integer, db.ForeignKey("G4_Users.HKKM_Id"), nullable=False)
    HKKM_Created_At = db.Column(db.DateTime, default=datetime.utcnow)

class G4CartItem(db.Model):
    __tablename__ = "G4_Cart_Items"
    HKKM_Id = db.Column(db.Integer, primary_key=True)
    HKKM_Cart_Id = db.Column(db.Integer, db.ForeignKey("G4_Cart.HKKM_Id"), nullable=False)
    HKKM_Product_Id = db.Column(db.Integer, db.ForeignKey("G4_Products.HKKM_Id"), nullable=False)
    HKKM_Quantity = db.Column(db.Integer, default=1, nullable=False)
    
    # Relationships
    product = db.relationship("G4Product", backref="cart_items", lazy=True)
