from .db import db


class User(db.Document):
    username = db.StringField(required=True, unique=True)
    passwordHash = db.StringField(required=True)
