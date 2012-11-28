import os

HERE = os.path.dirname(__file__)
SQLITE_NAME = "athena.sqlite"
SQLALCHEMY_DATABASE_URI = "sqlite:////" + HERE + "/" + SQLITE_NAME
SQLALCHEMY_ECHO = False
