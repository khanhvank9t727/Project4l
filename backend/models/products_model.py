from database.db import db


class G4Product(db.Model):

    __tablename__ = "G4_Products"

    HKKM_Id = db.Column(
        db.Integer,
        primary_key=True
    )

    HKKM_Name = db.Column(
        db.String(255),
        nullable=False
    )

    HKKM_Description = db.Column(
        db.Text
    )

    HKKM_Base_Price = db.Column(
        db.Float,
        nullable=False
    )

    HKKM_Stock_Quantity = db.Column(
        db.Integer,
        default=0
    )

    HKKM_Category_Id = db.Column(
        db.Integer,
        db.ForeignKey("G4_Categories.HKKM_Id")
    )

    HKKM_Brand_Id = db.Column(
        db.Integer
    )

    HKKM_Gender = db.Column(
        db.String(20)
    )

    HKKM_Age_Range = db.Column(
        db.String(50)
    )