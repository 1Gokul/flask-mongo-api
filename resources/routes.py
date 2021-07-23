from .users import UserApi, RegisterApi, LoginApi


def init_routes(api):
    api.add_resource(UserApi, "/api/users")
    api.add_resource(RegisterApi, "/api/register")
    api.add_resource(LoginApi, "/api/login")
