from flask import Response, request
from flask_restful import Resource
import flask_bcrypt
import json
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime  # for token expiry
from uuid import uuid4

from database.models import Item, User

SALTS = 10
VALIDITY = 360


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
        try:
            user = User.objects.get(username=request_body.get("username"))
        except Exception:
            response = {"error": "Wrong username or password."}
            status = 400

        else:
            passwordMatch = flask_bcrypt.check_password_hash(
                user.passwordHash, request_body.get("password")
            )

            if passwordMatch:
                token = create_access_token(
                    identity=str(user.id),
                    expires_delta=datetime.timedelta(minutes=VALIDITY),
                )  # 30mins validity
                response = {"token": token}
                status = 200

            else:
                response = {"error": "Wrong username or password."}
                status = 400

        return Response(
            json.dumps(response), status=status, mimetype="application/json"
        )


class CartApi(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        loggedInUser = User.objects.only("username", "cart").get(id=user_id).to_mongo()

        response = {
            "username": loggedInUser.get("username"),
            "cart": loggedInUser.get("cart"),
        }
        return Response(json.dumps(response), status=200, mimetype="application/json")

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        request_body = request.json

        logged_in_user = User.objects.get(id=user_id)

        item_quantity = request_body.get("quantity", 1)

        # Check if an item of the same name exists, to see if it raises an exception.
        try:
            item_name = logged_in_user.cart.filter(name=request_body.get("name"))[
                0
            ].name
        except IndexError:  # if the item does not exist, add the new item.
            item = Item(
                id=str(uuid4()), name=request_body.get("name"), quantity=item_quantity
            )
            logged_in_user.cart.append(item)
        else:  # If it exists, increase the quantity by the number specified.
            logged_in_user.cart.get(
                name=request_body.get("name")
            ).quantity += item_quantity

        logged_in_user.save()

        response = {
            "username": logged_in_user.username,
            "item": logged_in_user.cart.get(name=request_body.get("name")).to_mongo(),
        }

        return Response(json.dumps(response), status=200, mimetype="application/json")

    # Add post, put and delete
    # comment code


class ItemApi(Resource):
    @jwt_required()
    def get(self, id):
        user_id = get_jwt_identity()

        loggedInUser = User.objects.only("username", "cart").get(id=user_id)

        try:  # check if the item exists
            item = loggedInUser.cart.filter(id=id)[0]
        except IndexError:  # if it doesn't, return.
            response = {"error": "An item with that ID does not exist."}
            status = 404
        else:  # else, return the item.
            response = {"username": loggedInUser.username, "item": item.to_mongo()}
            status = 200

        return Response(
            json.dumps(response), status=status, mimetype="application/json"
        )

    @jwt_required()
    def put(self, id):
        user_id = get_jwt_identity()

        request_body = request.json

        if request_body is None:
            response = {"error": "Quantity not specified."}
            status = 400

        else:
            loggedInUser = User.objects.get(id=user_id)

            try:  # check if the item exists
                item = loggedInUser.cart.filter(id=id)[0]
            except IndexError:  # if it doesn't, return.
                response = {"error": "An item with that ID does not exist."}
                status = 404
            else:  # else, return the item.
                item.quantity = request_body.get("quantity")
                loggedInUser.save()

                response = {"username": loggedInUser.username, "item": item.to_mongo()}
                status = 200

        return Response(
            json.dumps(response), status=status, mimetype="application/json"
        )

    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()

        User.objects(id=user_id).update_one(pull__cart__id=id)

        return Response(status=204, mimetype="application/json")
