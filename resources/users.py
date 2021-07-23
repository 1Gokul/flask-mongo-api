from flask import Response, request
from flask_restful import Resource
import flask_bcrypt
import json
from flask_jwt_extended import create_access_token, jwt_required
import datetime  # for token expiry

from database.models import User

SALTS = 10
VALIDITY = 30


class UserApi(Resource):
    @jwt_required()
    def get(self):
        users = User.objects.only("id", "username").to_json()
        return Response(users, status=200)


class RegisterApi(Resource):
    def post(self):
        request_body = request.json

        new_user = User(
            username=request_body.get("username"),
            passwordHash=flask_bcrypt.generate_password_hash(
                request_body.get("password"), SALTS
            ),
        )

        new_user.save()

        response = {"id": str(new_user.id)}

        return Response(json.dumps(response), status=200, mimetype="application/json")


class LoginApi(Resource):
    def post(self):
        request_body = request.json
        print("USER", request_body.get("username"))
        try:
            user = User.objects.get(username=request_body.get("username")).to_mongo()
            print(user.get("passwordHash"))
        except Exception as e:
            response = {"error": "Wrong username or password."}
            return Response(
                json.dumps(response), status=403, mimetype="application/json"
            )

        else:
            passwordMatch = flask_bcrypt.check_password_hash(
                user.get("passwordHash"), request_body.get("password")
            )

            if passwordMatch:
                token = create_access_token(
                    str(user.get("id")), datetime.timedelta(minutes=VALIDITY)
                )  # 30mins validity
                response = {"token": token}
                return Response(
                    json.dumps(response), status=200, mimetype="application/json"
                )

            else:
                response = {"error": "Wrong username or password."}
                return Response(
                    json.dumps(response), status=403, mimetype="application/json"
                )
