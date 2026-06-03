import os
from flask import Flask
from config import Config
from database.db import db

# Import tất cả các Models để SQLAlchemy nhận diện được
from models.user_model import G4User
from models.category_model import G4Category
from models.products_model import G4Product
from models.cart_model import G4Cart, G4CartItem
from models.order_model import G4Order, G4OrderItem

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def init_database():
    with app.app_context():
        print("Đang kiểm tra và tạo các bảng còn thiếu trong Database...")
        # Lệnh này sẽ CHỈ TẠO THÊM các bảng chưa tồn tại (như G4_Cart, G4_Orders) 
        # và GIỮ NGUYÊN dữ liệu của các bảng đã có (G4_Users, G4_Products, G4_Categories)
        db.create_all()
        print("Hoàn tất! Các bảng mới đã được tạo thành công.")

if __name__ == "__main__":
    init_database()
