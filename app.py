from flask import Flask
from flask_jwt_extended.jwt_manager import JWTManager
from flask_restful import Api
from flask_bcrypt import Bcrypt
import json
import os

from resources.router import init_routes
from database.db import initialize
from database.models import User

app = Flask(__name__)

os.environ["MONGO_KEY"] = "<paste_your_connection_string_here>"

os.environ["JWT_SECRET"] = "<paste_your_jwt_secret_here>"

# Connect to MongoDB
app.config["MONGODB_HOST"] = os.environ.get("MONGO_KEY")

# JWT Secret
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET")

api = Api(app)
bcrypt = Bcrypt(app)
initialize(app)
jwt = JWTManager(app)

init_routes(api)

app.run()
