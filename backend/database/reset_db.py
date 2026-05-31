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

from sqlalchemy import text

from app import create_app

from database.db import db


app = create_app()


DROP_FK_SQL = """

DECLARE @sql NVARCHAR(MAX) = ''

SELECT @sql +=
    'ALTER TABLE ' +
    QUOTENAME(OBJECT_SCHEMA_NAME(parent_object_id)) +
    '.' +
    QUOTENAME(OBJECT_NAME(parent_object_id)) +
    ' DROP CONSTRAINT ' +
    QUOTENAME(name) +
    ';'
FROM sys.foreign_keys

EXEC sp_executesql @sql

"""


DROP_TABLE_SQL = """

DECLARE @sql NVARCHAR(MAX) = ''

SELECT @sql +=
    'DROP TABLE ' +
    QUOTENAME(TABLE_SCHEMA) +
    '.' +
    QUOTENAME(TABLE_NAME) +
    ';'
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'

EXEC sp_executesql @sql

"""


with app.app_context():

    connection = db.engine.connect()

    print("Dropping foreign keys...")

    connection.execute(
        text(DROP_FK_SQL)
    )

    print("Dropping tables...")

    connection.execute(
        text(DROP_TABLE_SQL)
    )

    connection.commit()

    print("Creating tables...")

    db.create_all()

    print("Database reset successful")