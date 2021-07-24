from . import users


def init_routes(api):
    api.add_resource(users.UserApi, "/api/users")
    api.add_resource(users.RegisterApi, "/api/register")
    api.add_resource(users.LoginApi, "/api/login")
    api.add_resource(users.CartApi, "/api/cart")
    api.add_resource(users.ItemApi, "/api/cart/<id>")
