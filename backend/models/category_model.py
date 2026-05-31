from database.db import db


class G4Category(db.Model):

    __tablename__ = "G4_Categories"


    HKKM_Id = db.Column(
        db.Integer,
        primary_key=True
    )

    HKKM_Name = db.Column(
        db.String(100),
        nullable=False
    )

    HKKM_Parent_Id = db.Column(
        db.Integer,
        db.ForeignKey(
            "G4_Categories.HKKM_Id"
        )
    )

    HKKM_Icon_Url = db.Column(
        db.Text
    )

    HKKM_Level = db.Column(
        db.Integer,
        default=1
    )