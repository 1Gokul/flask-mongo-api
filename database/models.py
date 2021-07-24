from enum import unique
from .db import db


class Item(db.EmbeddedDocument):
    item_id = db.StringField(required=True)
    name = db.StringField(required=True)
    quantity = db.IntField(required=True)


class User(db.Document):
    username = db.StringField(required=True, unique=True)
    passwordHash = db.StringField(required=True)
    cart = db.EmbeddedDocumentListField(Item, default=[])
