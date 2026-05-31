import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import bcrypt

from app import create_app

from database.db import db

from models.user_model import G4User
from models.category_model import G4Category
from models.products_model import G4Product


app = create_app()


def seed_admin():

    existing_admin = G4User.query.filter_by(
        HKKM_Email="admin@g4toy.com"
    ).first()

    if existing_admin:

        print("Admin already exists")
        return

    hashed_password = bcrypt.hashpw(
        "123456".encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    admin = G4User(

        HKKM_Email="admin@g4toy.com",

        HKKM_Password_Hash=hashed_password,

        HKKM_Full_Name="Administrator",

        HKKM_Role="ADMIN",

    )

    db.session.add(admin)

    db.session.commit()

    print("Admin account created")


def seed_products():

    existing_category = G4Category.query.filter_by(
        HKKM_Name="LEGO"
    ).first()

    if existing_category:

        print("Products already seeded")
        return

    category = G4Category(

        HKKM_Name="LEGO",

    )

    db.session.add(category)

    db.session.commit()

    product = G4Product(
        HKKM_Id=1,

        HKKM_Category_Id=category.HKKM_Id,

        HKKM_Brand_Id=1,

        HKKM_Age_Range="8-14",

        HKKM_Gender="Unisex",

        HKKM_Name="LEGO Technic",

        HKKM_Description="STEM Building Toy",

        HKKM_Base_Price=500000,

        HKKM_Stock_Quantity=10

    )

    db.session.add(product)

    db.session.commit()

    print("Products seeded")


if __name__ == "__main__":

    with app.app_context():

        seed_admin()

        seed_products()