from database.db import db


class G4User(db.Model):

    __tablename__ = "G4_Users"

    HKKM_Id = db.Column(
        db.Integer,
        primary_key=True
    )

    HKKM_Email = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )

    HKKM_Password_Hash = db.Column(
        db.String(255),
        nullable=True  # Nullable để hỗ trợ đăng nhập Google (không có mật khẩu)
    )

    HKKM_Full_Name = db.Column(
        db.String(100),
        nullable=False
    )

    HKKM_Phone = db.Column(
        db.String(20)
    )

    HKKM_Address = db.Column(
        db.Text
    )

    HKKM_Role = db.Column(
        db.String(50),
        default="Customer"
    )

    HKKM_Created_At = db.Column(
        db.DateTime,
        default=db.func.now()
    )

    HKKM_Auth_Provider = db.Column(
        db.String(20),
        default="LOCAL"
    )

    HKKM_Provider_Id = db.Column(
        db.String(255)
    )

    HKKM_Avatar_Url = db.Column(
        db.String(500)
    )

    HKKM_Is_Email_Verified = db.Column(
        db.Boolean,
        default=False
    )