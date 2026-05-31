import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://@"
        f"{os.getenv('DB_SERVER')}/"
        f"{os.getenv('DB_NAME')}?"
        "driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")