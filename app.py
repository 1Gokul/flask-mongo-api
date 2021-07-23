from flask import Flask
from flask_jwt_extended.jwt_manager import JWTManager
from flask_restful import Api
from flask_bcrypt import Bcrypt
import json
import os

from resources.routes import init_routes
from database.db import initialize
from database.models import User

app = Flask(__name__)


# Connect to MongoDB
app.config[
    "MONGODB_HOST"
] = os.environ.get("MONGO_KEY")

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET")

api = Api(app)
bcrypt = Bcrypt(app)
initialize(app)
jwt = JWTManager(app)

init_routes(api)

app.run(debug=True)
