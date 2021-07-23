from flask_mongoengine import MongoEngine

db = MongoEngine()


def initialize(app):
    db.init_app(app)
