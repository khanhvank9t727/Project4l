import os
from flask import Flask
from config import Config
from database.db import db
import bcrypt

# Import Models
from models.user_model import G4User
from models.category_model import G4Category
from models.products_model import G4Product
from models.cart_model import G4Cart, G4CartItem
from models.order_model import G4Order, G4OrderItem


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def seed_database():
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()

        print("Seeding Users...")
        admin_password = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        admin_user = G4User(
            HKKM_Email="admin@g4toystore.com",
            HKKM_Password_Hash=admin_password,
            HKKM_Full_Name="Super Admin",
            HKKM_Role="ADMIN",
            HKKM_Is_Email_Verified=True
        )
        db.session.add(admin_user)

        print("Seeding Categories...")
        cat1 = G4Category(HKKM_Name="Action Figures")
        cat2 = G4Category(HKKM_Name="Educational")
        cat3 = G4Category(HKKM_Name="Plush Toys")
        db.session.add_all([cat1, cat2, cat3])
        db.session.commit() # Commit to get Category IDs

        print("Seeding Products...")
        prod1 = G4Product(
            HKKM_Name="Superhero Action Figure",
            HKKM_Description="A really cool superhero with posable joints.",
            HKKM_Base_Price=25.99,
            HKKM_Stock_Quantity=100,
            HKKM_Category_Id=cat1.HKKM_Id,
            HKKM_Gender="Boy",
            HKKM_Age_Range="5-10"
        )
        prod2 = G4Product(
            HKKM_Name="Alphabet Blocks",
            HKKM_Description="Wooden blocks with letters and numbers.",
            HKKM_Base_Price=15.50,
            HKKM_Stock_Quantity=50,
            HKKM_Category_Id=cat2.HKKM_Id,
            HKKM_Gender="Unisex",
            HKKM_Age_Range="2-5"
        )
        prod3 = G4Product(
            HKKM_Name="Teddy Bear",
            HKKM_Description="Giant soft teddy bear for hugging.",
            HKKM_Base_Price=30.00,
            HKKM_Stock_Quantity=20,
            HKKM_Category_Id=cat3.HKKM_Id,
            HKKM_Gender="Girl",
            HKKM_Age_Range="All"
        )
        db.session.add_all([prod1, prod2, prod3])
        db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
