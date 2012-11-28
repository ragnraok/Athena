from Athena.app import app
app.config.from_pyfile("config.py")

from Athena.user import models # it must import models before create_all
from Athena.database import db
db.create_all()
